"""Contains the List abstract base class as well as error types."""

from abc import ABC, abstractmethod


class InvalidConfigError(Exception):
    """Indicate an invalid configuration was provided to the List."""

    pass


class NotFoundError(Exception):
    """Indicate a task with the given id does not exist."""

    def __init__(self, task_id=None):
        """Return a NotFoundError for id."""
        super().__init__()
        self.task_id = task_id

    def __repr__(self):
        """Return a human friendly error message."""
        if self.task_id:
            return 'no task with id {} exists'.format(self.task_id)
        return 'no task that matched query found'


class List(ABC):
    """An base class that all list implementations must derive from."""

    @abstractmethod
    def search(self, ast):
        """Evaluate the AST and return a List of matching results."""
        raise NotImplementedError

    @abstractmethod
    def add(self, task):
        """Add a task to the List."""
        raise NotImplementedError

    @abstractmethod
    def add_multiple(self, tasks):
        """Add multiple tasks to the List.

        Ideally should be more efficient resource utilization.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self):
        """Return a python list of the Task in this List."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, task_id):
        """Find a task by id."""
        raise NotImplementedError

    @abstractmethod
    def current(self):
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the List.
        """
        raise NotImplementedError

    @abstractmethod
    def complete(self, task_id):
        """Complete a task by id."""
        raise NotImplementedError

    @abstractmethod
    def update(self, task):
        """Update a task in the list.

        The original is retrived using the id of the given task.
        """
        raise NotImplementedError

    @abstractmethod
    def add_note(self, task_id, note):
        """Add note to a task by id."""
        raise NotImplementedError
