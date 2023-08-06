from typing import List, Iterable


class InsertionX(object):

    @classmethod
    def sort(cls, a: List[type(Iterable)]):
        n = len(a)
        exchanges = 0
        i = n - 1
        while i > 0:
            if cls.__less(a[i], a[i - 1]):
                cls.__exch(a, i, i - 1)
                exchanges += 1

            i -= 1

        if exchanges == 0:
            return

        for i in range(2, n):
            v = a[i]
            j = i
            while cls.__less(v, a[j - 1]):
                a[j] = a[j - 1]
                j -= 1

            a[j] = v

        assert cls.__is_sorted(a)

    @classmethod
    def reverse_sort(cls, a: List[type(Iterable)]):
        n = len(a)
        exchanges = 0
        i = n - 1
        while i > 0:
            if cls.__less(a[i - 1], a[i]):
                cls.__exch(a, i - 1, i)
                exchanges += 1

            i -= 1

        if exchanges == 0:
            return

        for i in range(2, n):
            v = a[i]
            j = i
            while cls.__less(a[j - 1], v):
                a[j] = a[j - 1]
                j -= 1

            a[j] = v

        assert cls.__is_reverse_sorted(a)

    @classmethod
    def sort_sublist(cls, a: List[type(Iterable)], lo: int, hi: int):
        exchanges = 0
        i = hi - 1
        while i > lo:
            if cls.__less(a[i], a[i - 1]):
                cls.__exch(a, i, i - 1)
                exchanges += 1

            i -= 1

        if exchanges == 0:
            return

        for i in range(2, hi - lo):
            v = a[i + lo]  # == #9
            j = i + lo # == i 7
            while cls.__less(v, a[j - 1]):
                a[j] = a[j - 1]
                j -= 1

            a[j] = v
        assert cls.__is_sorted_(a, lo, hi)

    @classmethod
    def reverse_sort_sublist(cls, a: List[type(Iterable)], lo: int, hi: int):
        exchanges = 0
        i = hi - 1
        while i > lo:
            if cls.__less(a[i - 1], a[i]):
                cls.__exch(a, i - 1, i)
                exchanges += 1

            i -= 1

        if exchanges == 0:
            return

        for i in range(2, hi - lo):
            v = a[i + lo]
            j = i + lo
            while cls.__less(a[j - 1], v):
                a[j] = a[j - 1]
                j -= 1

            a[j] = v

        assert cls.__is_reverse_sorted_(a, lo, hi)

    @classmethod
    def __less(cls, v: object, w: object) -> bool:
        return v < w

    @classmethod
    def __exch(cls, a: List[object], i: int, j: int):
        swap = a[i]
        a[i] = a[j]
        a[j] = swap

    @classmethod
    def __is_sorted(cls, a: List[object]):
        return cls.__is_sorted_(a, 0, len(a))

    @classmethod
    def __is_sorted_(cls, a: List[object], lo: int, hi: int):
        for i in range(lo + 1, hi):
            if cls.__less(a[i], a[i - 1]):
                return False

        return True

    @classmethod
    def __is_reverse_sorted(cls, a: List[type(Iterable)]):
        return cls.__is_reverse_sorted_(a, 0, len(a))

    @classmethod
    def __is_reverse_sorted_(cls, a: List[type(Iterable)], lo: int, hi: int):
        for i in range(lo + 1, hi):
            if cls.__less(a[i - 1], a[i]):
                return False

        return True

    @classmethod
    def show(cls, a: List[Iterable]):
        for i in range(len(a)):
            print(a[i])


if __name__ == '__main__':
    # a = ['danger', 'will', 'robinson', 'you', 'are', 'my', 'only', 'hope', 'am', 'i', 'int']
    # InsertionX.sort(a)
    # InsertionX.show(a)
    #a = ['danger', 'will', 'robinson', 'you', 'are', 'my', 'only', 'hope', 'am', 'i', 'int']
    a = [1, 4, 3, 5, 6, 7, 2, 9, 10, 8]
    InsertionX.reverse_sort(a)
    for i in range(len(a)):
        print(a[i])
