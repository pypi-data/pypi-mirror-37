"""
Java-like input scanner.
The scanner breaks the input into tokens, and then converts them to
different types when requested using various next methods.
The following example allows to read a float from stdin:
    # Input:
    # 3 0.5
    sc = Scanner()
    x = sc.next_int()
    y = sc.next_float()
    type(x) is int # True
    type(y) is float # True
    x + y # 3.5
The following code allows to read until EOF and obtain int types:
    # Assume input is:
    # 10 20 30
    # 40 50 60
    sc = Scanner()
    sum = 0
    while sc.has_next():
        sum += sc.next_int()
    sum # 210
The default input stream is sys.stdin. However, it is possible
to read from a file or even a string:
    sc = Scanner(file='data.txt')
    # do stuff
    sc.close()
    # Or
    sc = Scanner(source='some string to use as input')
The scanner can also use string delimeters other than whitespace.
    sc = Scanner(delim=',')
By default, the scanner does a str split. If forced, a regex pattern can also
be used. As expected, the latter method is slower:
    content = '1 fish  2.5 fish red fish  blue fish
    sc = Scanner(source=content, delim='\S*fish\S*', force_regex=True)
    sc.next_int() # 1
    sc.has_next() # True
    sc.next_float() # 2.5
    sc.next() # red
    sc.next() # blue
    sc.has_next() # False
"""

import io
import re
import sys


class Scanner(object):

    def __init__(self, file=None, source=None, delim=None, force_regex=False):
        if file:
            try:
                file = open(file, 'r')
            except (TypeError, FileNotFoundError, FileExistsError) as e:
                raise e("File does not exist")

        elif source:
            file = io.StringIO(source)
        else:
            file = sys.stdin
        if force_regex and not delim:
            raise ValueError('delim must be specified with force_regex')
        self.__file = file
        self.__delim = delim
        self.__force_regex = force_regex
        self.__token = None
        self.__tokens = None

    def has_next(self):
        '''Returns true if there's another token in the input.'''
        return self.__peek() is not None

    def next(self):
        '''Returns the next token in the input as a string.'''
        return self.next_token()

    def next_line(self):
        '''Returns the remaining of the current line as a string.'''
        current = self.next_token()
        rest = self.__delim.join(self.__tokens)
        return current + rest

    def next_int(self):
        '''Returns the next token in the input as an int.'''
        return self.next_type(int)

    def next_float(self):
        '''Returns the next token in the input as a float.'''
        return self.next_type(float)

    def next_type(self, func):
        '''Convert the next token in the input as a given type func.'''
        return func(self.next_token())

    def next_token(self):
        '''Scans and returns the next token that matches the delimeter.'''
        next_token = self.__peek()
        self.__token = None
        return next_token

    def __peek(self):
        '''Internal method. Creates a tokens iterator from the current line,
        and assigns the next token. When the iterator is finished, repeats
        the same process for the next line.'''
        if self.__token:
            return self.__token
        if not self.__tokens:
            line = self.__file.readline()
            if not line:
                return None
            # Use re split if forced, otherwise use str split
            if self.__force_regex:
                splits = re.split(self.__delim, line)
            else:
                splits = line.split(self.__delim)
                if type(splits[0]).__name__ == 'str':
                    for i in range(len(splits)):
                        splits[i] = splits[i].strip()

            self.__tokens = iter(splits)
        try:
            self.__token = next(self.__tokens)
        except StopIteration:
            self.__tokens = None
        # Recurse
        return self.__peek()

    def is_stdin(self):
        '''Returns true if sys.stdin is being used as the input.'''
        return self.__file == sys.stdin

    def close(self):
        '''Closes the scanner, including open files if any.'''
        if not self.is_stdin():
            self.__file.close()
