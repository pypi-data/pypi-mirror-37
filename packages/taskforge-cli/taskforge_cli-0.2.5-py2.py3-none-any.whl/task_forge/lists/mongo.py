"""Provides a MongoDB backed list implementation."""

from datetime import datetime

try:
    import pymongo
except ImportError:
    import sys
    print('you must install pymongo to use the MongoDB list')
    sys.exit(1)

from task_forge.ql.tokens import Type
from task_forge.task import Task

from . import List as AList


class List(AList):
    """A MongoDB backed list implementation."""

    def __init__(
            self,
            host='localhost',
            port=27017,
            db='task_forge',
            collection='tasks',
            username=None,
            password=None,
            ssl=False,
    ):
        """Create a List from the given configuration."""
        conn_url = 'mongodb://'
        if username and password:
            conn_url += '{}:{}@'.format(username, password)
        elif username:
            conn_url += '{}@'.format(username)
        conn_url += '{}:{}'.format(host, port)
        self._client = pymongo.MongoClient(conn_url, ssl=ssl)
        self._db = self._client[db]
        self._collection = self._db[collection]

    def add(self, task):
        """Add a task to the List."""
        self._collection.insert_one(task.to_dict())

    def add_multiple(self, tasks):
        """Add multiple tasks to the List."""
        self._collection.insert_many([task.to_dict() for task in tasks])

    def list(self):
        """Return a python list of the Task in this List."""
        return [
            Task.from_dict(doc)
            for doc in self._collection.find(projection={"_id": False})
        ]

    def find_by_id(self, task_id):
        """Find a task by task_id."""
        return Task.from_dict(
            self._collection.find_one({
                "id": task_id
            },
                                      projection={"_id": False}))

    def current(self):
        """Return the current task."""
        doc = self._collection.find_one({
            "completed_date": None,
        },
                                        projection={"_id": False},
                                        sort=[
                                            ("priority", pymongo.DESCENDING),
                                            ("created_date",
                                             pymongo.ASCENDING),
                                        ])
        return Task.from_dict(doc)

    def complete(self, task_id):
        """Complete a task by task_id."""
        self._collection.find_one_and_update({
            "id": task_id
        }, {"$set": {
            "completed_date": datetime.now()
        }})

    def update(self, task):
        """
        Update a task in the list.

        The original is retrieved using the task_id of the given task.
        """
        doc = task.to_dict()
        doc["id"] = doc["id"]
        del doc["id"]

        self._collection.find_one_and_update({"id": task.id}, {"$set": doc})

    def add_note(self, task_id, note):
        """Add note to a task by task_id."""
        self._collection.find_one_and_update({
            "id": task_id
        }, {"$push": {
            "notes": note.to_dict()
        }})

    def search(self, ast):
        """Evaluate the AST and return a List of matching results."""
        return [
            Task.from_dict(doc) for doc in self._collection.find(
                self.__eval(ast.expression), projection={"_id": False})
        ]

    @staticmethod
    def __eval(expression):
        """Evaluate expression returning dictionary for use as a MongoDB query."""
        if expression.is_str_literal():
            return List.__eval_str_literal(expression)

        if expression.is_infix():
            return List.__eval_infix(expression)

        return {}

    @staticmethod
    def __eval_str_literal(expression):
        """Evaluate a string literal query."""
        return {
            "$or": [
                {
                    "title": {
                        "$regex": expression.value
                    }
                },
                {
                    "body": {
                        "$regex": expression.value
                    }
                },
                {
                    "notes": {
                        "$regex": expression.value
                    }
                },
            ]
        }

    @staticmethod
    def __eval_infix(expression):
        """Evaluate an infix expression."""
        if expression.is_logical_infix():
            return {
                "${}".format(expression.operator.literal.lower()): [
                    List.__eval(expression.left),
                    List.__eval(expression.right),
                ]
            }

        if (expression.left.value == 'completed'
                and expression.right.is_boolean_literal()):
            if expression.right.value:
                return {"completed_date": {"$ne": None}}

            return {"completed_date": None}

        if expression.operator.token_type == Type.LIKE:
            return {expression.left.value: {"$regex": expression.right.value}}

        return {
            expression.left.value: {
                "${}".format(expression.operator.token_type.name.lower()):
                expression.right.value
            }
        }
