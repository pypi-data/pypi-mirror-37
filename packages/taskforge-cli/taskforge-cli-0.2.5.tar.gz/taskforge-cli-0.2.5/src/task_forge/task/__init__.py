"""Provides the Task and Note classes used throughout Taskforge."""

from datetime import datetime
from uuid import uuid4

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class Note:
    """
    A note or 'comment' on a task.

    A basic note instantiation only requires the body field. All other fields
    are optional and id should not be set unless instantiating from an existing
    Note.

    :param body: The body of the note.
    :type body: str
    :param id: The unique id for this note. If None this will be generated using
               :func:`uuid.uuid4`. Should only be provided if deserializing an
               existing :class:`Note`.
    :type id: Optional[str].
    :param created_date: The created_date for this note. If None this will be generated using
               :meth:`datetime.datetime.now`. Should only be provided if deserializing an
               existing :class:`Note`.
    :type created_date: Optional[datetime.datetime].
    """

    def __init__(self, body, id=None, created_date=None):
        """Create a note with body."""
        if id is None:
            id = uuid4().hex
        self.id = id
        if created_date is None:
            created_date = datetime.now()
        elif isinstance(created_date, str):
            created_date = datetime.strptime(created_date, DATE_FORMAT)
        self.created_date = created_date
        self.body = body

    def __eq__(self, other):
        """Return True if self and other have the same id."""
        if not isinstance(other, Note):
            return False
        return self.id == other.id

    def __repr__(self):
        """Return a simple string of note id and body."""
        return f'Note({self.id})'

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create a note instance from a dictionary.

        Handles JSON-deserialized types appropriately. i.e. datetime fields will
        be properly parsed if in string form.
        """
        return cls(**dictionary)

    def to_json(self):
        """
        Convert this note object into a dictionary with JSON incompatible types serialized.

        .. note:: For richer data types use :meth:`Note.to_dict` instead.
        """
        dictionary = self.to_dict()
        dictionary['created_date'] = self.created_date.strftime(DATE_FORMAT)
        return dictionary

    def to_dict(self):
        """Convert this note object into a dictionary."""
        return {
            'id': self.id,
            'created_date': self.created_date,
            'body': self.body,
        }


class Task:  # pylint: disable=too-many-instance-attributes
    """
    Represents a task in a Task List.

    This class is the basic unit in Taskforge and is central to all
    functionality.

    The basic instantiation of a Task only requires a title and will fill out
    any required metadata with default values:

    >>> from task_forge.task import Task
    >>> Task('An example Task')
    Task(c659687d9ad54b308a258850a5a06af1)

    All fields available for a task and their defaults are:

    :param title: The title or 'summary' of a task.
    :type title: str
    :param id: The unique id for this task. If None this will be generated using
               :func:`uuid.uuid4`. Should only be provided if deserializing an
               existing :class:`Task`.
    :type id: Optional[str].
    :param created_date: A datetime object representing when this task was
                         created. If not provided defaults to
                         :meth:`datetime.now`. Should only be provided if
                         deserializing an existing :class:`Task`.
    :type created_date: Optional[datetime.datetime]
    :param body: **Default** ("") - The body or 'description' of a task.
    :type body: str
    :param context: **Default** ("default") - The 'list' this task belongs to.
                    Common values are work, personal etc.
    :type context: str
    :param priority: **Default** (1.0) - The priority of this task, this is the
                     primary sorting criteria for tasks.
    :type priority: float
    :param notes: **Default** (None) - A list of Note objects to for this task.
    :type notes: List[Note]
    :param completed_date: **Default** (None) - A datetime object representing
                           when this task was completed.
    :type completed_date: datetime.datetime
    """

    def __init__(  # pylint: disable=too-many-arguments
            self,
            title,
            id=None,
            context='default',
            priority=1.0,
            notes=None,
            created_date=None,
            completed_date=None,
            body='',
    ):
        """
        Create a Task with the given fields, defaulting appropriate metadata.

        All other fields are optional and id should not be set unless
        instantiating from an existing task.
        """
        if id is None:
            id = uuid4().hex
        self.id = id
        self.title = title
        if created_date is None:
            created_date = datetime.now()
        elif isinstance(created_date, str):
            created_date = datetime.strptime(created_date, DATE_FORMAT)
        self.created_date = created_date
        self.context = context
        self.priority = priority
        if isinstance(completed_date, str):
            completed_date = datetime.strptime(completed_date, DATE_FORMAT)
        self.completed_date = completed_date
        if notes is None:
            notes = []
        self.notes = notes
        self.body = body

    def __eq__(self, other):
        """Return True if self and other have the same id."""
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __lt__(self, other):
        """Sorts highest priority first then oldest first."""
        if self.priority > other.priority:
            return True

        if self.priority < other.priority:
            return False

        return self.created_date < other.created_date

    def __repr__(self):
        """Return a simple string of the task id and title."""
        return f'Task({self.id})'

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create a Task from a dictionary representation.

        Handles JSON-deserialized types appropriately. i.e. datetime fields will
        be properly parsed if in string form.
        """
        if dictionary.get('notes'):
            dictionary['notes'] = [
                Note.from_dict(note) for note in dictionary['notes']
            ]
        else:
            dictionary['notes'] = []

        return cls(**dictionary)

    def to_json(self):
        """
        Convert to a dictionary which has JSON incompatible types properly serialized.

        .. note:: For richer data types use :meth:`Task.to_dict` instead.
        """
        dictionary = self.to_dict()
        dictionary['notes'] = [n.to_json() for n in self.notes]
        dictionary['created_date'] = self.created_date.strftime(DATE_FORMAT)
        if self.completed_date:
            dictionary['completed_date'] = self.completed_date.strftime(
                DATE_FORMAT)
        return dictionary

    def to_dict(self):
        """Convert this task object into a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'context': self.context,
            'priority': self.priority,
            'created_date': self.created_date,
            'completed_date': self.completed_date,
            'notes': [n.to_dict() for n in self.notes],
        }

    def complete(self):
        """
        Complete this task.

        Sets self.completed_date using :meth:`datetime.datetime.now`.
        """
        self.completed_date = datetime.now()
        return self

    def is_complete(self):
        """Indicate whether this task is completed or not."""
        return self.is_completed()

    def is_completed(self):
        """Indicate whether this task is completed or not."""
        return self.completed_date is not None
