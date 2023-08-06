"""
Usage: task complete [<ID>...]

Complete tasks by ID. If no IDs are provided then the current task indicated by
'task next' is completed.
"""

import sys

from ..lists import NotFoundError
from .utils import inject_list


@inject_list
def complete_tasks(tasks, task_list=None):
    """
    Complete tasks by the ids in tasks.

    If no tasks are provided then complete the current task.
    """
    try:
        current = task_list.current()
        tasks = [current.id]
    except NotFoundError:
        print('no ID given and no current task found')
        sys.exit(0)

    for task in tasks:
        task_list.complete(task)


def run(args):
    """Add the next command to parser."""
    tasks = args['<ID>']
    complete_tasks(tasks)
