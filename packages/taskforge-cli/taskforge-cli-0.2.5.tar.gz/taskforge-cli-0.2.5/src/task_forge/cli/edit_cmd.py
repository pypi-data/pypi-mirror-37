"""
Usage: task edit [<ID>]

Edit the task indicated by ID as a toml file. If no ID given opens the current
task.

Will use $EDITOR if set and if not will attempt to find an editor based on
platform.
"""

import sys
import os
import shlex

from tempfile import NamedTemporaryFile
from subprocess import call

import toml

from task_forge.task import Task
from task_forge.lists import NotFoundError
from task_forge.cli.utils import inject_list


def get_editor_program():
    """Return editor based on operating system"""
    if sys.platform == 'win32':
        if 'EDITOR' in os.environ:
            return os.getenv('EDITOR')

        return 'notepad.exe'

    return os.getenv('EDITOR', 'vi')


def editor(filename):
    """Open filename in $EDITOR"""
    program = get_editor_program()
    args = '{} {}'.format(program, filename)
    call(shlex.split(args),
         stdin=sys.stdin,
         stdout=sys.stdout,
         stderr=sys.stderr)


@inject_list
def run(args, task_list=None):
    """Open task by ID in $EDITOR. Update task based on result."""
    try:
        if args['<ID>']:
            task = task_list.find_by_id(args['<ID>'])
        else:
            task = task_list.current()

        tmp = NamedTemporaryFile(mode='w+', suffix='.toml', delete=False)
        toml.dump(task.to_dict(), tmp)
        tmp.close()

        editor(tmp.name)

        with open(tmp.name) as tmp:
            new_task = Task.from_dict(toml.load(tmp))

        task_list.update(new_task)
        os.remove(tmp.name)
    except NotFoundError:
        print('no task with that ID exists')
        sys.exit(1)
