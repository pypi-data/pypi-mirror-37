from typing import List, Iterable

from stdlib.utils.randomwordgenerator import RandomWordGenerator


class MergeX(object):
    CUTOFF = 7

    @classmethod
    def merge(cls, src: List[type(Iterable)], dst: List[type(Iterable)], lo: int, mid: int, hi: int) -> None:
        assert cls.__is_sorted(src, lo, mid)
        assert cls.__is_sorted(src, mid + 1, hi)

        i, j = lo, mid + 1
        k = lo
        while k <= hi:
            if i > mid:
                dst[k] = src[j]
                j += 1
            elif j > hi:
                dst[k] = src[i]
                i += 1
            elif cls.__less(src[j], src[i]):
                dst[k] = src[j]
                j += 1
            else:
                dst[k] = src[i]
                i += 1
            k += 1

        assert cls.__is_sorted(dst, lo, hi)

    @classmethod
    def __sort(cls, src: List[type(Iterable)], dst: List[type(Iterable)], lo: int, hi: int):
        if hi <= lo + cls.CUTOFF:
            # Insertion.sort_sublist(dst, lo, hi)
            cls.insertion_sort(dst, lo, hi)

        mid = int(lo + (hi - lo) / 2)
        cls.__sort(src, dst, lo, mid)
        cls.__sort(src, dst, mid + 1, hi)

        if not cls.__less(src[mid + 1], src[mid]):
            for i in range(lo, hi + 1):
                dst[i] = src[i]

            return

        cls.merge(src, dst, lo, mid, hi)

    @classmethod
    def sort(cls, a: List[type(Iterable)]) -> None:
        aux = list(a)

        cls.__sort(aux, a, 0, len(a) - 1)
        assert cls.is_sorted(a)

    @classmethod
    def insertion_sort(cls, a: List[type(Iterable)], lo: int, hi: int) -> None:
        i = lo
        while i <= hi:
            j = i
            while j > lo and cls.__less(a[j], a[j - 1]):
                print(a, 'before exchange')
                cls.__exch(a, j, j - 1)
                print(a, 'after exchange')
                j -= 1
            i += 1

    @classmethod
    def __exch(cls, a: List[object], i: int, j: int) -> None:
        swap = a[i]
        a[i] = a[j]
        a[j] = swap

    @classmethod
    def __less(cls, v: object, w: object) -> bool:
        return v < w

    @classmethod
    def __is_sorted(cls, a: List[type(Iterable)], lo: int, hi: int):
        for i in range(lo + 1, hi + 1):
            if cls.__less(a[i], a[i - 1]):
                return False

        return True

    @classmethod
    def is_sorted(cls, a: List[type(Iterable)]):
        return cls.__is_sorted(a, 0, len(a) - 1)

    @classmethod
    def show(cls, a: List[type(Iterable)]):
        for i in range(len(a)):
            print(a[i])


def main():
    # a = RandomWordGenerator.generate_word_list(10)
    a = RandomWordGenerator.generate_int_list(int_size=100, rows=10)
    MergeX.sort(a)
    MergeX.is_sorted(a)


if __name__ == '__main__':
    main()
