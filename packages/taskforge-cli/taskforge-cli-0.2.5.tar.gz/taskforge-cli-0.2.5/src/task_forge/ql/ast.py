"""AST and Expression classes for the Taskforge query language."""

from datetime import datetime

from .tokens import Type


class AST:
    """Abstract syntax tree for the Taskforge query language."""

    def __init__(self, expression):
        """Build an AST from expression."""
        self.expression = expression

    def __eq__(self, other):
        """Return True if other has the same expression."""
        return self.expression == other.expression

    def __repr__(self):
        """
        Return a string representation of this AST.

        The resulting string is parsable by a Parser.
        """
        return self.expression.__repr__()


class Expression:
    """An expression is a statement that yields a value."""

    date_formats = [
        # Variations of 12 hour clock with AM/PM
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %I:%M%p",
        "%Y-%m-%d %I:%M:%S %p",
        "%Y-%m-%d %I:%M:%S%p",
        # 24 hour formats
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        # Day only
        "%Y-%m-%d",
    ]

    def __init__(self, token, left=None, right=None):
        """
        Build an Expression from token.

        If token is an operator left and right will be used to build
        an infix expression.

        Otherwise a literal will be returned parsing value from
        token.literal.
        """
        self.token = token

        self.value = None
        self.operator = None
        self.left = None
        self.right = None

        if token.token_type == Type.STRING:
            self.value = token.literal
        elif token.token_type == Type.NUMBER:
            self.value = float(token.literal)
        elif token.token_type == Type.BOOLEAN:
            self.value = token.literal.lower() == 'true'
        elif token.token_type == Type.DATE:
            self.value = Expression.parse_date(token.literal)
        else:
            self.operator = token
            self.left = left
            self.right = right

    def __repr__(self):
        """Return a string representation of this expression."""
        if self.is_infix() and self.token.token_type in [Type.AND, Type.OR]:
            return '({} {} {})'.format(self.left, self.operator.literal,
                                       self.right)

        if self.is_infix():
            return '({} {} {})'.format(
                self.left.value if self.left is not None else self.left,
                self.operator.literal, self.right)

        if isinstance(self.value, str):
            return "'{}'".format(self.value)

        return '{}'.format(self.value)

    def __eq__(self, other):
        """Return True if other is the same kind of expression with the same values."""
        if self.is_infix():
            return (other.is_infix() and self.left == other.left
                    and self.operator == other.operator
                    and self.right == other.right)

        return self.value == other.value and self.token == other.token

    @staticmethod
    def parse_date(date_string):
        """Parse a date_string using the first valid format."""
        for date_format in Expression.date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                continue

        raise ValueError('date string did not match any known formats')

    def is_infix(self):
        """Indicate whether this expression is an infix expression."""
        return self.operator is not None

    def is_literal(self):
        """Indicate whether this expression is a literal value."""
        return self.value is not None

    def is_comparison_infix(self):
        """Indicate if this is a value comparison expression."""
        return self.is_infix() and not self.is_logical_infix()

    def is_logical_infix(self):
        """Indicate if this is a logical AND/OR expression."""
        return self.is_and_infix() or self.is_or_infix()

    def is_and_infix(self):
        """Indicate if this is a logical AND expression."""
        return self.is_infix() and self.operator.token_type == Type.AND

    def is_or_infix(self):
        """Indicate if this is a logical OR expression."""
        return self.is_infix() and self.operator.token_type == Type.OR

    def is_str_literal(self):
        """Indicate whether this expression is a string value."""
        return self.is_literal() and self.token.token_type == Type.STRING

    def is_date_literal(self):
        """Indicate whether this expression is a date value."""
        return self.is_literal() and self.token.token_type == Type.DATE

    def is_number_literal(self):
        """Indicate whether this expression is a number value."""
        return self.is_literal() and self.token.token_type == Type.NUMBER

    def is_boolean_literal(self):
        """Indicate whether this expression is a boolean value."""
        return self.is_literal() and self.token.token_type == Type.BOOLEAN
