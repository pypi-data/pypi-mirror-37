"""Provides a SQLite 3 backed list implementation."""

import os
import sqlite3
from datetime import datetime
from uuid import uuid1

from task_forge.ql.tokens import Type
from task_forge.task import Note, Task

from . import InvalidConfigError, List as AList, NotFoundError


class List(AList):
    """A SQLite 3 backed list implementation."""

    __create_task_table = r"""
CREATE TABLE IF NOT EXISTS tasks(
    id text PRIMARY KEY,
    title text,
    body text,
    context text,
    priority real,
    created_date integer,
    completed_date integer
)"""

    __create_note_table = r"""
CREATE TABLE IF NOT EXISTS notes(
    task_id text,
    id text,
    body text,
    created_date integer,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
)"""

    __insert = r"""
INSERT INTO tasks
(
    id,
    title,
    body,
    context,
    priority,
    created_date,
    completed_date
)
VALUES (?,?,?,?,?,?,?)
"""

    __select = r"""
SELECT id, title, body, context, priority, created_date, completed_date
FROM tasks
"""

    def __init__(
            self,
            directory='',
            file_name='',
            create_tables=False,
    ):
        """Create a List from the given configuration.

        Either directory or file_name should be provided. Raises
        InvalidConfigError if neither are provided. If both are
        provided then file_name is used.

        create_tables forces the table creation query to
        run. Otherwise will create tables if the resulting sqlite db
        file does not already exist.
        """
        if not file_name and not directory:
            raise InvalidConfigError(
                'either directory or file_name must be provided')

        if not file_name:
            directory = directory.replace('~', os.getenv('HOME', os.getenv('APPDATALOCAL', '')))
            file_name = os.path.join(directory, 'tasks.sqlite3')

        parent = os.path.dirname(file_name)
        if not os.path.isdir(parent):
            os.makedirs(parent)

        if not os.path.isfile(file_name):
            create_tables = True

        self.conn = sqlite3.connect(file_name)
        if create_tables:
            self.conn.execute(self.__create_task_table)
            self.conn.execute(self.__create_note_table)

    @staticmethod
    def note_from_row(row):
        """Convert a SQL row tuple back into a Note object."""
        return Note(
            id=row[0],
            body=row[1],
            created_date=datetime.fromtimestamp(row[2]))

    @staticmethod
    def task_to_row(task):
        """Convert a task to a tuple with the correct column order."""
        return (
            task.id,
            task.title,
            task.body,
            task.context,
            task.priority,
            task.created_date.timestamp(),
            task.completed_date.timestamp() if task.completed_date else 0,
        )

    def task_from_row(self, row):
        """Convert a SQL row tuple back into a Task object.

        Raises a NotFoundError if row is None
        """
        if row is None:
            raise NotFoundError

        if len(row) != 7:
            raise NotFoundError

        return Task(
            id=row[0],
            title=row[1],
            body=row[2],
            context=row[3],
            priority=row[4],
            created_date=datetime.fromtimestamp(row[5]),
            completed_date=datetime.fromtimestamp(row[6]) if row[6] else None,
            notes=self.__get_notes(row[0]))

    def __get_notes(self, id):
        return [
            List.note_from_row(row) for row in self.conn.execute(
                'SELECT id, body, created_date FROM notes WHERE task_id = ?', (
                    id, ))
        ]

    def add(self, task):
        """Add a task to the List."""
        self.conn.\
            execute(self.__insert, List.task_to_row(task))
        self.conn.commit()

    def add_multiple(self, tasks):
        """Add multiple tasks to the List."""
        self.conn.\
            executemany(
                self.__insert,
                [List.task_to_row(task) for task in tasks])
        self.conn.commit()

    def list(self):
        """Return a python list of the Task in this List."""
        return [
            self.task_from_row(row) for row in self.conn.execute(self.__select)
        ]

    def find_by_id(self, task_id):
        """Find a task by task_id."""
        cursor = self.conn.execute(self.__select + 'WHERE id = ?', (task_id, ))
        return self.task_from_row(cursor.fetchone())

    def current(self):
        """Return the current task."""
        return self.task_from_row(
            self.conn.\
            execute(
                self.__select +
                "WHERE completed_date = 0 " +
                "ORDER BY priority DESC, created_date ASC"
            ).\
            fetchone())

    def complete(self, task_id):
        """Complete a task by task_id."""
        self.conn.\
            execute(
                'UPDATE tasks SET completed_date = ? WHERE id = ?',
                (datetime.now().timestamp(), task_id)
            )
        self.conn.commit()

    def update(self, task):
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        update_tuple = List.task_to_row(task)
        # move id to the end
        update_tuple = (
            update_tuple[1],
            update_tuple[2],
            update_tuple[3],
            update_tuple[4],
            update_tuple[5],
            update_tuple[6],
            update_tuple[0],
        )
        self.conn.execute(
            r"""
UPDATE tasks
SET
    title = ?,
    body = ?,
    context = ?,
    priority = ?,
    created_date = ?,
    completed_date = ?
WHERE id = ?
""", update_tuple)
        self.conn.commit()

    def add_note(self, task_id, note):
        """Add note to a task by task_id."""
        self.conn.\
            execute(
                'INSERT INTO notes (task_id, id, body, created_date) VALUES (?, ?, ?, ?)',
                (
                    task_id,
                    note.id,
                    note.body,
                    note.created_date.timestamp(),
                )
            )
        self.conn.commit()

    def search(self, ast):
        """Evaluate the AST and return a List of matching results."""
        where, values = List.__eval(ast.expression)
        return [
            self.task_from_row(task)
            for task in self.conn.execute(self.__select + 'WHERE ' +
                                          where, values)
        ]

    @staticmethod
    def __eval(expression):
        """Evaluate expression returning a where clause and a dictionary of values."""
        if expression.is_str_literal():
            return List.__eval_str_literal(expression)

        if expression.is_infix():
            return List.__eval_infix(expression)

        return ('', {})

    @staticmethod
    def __eval_str_literal(expression):
        """Evaluate a string literal query."""
        ident = uuid1().hex
        return ("(title LIKE :{ident} OR body LIKE :{ident})".format(
            ident=ident), {
                ident: '%{}%'.format(expression.value)
            })

    @staticmethod
    def __eval_infix(expression):
        """Evaluate an infix expression."""
        if expression.is_logical_infix():
            left, left_values = List.__eval(expression.left)
            right, right_values = List.__eval(expression.right)
            return ('({}) {} ({})'.format(
                left,
                expression.operator.literal,
                right,
            ), {
                **left_values,
                **right_values
            })

        ident = uuid1().hex
        if (expression.left.value == 'completed'
                and expression.right.is_boolean_literal()):
            return ('completed_date != 0'
                    if expression.right.value else 'completed_date = 0', {})

        if expression.operator.token_type == Type.LIKE:
            return ('({} LIKE :{})'.format(expression.left.value, ident), {
                ident: '%{}%'.format(expression.right.value)
            })

        return ('({} {} :{})'.format(expression.left.value,
                                     expression.operator.literal, ident), {
                                         ident: expression.right.value
                                     })
