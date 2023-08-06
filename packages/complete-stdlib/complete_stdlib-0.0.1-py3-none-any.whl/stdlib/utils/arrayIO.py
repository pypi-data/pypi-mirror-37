import typing

from stdlib.stdlib.stdin import StdIn


class ArrayIO(object):
    """
    Standard array IO providing functions to read and print 1d and 2d array from a standard input.
    """
    @classmethod
    def read_double_1d(cls) -> typing.List[float]:
        n = StdIn.read_int()
        a = [0.0 for i in range(n)]
        for i in range(n):
            a[i] = StdIn.read_float()

        return a

    @classmethod
    def print_1d(cls, a: typing.List[float]) -> None:
        n = len(a)
        print(n)
        for i in range(n):
            type_of = type(a[i]).__name__
            print('{0:9.5}'.format(a[i]) if type_of == 'float' else '{0}'.format(
                a[i]) if type_of == 'int' else '1' if a[i] else '0')

        print('\n')

    @classmethod
    def read_float_2d(cls) -> typing.List[typing.List[float]]:
        m = StdIn.read_int()
        n = StdIn.read_int()
        a = [[] for i in range(m)]
        for i in range(m):
            a[i] = [0.0 for x in range(n)]

        for i in range(m):
            for j in range(n):
                a[i][j] = StdIn.read_float()

        return a

    @classmethod
    def print_2d(cls, a: typing.List[typing.List[float]]) -> None:
        m = len(a)
        n = len(a[0])
        print('{} {}'.format(m, n))
        for i in range(m):
            for j in range(n):
                type_of = type(a[i][j]).__name__
                print('{0:9.5}'.format(a[i][j]) if type_of == 'float' else '{0}'.format(
                    a[i][j]) if type_of == 'int' else '1' if a[i][j] else '0')

            print()

    @classmethod
    def read_int_1d(cls) -> typing.List[int]:
        n = StdIn.read_int()
        a = [0 for i in range(n)]
        for i in range(n):
            a[i] = StdIn.read_int()

        return a

    @classmethod
    def read_int_2d(cls) -> typing.List[typing.List[int]]:
        m = StdIn.read_int()
        n = StdIn.read_int()
        a = [[] for i in range(m)]
        for i in range(m):
            for j in range(n):
                a[i][j] = StdIn.read_int()

        return a

    @classmethod
    def read_bool_1d(cls) -> typing.List[bool]:
        n = StdIn.read_int()
        a = [False for i in range(n)]
        for i in range(n):
            a[i] = StdIn.read_bool()

        return a

    @classmethod
    def read_bool_2d(cls) -> typing.List[typing.List[bool]]:
        m = StdIn.read_int()
        n = StdIn.read_int()
        a = [[] for i in range(m)]
        for i in range(m):
            for j in range(n):
                a[i][j] = StdIn.read_bool()

        return a


def main():
    pass
