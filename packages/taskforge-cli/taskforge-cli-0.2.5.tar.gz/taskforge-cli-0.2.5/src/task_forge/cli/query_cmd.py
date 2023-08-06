"""
Usage: task query [options] [<query>...]

Search or list tasks in this list.

QUERY will be concatenated using spaces and will be interpreted using the
Taskforge Query Language.

If no query is provided all tasks will be returned.

You can view information about the Taskforge Query Language using 'task help ql'
or by visiting:

http://taskforge.io/docs/query_language

Options:
    -o <format>, --output <format>  How to display the tasks which match the
                                    query. Available formats are: json, csv,
                                    table, text which are described below.
                                    [default: table]

output formats:

   Text output format is the same as for task next where each task will be
   printed on one line with the format:

   $TASK_ID: $TASK_TITLE

   Table output format lists tasks in an ascii table and it looks like this:

   | ID  | Created Date  | Completed Date  | Priority  | Title  | Context  |
   | --- | ------------- | --------------- | --------- | ------ | -------- |
   | $ID | $CREATED_DATE | $COMPLETED_DATE | $PRIORITY | $TITLE | $CONTEXT |

   JSON output format will "pretty print" a JSON array of the tasks in the list
   to stdout.  They will be properly indented 4 spaces and should be fairly
   human readable.  This is useful for migrating from one list implementation
   for another as you can redirect this output to a file then import it with:
   'task add --from-file $YOUR_JSON_FILE'

   CSV will output all task metadata in a csv format. It will write to stdout
   so you can use shell redirection to put it into a csv file like so:

   'task list --output csv > my_tasks.csv'

   This is useful for importing tasks into spreadsheet programs like Excel.
"""

import csv
import json
import sys

from ..lists import NotFoundError
from ..ql.parser import ParseError, Parser
from .utils import inject_list


def print_table(tasks):
    """Print an ASCII table of the tasks."""
    rows = [[
        'ID', 'Created Date', 'Completed Date', 'Priority', 'Title', 'Context'
    ]]
    rows += [[
        task.id,
        str(task.created_date),
        str(task.completed_date),
        str(task.priority), task.title, task.context
    ] for task in tasks]

    # Create a list of the lengths of the longest item in each column.
    # Something like [10, 4, 3, 8]
    column_widths = None
    for row in rows:
        if not column_widths:
            # Get the initial length of our headers
            column_widths = [len(x) for x in row]
        else:
            # Compare the current_width with the width of the data in that
            # column on this row. If the width of the data is larger use that
            # instead of our current width.
            column_widths = [
                max(current_width, len(column_data))
                for current_width, column_data in zip(column_widths, row)
            ]

    # Insert the "separator" row
    rows.insert(1, ['-' * x for x in column_widths])
    for row in rows:
        # ljust will add a number of spaces to the right of data to make it
        # match the width of that column. So if we have the string "a task"
        # which has a length of 6 (i.e. len("a task")) and the widest data for
        # that column is 10 we will end up with "a task    ".
        cols = [data.ljust(width) for width, data in zip(column_widths, row)]
        print("| {} |".format(" | ".join(cols)))


def print_text(tasks):
    """Print the __repr__ of all tasks in the list."""
    for task in tasks:
        print(task)


def print_json(tasks):
    """Print a list of tasks as json to stdout."""
    dicts = [task.to_json() for task in tasks]
    json.dump(dicts, sys.stdout, indent="\t")
    # add a newline to output
    print()


def print_csv(tasks):
    """Print a list of tasks as csv to stdout."""
    writer = csv.DictWriter(
        sys.stdout,
        extrasaction='ignore',
        fieldnames=[
            'id',
            'created_date',
            'completed_date',
            'priority',
            'title',
            'context',
            'body',
        ])

    writer.writeheader()
    for task in tasks:
        writer.writerow(task.to_dict())


def print_tasks(tasks, output='table'):
    """Print tasks using the print function which corresponds to output."""
    if output == 'table':
        print_table(tasks)
    elif output == 'text':
        print_text(tasks)
    elif output == 'json':
        print_json(tasks)
    elif output == 'csv':
        print_csv(tasks)
    else:
        print('{} is not a valid output format. Defaulting to table.'.format(
            output))
        print_table(tasks)


@inject_list
def query_tasks(query, task_list=None):
    """Return tasks which match query or all tasks if query is blank"""
    if query:
        ast = Parser(query).parse()
        return task_list.search(ast)

    return task_list.list()


def run(args):
    """Add the query command to parser."""
    query = ' '.join(args['<query>']) if args['<query>'] else ''
    try:
        tasks = query_tasks(query)
        print_tasks(tasks, output=args['--output'])
    except NotFoundError:
        print('no tasks matched query')
    except ParseError as parse_error:
        print('unable to parse query: {}'.format(parse_error))
        sys.exit(1)
