"""
Usage: task todo [options]

A convenience command for listing tasks which are incomplete.

Options:
    -o <format>, --output <format>  How to display the tasks which match the
                                    query. Available formats are: json, csv,
                                    table, text. See 'task list --help' for
                                    more information on how each format is
                                    displayed. [default: table]

"""

from ..lists import NotFoundError
from ..ql.ast import AST, Expression
from ..ql.tokens import Token
from .query_cmd import print_tasks
from .utils import inject_list


@inject_list
def run(args, task_list=None):
    """Print the current task in task_list."""
    ast = AST(
        Expression(
            Token('='),
            left=Expression(Token('completed')),
            right=Expression(Token('false'))))

    try:
        tasks = task_list.search(ast)
        print_tasks(tasks, output=args['--output'])
    except NotFoundError:
        print('No incomplete tasks!')
