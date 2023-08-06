"""
Usage: task next [options]

Print the "next" or "current" task. This is calculated by the list as the
highest priority, oldest task in the list.

Default output format is:

$TASK_ID: $TASK_TITLE

You can modify the output with the options below.

Options:
    -i, --id-only     Print only the task ID
    -t, --title-only  Print only the task title
"""

from ..lists import NotFoundError
from .utils import inject_list


@inject_list
def run(args, task_list=None):
    """Print the current task in task_list."""
    try:
        task = task_list.current()
    except NotFoundError:
        print('No current task!')
        return

    if args['--title-only']:
        print(task.title)
    elif args['--id-only']:
        print(task.id)
    else:
        print(f'{task.id}: {task.title}')
