class Heap:
    """
    Heap sort that array!
    """
    @classmethod
    def sort(cls, pq: list):
        n = len(pq)
        k = int(n / 2)
        while k >= 1:
            cls.__sink(pq, k, n)
            k -= 1

        while n > 1:
            cls.__exch(pq, 1, n)
            n -= 1
            cls.__sink(pq, 1, n)

    @staticmethod
    def __sink(pq: list, k: int, n: int):
        while 2 * k <= n:
            j = 2 * k
            if j < n and Heap.__less(pq, j, j + 1):
                j += 1
            if not Heap.__less(pq, k, j):
                break
            Heap.__exch(pq, k, j)
            k = j

    @staticmethod
    def __less(pq: list, i: int, j: int) -> bool:
        return pq[i - 1] < pq[j - 1]

    @staticmethod
    def __exch(pq: list, i: int, j: int):
        swap = pq[i - 1]
        pq[i - 1] = pq[j - 1]
        pq[j - 1] = swap

    @classmethod
    def show(cls, a: list):
        for i in range(len(a)):
            print(a[i])


if __name__ == '__main__':
    a = [3, 2, 5, 4, 7, 6, 1, 2, 5, 4, 2, 10]
    Heap.sort(a)
    Heap.show(a)
