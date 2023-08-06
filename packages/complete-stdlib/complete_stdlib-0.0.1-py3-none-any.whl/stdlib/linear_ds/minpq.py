from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator
from stdlib.abstracts.comparator import Comparator


class MinPQ(Iterable):
    class HeapIterator(Iterator):
        def __init__(self, that):
            self.copy = MinPQ
            self.that = that
            if that.comparator is None:
                self.copy = MinPQ(that.__sizeof__())
            else:
                self.copy = MinPQ(that.__sizeof__(), that.comparator)

        def __has_next__(self) -> bool:
            print(not self.copy.__empty__())
            return not self.copy.__empty__()

        def __remove__(self):
            return NotImplementedError

        def __next__(self) -> object:
            if not self.__has_next__():
                raise StopIteration

            return self.copy.del_min()

    def __init__(self, init_capacity=None, comparator=None, keys=None):
        """

        :param init_capacity:
        :type init_capacity: int
        :param comparator:
        :type comparator: Comparator
        :param keys:
        :type keys:
        """
        self.comparator = comparator
        if init_capacity is not None and comparator is None and keys is None:
            self.pq = list(range(init_capacity + 1))
            self.n = 0
        elif init_capacity is None and comparator is None and keys is None:
            self.pq = list(range(1))
            self.n = 0
        if init_capacity is not None and comparator is not None and keys is None:
            self.pq = list(range(init_capacity + 1))
            self.n = 0
        elif init_capacity is None and comparator is not None and keys is None:
            self.pq = list(range(1))
        if init_capacity is None and comparator is None and keys is not None:
            self.n = len(keys)
            self.pq = list(range(self.n + 1))
            for i in range(self.n):
                self.pq[i + 1] = keys[i]

            k = int(self.n / 2)
            while k >= 1:
                self.__sink(k)
            assert self.__is_min_heap()

    def __empty__(self) -> bool:
        return self.n == 0

    def __sizeof__(self) -> int:
        return self.n

    def min(self) -> object:
        if self.__empty__():
            raise IndexError("Priority queue underflow")
        return self.pq[1]

    def __resize(self, capacity: int):
        assert capacity > self.n
        temp = list(range(capacity))
        for i in range(1, self.n + 1):
            temp[i] = self.pq[i]

        self.pq = temp

    def insert(self, x: object):
        if self.n == len(self.pq) - 1:
            self.__resize(2 * len(self.pq))
        self.n += 1
        self.pq[self.n] = x
        self.__swim(self.n)
        assert self.__is_min_heap()

    def del_min(self) -> object:
        if self.__empty__():
            raise IndexError("Priority Queue underflow")
        _min = self.pq[1]
        self.__exch(1, self.n)
        self.n -= 1
        self.__sink(1)
        self.pq[self.n + 1] = None
        if self.n > 0 and self.n == (len(self.pq) - 1) / 4:
            self.__resize(int(len(self.pq) / 2))

        assert self.__is_min_heap()
        return _min

    def __swim(self, k: int):
        while k > 1 and self.__greater(int(k / 2), k):
            self.__exch(k, int(k / 2))
            k = int(k / 2)

    def __sink(self, k: int):
        while 2 * k <= self.n:
            j = 2 * k
            if j < self.n and self.__greater(j, j + 1):
                j += 1
            if not self.__greater(k, j):
                break
            self.__exch(k, j)
            k = j

    def __greater(self, i: int, j: int) -> bool:
        if self.comparator is None:
            return self.pq[i] > self.pq[j]

        else:
            return self.comparator.compare(self.pq[i], self.pq[j])

    def __exch(self, i: int, j: int):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap

    def __is_min_heap(self) -> bool:
        return self.__is_min_heap_(1)

    def __is_min_heap_(self, k: int) -> bool:
        if k > self.n:
            return True
        left = 2 * k
        right = 2 * k + 1
        if left <= self.n and self.__greater(k, left):
            return False
        if right <= self.n and self.__greater(k, right):
            return False
        return self.__is_min_heap_(left) and self.__is_min_heap_(right)

    def __iter__(self) -> Iterator[object]:
        return self.HeapIterator(that=self)


if __name__ == '__main__':
    comp = Comparator()
    pq = MinPQ()
    a = ['help', 'me', 'please', 'for', 'the', 'love', 'ammon']
    for i in a:
        pq.insert(i)

    for i in pq:
        print(i)

    print(pq.del_min())
