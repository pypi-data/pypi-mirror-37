from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator


class IndexMinPQ(Iterable):
    def __init__(self, max_n: int):
        if max_n < 0:
            raise ValueError

        self.max_n = max_n
        self.n = 0
        self.keys = [] * max_n + 1
        self.pq = [0 for i in range(max_n + 1)]
        self.qp = [-1 for i in range(max_n + 1)]

    def __empty__(self) -> bool:
        return self.n == 0

    def __contains__(self, item: int) -> bool:
        if item < 0 or item >= self.max_n:
            raise ValueError()

        return self.qp[item] != -1

    def __sizeof__(self):
        return self.n

    def insert(self, i: int, key) -> None:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if self.__contains__(i):
            raise ValueError("Index is already in the priority queue")

        self.n += 1
        self.qp[i] = self.n
        self.pq[self.n] = i
        self.keys[i] = key
        self.__swim(self.n)

    def min_index(self) -> int:
        if self.n == 0:
            raise IndexError("Priority queue underflow")

        return self.pq[1]

    def min_key(self) -> object:
        if self.n == 0:
            raise IndexError("Priority queue underflow")

        return self.keys[self.pq[1]]

    def del_min(self) -> int:
        if self.n == 0:
            raise IndexError("Priority queue underflow")

        min = self.pq[1]
        self.__exch(1, self.n)
        self.n -= 1
        self.__sink(1)
        assert min == self.pq[self.n + 1]
        self.qp[min] = -1
        self.keys[min] = None
        self.pq[self.n + 1] = -1
        return min

    def key_of(self, i: int) -> object:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if not self.__contains__(i):
            raise IndexError("Index is not in the priority queue")

        else:
            return self.keys[i]

    def change_key(self, i: int, key: object) -> None:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if not self.__contains__(i):
            raise IndexError("Index is not in the priority queue")

        self.keys[i] = key
        self.__swim(self.qp[i])
        self.__sink(self.qp[i])

    def decrease_key(self, i: int, key: object) -> None:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if not self.__contains__(i):
            raise IndexError("Index is not in the priority queue")

        if self.keys[i] <= key:
            raise ValueError("Calling decrease_ke() with given argument would not strictly decrease the key")

        self.keys[i] = key
        self.__swim(self.qp[i])

    def increase_key(self, i: int, key: object) -> None:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if not self.__contains__(i):
            raise IndexError("Index is not in the priority queue")

        if self.keys[i] >= key:
            raise ValueError("Calling increase_ke() with given argument would not strictly increase the key")

        self.keys[i] = key
        self.__sink(self.qp[i])

    def delete(self, i: int) -> None:
        if i < 0 or i >= self.max_n:
            raise ValueError

        if not self.__contains__(i):
            raise IndexError("Index is not in the priority queue")

        index = self.qp[i]
        self.__exch(index, self.n)
        self.n -= 1
        self.__swim(index)
        self.__sink(index)
        self.keys[i] = None
        self.qp[i] = -1

    def __greater(self, i: int, j: int) -> bool:
        return self.keys[self.pq[i]] > self.keys[self.pq[j]]

    def __exch(self, i: int, j: int) -> None:
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def __swim(self, k: int) -> None:
        while k > 1 and self.__greater(int(k / 2), k):
            self.__exch(k, int(k / 2))
            k = int(k / 2)

    def __sink(self, k: int) -> None:
        while 2 * k <= self.n:
            j = 2 * k
            if j < self.n and self.__greater(j, j + 1):
                j += 1

            if not self.__greater(k, j):
                break

            self.__exch(k, j)
            k = j

    def __iter__(self):
        return HeapIterator(self)


class HeapIterator(Iterator):
    def __init__(self, outer: IndexMinPQ):
        self.copy = IndexMinPQ(len(outer.pq) - 1)
        for i in range(1, outer.n + 1):
            self.copy.insert(outer.pq[i], outer.keys[outer.pq[i]])

    def __has_next__(self) -> bool:
        return not self.copy.__empty__()

    def __next__(self):
        if not self.__has_next__():
            raise StopIteration

        return self.copy.del_min()

    def __remove__(self):
        raise NotImplementedError


def main():
    strings = ["it", "was", "the", "best", "of", "times", "it", "was", "the", "worst"]

    pq = IndexMinPQ(len(strings))
    for i in range(len(strings)):
        pq.insert(i, strings[i])

    while not pq.__empty__():
        i = pq.del_min()
        print("{} {}".format(i, strings[i]))

    print()

    for i in range(len(strings)):
        pq.insert(i, strings[i])

    for i in pq:
        print("{} {}".format(i, strings[i]))

    while not pq.__empty__():
        pq.del_min()


if __name__ == '__main__':
    main()
