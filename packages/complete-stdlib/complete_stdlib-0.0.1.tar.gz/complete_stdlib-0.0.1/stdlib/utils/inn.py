import sys
from typing import List
import requests
from stdlib.utils.scanner import Scanner


class In(object):
    def __init__(self, file: str = None, url: str = None):
        try:
            self.arg = sys.argv[1]
        except IndexError as e:
            self.arg = None

        self.file = file
        self.url = url
        self.__scanner = None
        self.__in()

    def __in(self):
        if self.arg is not None and self.file is None and self.url is None:
            return self.__arg()
        elif self.arg is None and self.file is not None and self.url is None:
            return self.__file()
        elif self.arg is None and self.file is None and self.url is not None:
            return self.__url()

    def __arg(self):
        pass

    def __file(self):
        try:
            self.__scanner = Scanner(file=self.file, delim=' ')
        except (FileExistsError, FileNotFoundError, TypeError) as e:
            raise e("File does not exist")

    def __url(self):
        response = requests.get(url=self.url)
        return response.content

    def has_next_line(self) -> bool:
        return self.__scanner.has_next()

    def exists(self):
        return self.__scanner is None

    def __empty__(self):
        return not self.__scanner.has_next()

    def read_line(self) -> str:
        try:
            line = self.__scanner.next_line()
        except IndexError:
            line = None

        return line

    def read_all(self) -> str:
        if not self.__scanner.has_next():
            return ""

        result = ''
        while self.__scanner.has_next():
            result += self.__scanner.next() + ' '

        return result

    def read_string(self) -> str:
        try:
            return self.__scanner.next()
        except IndexError:
            raise IndexError("attempts to read a string value from standard input, but there are not more tokens "
                             "available")

    def read_int(self) -> int:
        try:
            token = self.__scanner.next_int()
            # print("next token {0}".format(token))
            return token
        except ValueError as e:
            token = self.__scanner.next()
            raise ValueError("attempts to read an 'int' value from standard input, but the next token "
                             "is '{}'".format(token))
        except IndexError as e:
            raise IndexError("attemps to read an 'int' value from standard input, but there are no more "
                             "tokens available")

    def read_float(self) -> float:
        try:
            return self.__scanner.next_float()
        except ValueError:
            token = self.__scanner.next()
            raise ValueError("attempts to read an 'float' value from standard input, but the next token "
                             "is '{}'".format(token))
        except IndexError:
            raise IndexError("attemps to read an 'float' value from standard input, but there are no more "
                             "tokens available")

    def read_bool(self) -> bool:
        try:
            token = self.read_string()
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

    def read_all_strings(self) -> List[str]:
        tokens = self.read_all().split(' ')
        if len(tokens) == 0 or len(tokens[0]) > 0:
            return tokens

        decapitokens = []
        for i in range(len(tokens) - 1):
            decapitokens[i] = tokens[i + 1]

        return decapitokens

    def read_all_lines(self) -> List[str]:
        lines = []
        while self.has_next_line():
            lines.append(self.read_line())

        return lines

    def read_all_ints(self) -> List[int]:
        fields = self.read_all_strings()
        vals = []
        for i in range(len(fields)):
            vals.append(int(fields[i]))

        return vals

    def read_all_floats(self) -> List[float]:
        fields = self.read_all_strings()
        vals = []
        for i in range(len(fields)):
            vals.append(float(fields[i]))

        return vals


def main():
    print()
