from typing import List

from stdlib.utils.scanner import Scanner


class StdIn(object):
    CHARSET_NAME = "UTF-8"
    LOCALE = "US"
    WHITESPACE_PATTERN = " "
    EMTPY_PATTERN = ""
    EVERYTHING_PATTERN = "\\A"

    scanner = Scanner()

    @classmethod
    def is_empty(cls) -> bool:
        return not cls.scanner.has_next()

    @classmethod
    def has_next_line(cls) -> bool:
        return cls.scanner.has_next()

    @classmethod
    def read_line(cls) -> str:
        try:
            line = cls.scanner.next_line()
        except IndexError:
            line = None

        return line

    @classmethod
    def read_all(cls) -> str:
        if not cls.scanner.has_next():
            return ""

        result = ''
        while cls.scanner.has_next():
            result += cls.scanner.next() + ' '

        return result

    @classmethod
    def read_string(cls) -> str:
        try:
            return cls.scanner.next()
        except IndexError:
            raise IndexError("attempts to read a string value from standard input, but there are not more tokens "
                             "available")

    @classmethod
    def read_int(cls) -> int:
        try:
            return cls.scanner.next_int()
        except ValueError as e:
            token = cls.scanner.next()
            raise ValueError("attempts to read an 'int' value from standard input, but the next token "
                             "is '{}'".format(token))
        except IndexError as e:
            raise IndexError("attemps to read an 'int' value from standard input, but there are no more "
                             "tokens available")

    @classmethod
    def read_float(cls) -> float:
        try:
            return cls.scanner.next_float()
        except ValueError:
            token = cls.scanner.next()
            raise ValueError("attempts to read an 'float' value from standard input, but the next token "
                             "is '{}'".format(token))
        except IndexError:
            raise IndexError("attemps to read an 'float' value from standard input, but there are no more "
                             "tokens available")

    @classmethod
    def read_bool(cls) -> bool:
        try:
            token = cls.read_string()
            if token.lower() == 'true':
                return True
            if token.lower() == 'false':
                return False
            if token == 1:
                return True
            if token == 0:
                return False
            raise ValueError("attempts to read in a bool value from std input but the next toekn is is \"" + token +
                             "\"")
        except IndexError as e:
            raise IndexError("attempts to read a 'boolean' value from standard input, but there are no more tokens "
                             "available")

    @classmethod
    def read_all_strings(cls) -> List[str]:
        tokens = cls.read_all().split(' ')
        if len(tokens) == 0 or len(tokens[0]) > 0:
            return tokens

        decapitokens = []
        for i in range(len(tokens) - 1):
            decapitokens[i] = tokens[i + 1]

        return decapitokens

    @classmethod
    def read_all_lines(cls) -> List[str]:
        lines = []
        while cls.has_next_line():
            lines.append(cls.read_line())

        return lines

    @classmethod
    def read_all_ints(cls) -> List[int]:
        fields = cls.read_all_strings()
        vals = []
        for i in range(len(fields)):
            vals.append(int(fields[i]))

        return vals

    @classmethod
    def read_all_floats(cls) -> List[float]:
        fields = cls.read_all_strings()
        vals = []
        for i in range(len(fields)):
            vals.append(float(fields[i]))

        return vals
