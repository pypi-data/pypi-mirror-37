"""Contains the Lexer class for tokenizing input for the Taskforge Query Language."""

from .tokens import Token, Type


class Lexer:
    """Scans input producing tokens."""

    def __init__(self, query):
        """Create a lexer for the string query."""
        self.data = query
        self.pos = 0
        self.read_pos = 0
        self.char = ''
        self._read_char()

    def __iter__(self):
        """Return self, for use with for loops."""
        return self

    def __next__(self):  # pylint: disable=too-many-branches
        """Return the next token from input."""
        self._skip_whitespace()

        if self.char == '':
            raise StopIteration
        elif self.char == '^':
            if self._peek_char() == '=':
                self._read_char()
                token = Token('!=')
            elif self._peek_char() == '^':
                self._read_char()
                token = Token('!~')
            else:
                token = Token('~')
        elif self.char == '!':
            literal = self.char
            self._read_char()
            literal += self.char
            token = Token(literal)
        elif self.char == '>' or self.char == '<':
            literal = self.char
            if self._peek_char() == '=':
                self._read_char()
                literal += self.char
            token = Token(literal)
        elif self.char == '"' or self.char == "'":
            # skip the opening quote
            self._read_char()

            token = Token(self._quoted_string())
            if self.char != '"' and self.char != "'":
                token = Token(
                    'unexpected eof: no closing quote',
                    token_type=Type.UNEXPECTED)
        elif self.char == '-':
            # skip the -
            self._read_char()
            token = Token(self._unquoted_string(), token_type=Type.STRING)
        elif self.char.isdigit():
            # numbers can be followed by non space characters and
            # cause lexing errors when followed by a non-space
            # character and therefore do not need the additional read
            # at the bottom of this function since it would "skip" characters
            # like )
            return Token(self._number())
        elif self.char.isalpha():
            # same as above for numbers
            return Token(self._unquoted_string())
        else:
            token = Token(self.char)

        self._read_char()
        return token

    def next_token(self):
        """Return the next token from the input."""
        return self.__next__()

    def _read_char(self):
        """Read a character from input advancing the cursor."""
        if self.read_pos >= len(self.data):
            self.char = ''
        else:
            self.char = self.data[self.read_pos]

        self.pos = self.read_pos
        self.read_pos += 1

    def _peek_char(self):
        """Return the next character."""
        if self.read_pos > len(self.data):
            return ''

        return self.data[self.read_pos]

    def _read(self, valid):
        """
        Read characters in the lexer until valid returns False.

        Returns the full string which matched the valid function.
        """
        start = self.pos
        while valid(self.char):
            self._read_char()

        return self.data[start:self.pos]

    def _skip_whitespace(self):
        while self.char.isspace():
            self._read_char()

    def _unquoted_string(self):
        return self._read(lambda c: c.isalpha())

    def _number(self):
        return self._read(lambda c: c.isdigit() or c == '.')

    def _quoted_string(self):
        return self._read(lambda c: c not in ('"', "'"))
