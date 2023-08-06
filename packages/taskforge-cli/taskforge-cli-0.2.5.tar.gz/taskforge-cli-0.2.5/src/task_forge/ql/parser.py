"""Contains the Parser class for the Taskforge Query Language."""

from enum import IntEnum

from .ast import AST, Expression
from .lexer import Lexer
from .tokens import Token, Type


class Precedence(IntEnum):
    """Operator precedence."""

    LOWEST = 0
    STRING = 1
    ANDOR = 2
    COMPARISON = 3


PRECEDENCES = {
    Type.EQ: Precedence.COMPARISON,
    Type.NE: Precedence.COMPARISON,
    Type.GT: Precedence.COMPARISON,
    Type.GTE: Precedence.COMPARISON,
    Type.LT: Precedence.COMPARISON,
    Type.LTE: Precedence.COMPARISON,
    Type.LIKE: Precedence.COMPARISON,
    Type.NLIKE: Precedence.COMPARISON,
    Type.AND: Precedence.ANDOR,
    Type.OR: Precedence.ANDOR,
    Type.STRING: Precedence.STRING,
}


class ParseError(Exception):
    """Raised by the Parser when invalid syntax occurs."""

    pass


class Parser:
    """Parser for the task_forge query language."""

    def __init__(self, query='', lexer=None):
        """
        Create a lexer and parser for query.

        If lexer is not None use that lexer instead of creating one
        for query.
        """
        if lexer is None:
            self.lexer = Lexer(query)
        else:
            self.lexer = lexer

        self.current_token = None
        self.peek_token = None

        self.prefixes = {
            Type.STRING: self._parse_literal,
            Type.NUMBER: self._parse_literal,
            Type.DATE: self._parse_literal,
            Type.BOOLEAN: self._parse_literal,
            Type.LPAREN: self._parse_grouped_expression,
        }

        self.infixes = {
            Type.EQ: self._parse_infix_expression,
            Type.NE: self._parse_infix_expression,
            Type.LT: self._parse_infix_expression,
            Type.GT: self._parse_infix_expression,
            Type.GTE: self._parse_infix_expression,
            Type.LTE: self._parse_infix_expression,
            Type.LIKE: self._parse_infix_expression,
            Type.NLIKE: self._parse_infix_expression,
            Type.OR: self._parse_infix_expression,
            Type.AND: self._parse_infix_expression,
            Type.STRING: self._concat,
        }

        # Populate current and peek token
        next(self)
        next(self)

    def __iter__(self):
        """Return self, an iterator over tokens."""
        return self

    def __next__(self):
        """Get the next token from input."""
        self.current_token = self.peek_token
        try:
            self.peek_token = next(self.lexer)
        except StopIteration:
            self.peek_token = Token('EOF', token_type=Type.EOF)

        if (self.current_token is not None
                and self.current_token.token_type == Type.EOF):
            raise StopIteration

        return self.current_token

    @classmethod
    def from_lexer(cls, lexer):
        """Create a Parser from lexer."""
        return cls(lexer=lexer)

    def set_input(self, query):
        """Change the input of this parser."""
        self.lexer = Lexer(query)

    def parse(self):
        """Parse the query returning an AST. Raises ParseError on failure."""
        return AST(self._parse_expression(Precedence.LOWEST))

    def _parse_expression(self, precedence):
        """Parse an expression."""
        prefix_fun = self.prefixes.get(self.current_token.token_type)
        if prefix_fun is None:
            raise ParseError('no prefix function for: {}'.format(
                self.current_token.token_type))

        expression = prefix_fun()
        while (self.peek_token.token_type != Type.EOF and precedence <
               PRECEDENCES.get(self.peek_token.token_type, Precedence.LOWEST)):
            infix_fun = self.infixes.get(self.peek_token.token_type)
            if infix_fun is None:
                return expression

            next(self)
            expression = infix_fun(expression)

        return expression

    def _parse_infix_expression(self, left):
        """Parse a an infix expression."""
        expression = Expression(self.current_token, left=left)
        if ((expression.operator.token_type == Type.AND
             or expression.operator.token_type == Type.OR)
                and not (expression.left.is_infix()
                         or expression.left.token.token_type == Type.STRING)):
            raise ParseError(
                'left side of a logical expression must be an infix'
                ' expression or string literal got: {}'\
                .format(expression.left.token.token_type))
        elif ((expression.operator.token_type != Type.AND
               and expression.operator.token_type != Type.OR)
              and expression.left.token.token_type != Type.STRING):
            raise ParseError(
                'left side of an infix expression must be a string literal got: {}'\
                .format(expression.left.token.token_type))

        precedence = PRECEDENCES.get(self.current_token.token_type,
                                     Precedence.LOWEST)
        next(self)
        expression.right = self._parse_expression(precedence)
        return expression

    def _concat(self, left):
        """Concatenate multiple unquoted strings into one value."""
        if not (left.is_literal() and isinstance(left.value, str)):
            raise ParseError(
                'can only concat string literals got: {}'.format(left))

        left.token.literal += ' ' + self.current_token.literal
        left.value += ' ' + self.current_token.literal
        return left

    def _parse_literal(self):
        """Return a literal expression from the current token of parser."""
        return Expression(self.current_token)

    def _parse_grouped_expression(self):
        """Return an expression with a the LOWEST precedence."""
        # Skip the (
        next(self)

        expression = self._parse_expression(Precedence.LOWEST)
        if self.peek_token.token_type != Type.RPAREN:
            raise ParseError('unclosed grouped expression @ {}'.format(
                self.lexer.pos))

        # Skip the )
        next(self)
        return expression
