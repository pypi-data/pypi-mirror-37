"""Contains the Token and Type classes."""

import re
from enum import Enum

DATE_REGEX = re.compile(
    '^[0-9]{4}-[0-9]{2}-[0-9]{2}( [0-9]{2}:[0-9]{2})? ?(AM|PM|pm|am)?')
NUMBER_REGEX = re.compile('^[0-9]{1,}')


class Type(Enum):
    """Represents the various token types."""

    GT = 'GT'
    LT = 'LT'
    GTE = 'GTE'
    LTE = 'LTE'
    EQ = 'EQ'
    NE = 'NE'
    LIKE = 'LIKE'
    NLIKE = 'NLIKE'

    AND = 'AND'
    OR = 'OR'

    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    EOF = 'EOF'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'

    UNEXPECTED = 'UNEXPECTED'


LITERAL_TYPES = {
    "or": Type.OR,
    "OR": Type.OR,
    "and": Type.AND,
    "AND": Type.AND,
    "false": Type.BOOLEAN,
    "False": Type.BOOLEAN,
    "true": Type.BOOLEAN,
    "True": Type.BOOLEAN,
    ">": Type.GT,
    "<": Type.LT,
    ">=": Type.GTE,
    "<=": Type.LTE,
    "=": Type.EQ,
    "!=": Type.NE,
    "^=": Type.NE,
    "^": Type.LIKE,
    "~": Type.LIKE,
    "^^": Type.NLIKE,
    "!~": Type.NLIKE,
    "(": Type.LPAREN,
    ")": Type.RPAREN,
}


class Token:
    """A query language lexical Token."""

    def __init__(self, literal, token_type=None):
        """
        Return a token for literal.

        If token_type is None will be determined from literal.
        """
        self.literal = literal
        if token_type is not None:
            self.token_type = token_type
            return

        if LITERAL_TYPES.get(literal):
            self.token_type = LITERAL_TYPES[literal]
        elif DATE_REGEX.match(literal):
            self.token_type = Type.DATE
        elif NUMBER_REGEX.match(literal):
            self.token_type = Type.NUMBER
        else:
            self.token_type = Type.STRING

    def __repr__(self):
        """Return a string representation of this token."""
        return 'Token({}, {})'.format(self.token_type, self.literal)

    def __eq__(self, other):
        """Return equal if other's literal and token_type are the same."""
        return (self.literal == other.literal
                and self.token_type == other.token_type)
