from stdlib.abstracts.iterable import Iterable
from stdlib.sorting.quickx import QuickX
from stdlib.linear_ds.queue import Queue
from typing import List


class Collections(object):
    @classmethod
    def reverse(cls, a: (List[type(Iterable)], str)):
        for i in range(0, int(len(a) / 2)):
            temp = a[i]
            a[i] = a[len(a) - i - 1]
            a[len(a) - i - 1] = temp

    @classmethod
    def sort(cls, a: (List[type(Iterable)], str)):
        QuickX.sort(a)

    @classmethod
    def reverse_sort(cls, a: (List[type(Iterable)], str)):
        QuickX.reverse_sort(a)

    @classmethod
    def queue(cls):
        return Queue()

    @classmethod
    def binary_search(cls, a: (List[int], List[str]), key: (int, str), to_lower: bool = False) -> int:
        try:
            assert cls.__is_binary_sorted(a)
        except AssertionError:
            print("List is not sorted. Please sort the list first and then search")
            return -1
        lo = 0
        hi = len(a) - 1
        if to_lower:
            key = key.lower()
        while lo <= hi:
            mid = int(lo + (hi - lo) / 2)
            if key < (a[mid].lower() if to_lower else a[mid]):
                hi = mid - 1
            elif key > (a[mid].lower() if to_lower else a[mid]):
                lo = mid + 1
            else:
                return mid

        return -1

    @classmethod
    def __is_binary_sorted(cls, a: List[type(Iterable)]):
        for i in range(1, len(a)):
            if a[i] < a[i - 1]:
                return False

        return True

    @classmethod
    def swap(cls, a: List[type(Iterable)], i: int, j: int):
        swap = a[i]
        a[i] = a[j]
        a[j] = swap

    @classmethod
    def fill(cls, a: List[type(Iterable)], obj: type(object)):
        for i in range(len(a)):
            a[i] = obj


if __name__ == '__main__':
    a = ['help', 'me', 'please', 'sir', 'no', 'dont', 'i', 'am', 'ok']

    # Collections.shuffle(a)
    print(a)
    print(Collections.binary_search(a, 'Please'))
    Collections.sort(a)
    print(a)
    print(Collections.binary_search(a, 'NO', True))

