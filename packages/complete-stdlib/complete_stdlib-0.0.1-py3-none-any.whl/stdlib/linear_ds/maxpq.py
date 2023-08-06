import typing

from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator
from stdlib.abstracts.comparator import Comparator


class MaxPQ(Iterable):
    class HeapIterator(Iterator):
        def __init__(self, comparator: Comparator, maxpq):
            if comparator is None:
                self.copy = maxpq(maxpq.__sizeof__())

            else:
                self.copy = maxpq(maxpq.__sizeof__(), comparator)

            for i in range(1, maxpq.n + 1):
                self.copy.insert(maxpq.pq[i])

        def __has_next__(self) -> bool:
            return not self.copy.__empty__()

        def __next__(self):
            if not self.__has_next__():
                raise StopIteration

            return self.copy.del_max()

        def __remove__(self):
            raise NotImplementedError()

    def __init__(self, init_capacity: int = None, comparator: Comparator = None,
                 keys: typing.List[typing.Generic] = None):
        if keys:
            self.n = len(keys)
            self.pq = []
            for i in range(self.n):
                self.pq[i + 1] = keys[i]

            k = self.n / 2
            while k >= 1:
                self.__sink(k)
                k -= 1

            assert self.__is_max_heap()

        else:
            self.pq = [typing.Generic for i in range((init_capacity if init_capacity else 1) + 1)]
            self.n = 0
            if comparator:
                self.comparator = comparator

    def __iter__(self):
        return self.HeapIterator(self.comparator, self)

    def __empty__(self):
        return self.n == 0

    def __sizeof__(self):
        return self.n

    def max(self):
        if self.__empty__():
            raise IndexError("Priority queue underflow")

        return self.pq[1]

    def resize(self, capacity: int) -> None:
        assert capacity > self.n
        temp = [typing.Generic for i in range(capacity)]
        for i in range(1, self.n + 1):
            temp[i] = self.pq[i]

        self.pq = temp

    def insert(self, x) -> None:
        if self.n == len(self.pq) - 1:
            self.resize(2 * len(self.pq))

        self.n += 1
        self.pq[self.n] = x
        self.__swim(self.n)
        # assert self.__is_max_heap()

    def del_max(self):
        if self.__empty__():
            raise IndexError("Priority queue underflow")

        max = self.pq[1]
        self.__exch(1, self.n)
        self.n -= 1
        self.__sink(1)
        self.pq[self.n + 1] = None
        if self.n > 0 and self.n == len(self.pq) - 1 / 4:
            self.resize(int(len(self.pq) / 2))

        assert self.__is_max_heap()
        return max

    def __sink(self, k: int):
        while 2 * k <= self.n:
            j = 2 * k
            if j < self.n and self.__less(j, j + 1):
                j += 1

            if not self.__less(k, j):
                break

            self.__exch(k, j)
            k = j

    def __swim(self, k: int):
        while k > 1 and self.__less(k / 2, k):
            self.__exch(k, k / 2)
            k = k / 2

    def __less(self, i: int, j: int) -> bool:
        if self.comparator is None:
            return self.pq[i] < self.pq[j]

        else:
            return self.comparator.compare(self.pq[i], self.pq[j]) < 0

    def __exch(self, i: int, j: int):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap

    def __is_max_heap(self) -> bool:
        return self._is_max_heap(1)

    def _is_max_heap(self, k: int) -> bool:
        if k > self.n:
            return True

        left = 2 * k
        right = 2 * k + 1
        if left <= self.n and self.__less(k, left):
            return False
        if right <= self.n and self.__less(k, right):
            return False


def main():
    pq = MaxPQ()
    pq.insert('hello')
    pq.insert('sailor')
    pq.insert('jerry')

    while not pq.__empty__():
        print(pq.del_max())


if __name__ == '__main__':
    main()
