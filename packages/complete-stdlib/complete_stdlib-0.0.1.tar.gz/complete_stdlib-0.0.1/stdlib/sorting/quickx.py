import random
from typing import List, Iterable

from stdlib.sorting.insertionx import InsertionX


class QuickX(object):
    INSERTION_SORT_CUTOFF = 8

    @classmethod
    def sort(cls, a: List[type(Iterable)]):
        # random.shuffle(a)
        cls.__sort(a, 0, len(a) - 1)
        # assert cls.__is_sorted(a)

    @classmethod
    def reverse_sort(cls, a: List[type(Iterable)]):
        # random.shuffle(a)
        cls.__reverse_sort(a, 0, len(a) - 1)
        assert cls.__is_reverse_sorted(a)

    @classmethod
    def __sort(cls, a: List[object], lo: int, hi: int):
        if hi <= lo:
            return

        # cutoff to insertion sort (Insertion.sort() uses half-open intervals
        n = hi - lo + 1
        if n <= cls.INSERTION_SORT_CUTOFF:
            # print(a, 'before insertion', 'lo = ', lo, 'hi', hi + 1)
            InsertionX.sort_sublist(a, lo, hi + 1)
            # print(a, 'after insertion', 'lo = ', lo, 'hi', hi + 1)
            # print('\n')
            return

        j = cls.__partition(a, lo, hi)
        cls.__sort(a, lo, j - 1)
        cls.__sort(a, j + 1, hi)

    @classmethod
    def __partition(cls, a: List[type(Iterable)], lo: int, hi: int) -> int:
        n = hi - lo + 1
        m = cls.__median(a, lo, int(lo + (n / 2)), hi)
        cls.__exch(a, m, lo)

        i = lo + 1
        j = hi
        v = a[lo]

        while cls.__less(a[i], v):
            i += 1
            if i == len(a):
                i -= 1
                if cls.__less(a[i - 1], a[i]):
                    cls.__exch(a, i, i - 1)

            if i == hi:
                cls.__exch(a, lo, hi)
                return hi

        while cls.__less(v, a[j]):
            j -= 1
            if j == lo + 1:
                return lo

        while i < j:
            cls.__exch(a, i, j)
            while cls.__less(a[i], v):
                i += 1

            while cls.__less(v, a[j]):
                j -= 1

        cls.__exch(a, lo, j)
        return j

    @classmethod
    def __reverse_sort(cls, a: List[object], lo: int, hi: int):
        if lo >= hi:
            return

        # cutoff to insertion sort (Insertion.sort() uses half-open intervals)
        n = hi - lo + 1  # 8 - 0 + 1 = 9
        if n <= cls.INSERTION_SORT_CUTOFF:
            InsertionX.reverse_sort_sublist(a, lo, hi + 1)
            return

        j = cls.__reverse_partition(a, lo, hi)
        cls.__reverse_sort(a, lo, j - 1)
        cls.__reverse_sort(a, j + 1, hi)

    @classmethod
    def __reverse_partition(cls, a: List[type(Iterable)], lo: int, hi: int) -> int:
        n = hi - lo + 1
        m = cls.__median(a, lo, int(lo + (n / 2)), hi)
        cls.__exch(a, m, lo)

        v = a[lo]
        i = lo + 1
        j = hi

        try:
            while cls.__less(v, a[i]):
                i += 1
                if i == len(a):
                    i -= 1
                    if cls.__less(a[i - 1], a[i]):
                        cls.__exch(a, i - 1, i)

                if i == hi:
                    return hi

        except IndexError as e:
            print("i = {}. List __sizeof__ is {}. Line 118 in my code. Hi = {}. v = {}.".format(i, len(a), hi, v))

        try:
            while cls.__less(a[j], v):
                j -= 1
                if j == lo + 1:
                    return lo
        except IndexError as e:
            print("j = {}. List __sizeof__ is {}. Line 113 in my code. lo = {}".format(j, len(a), lo))

        while i < j:
            cls.__exch(a, i, j)
            while cls.__less(v, a[i]):
                i += 1

            while cls.__less(a[j], v):
                j -= 1

        cls.__exch(a, lo, j)
        return j

    @classmethod
    def __median(cls, a: List[type(Iterable)], i: int, j: int, k: int) -> int:
        return (j if cls.__less(a[j], a[k]) else k if cls.__less(a[i], a[k]) else i) if cls.__less(a[i], a[j]) else \
            (j if cls.__less(a[k], a[j]) else k if cls.__less(a[k], a[i]) else i)

    @classmethod
    def __less(cls, v: object, w: object):
        return v < w

    @classmethod
    def __exch(cls, a: List[type(Iterable)], i: int, j: int):
        swap = a[i]
        a[i] = a[j]
        a[j] = swap

    @classmethod
    def __is_sorted(cls, a: List[type(Iterable)]):
        for i in range(1, len(a)):
            if cls.__less(a[i], a[i - 1]):
                # print(i, len(a))
                # print(a[i], a[i - 1])
                return False

        return True

    @classmethod
    def __is_reverse_sorted(cls, a: List[type(Iterable)]):
        for i in range(1, len(a)):
            if cls.__less(a[i - 1], a[i]):
                return False

        return True

    @classmethod
    def show(cls, a: List[type(Iterable)], ascending_order=True):
        for i in range(len(a)):
            print(a[i])

        if ascending_order:
            assert cls.__is_sorted(a)
        else:
            assert cls.__is_reverse_sorted(a)


def main():
    # a_rev = RandomWordGenerator.generate_int_list(100, 1000)
    # for i in range(1000):
    #     a_rev = RandomWordGenerator.generate_int_list(100, 1000)
    #     QuickX.reverse_sort(a_rev)
    #
    # QuickX.show(a_rev, ascending_order=False)
    # print('\n\n')
    b = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    print(b)
    random.shuffle(b)
    QuickX.reverse_sort(b)
    print(b)
    # QuickX.show(b)

    # b = RandomWordGenerator.generate_int_list(100000, 100000)
    # start = time.clock()
    # QuickX.sort(b)
    # end = time.clock()
    # print("Total time ", end - start / 10000)
    # QuickX.show(b)


if __name__ == '__main__':
    main()
