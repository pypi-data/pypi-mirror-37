class Merge(object):
    def __init__(self):
        pass

    @classmethod
    def sort(cls, a: list):
        """
        Public sort method. Used to sort using Merge sort
        :param a: list to be sorted
        :return: Nothing
        """
        aux = list(range(len(a)))
        cls.__sort(a, aux, 0, len(a) - 1)
        # assert (cls.is_sorted(a) is True)

    @classmethod
    def index_sort(cls, a):
        """
        Returns an indexed sorted array
        :param a: list to be sorted
        :return: Returns an indexed sorted array
        """
        n = len(a)
        index = [i for i in range(n)]
        aux = list(range(n))
        cls.__index_sort(a, index, aux, 0, n - 1)
        return index

    @classmethod
    def is_sorted(cls, a: list):
        return cls.__is_sorted(a, 0, len(a) - 1)

    @staticmethod
    def __index_sort(a: list, index: list, aux: list, lo: int, hi: int):
        if hi <= lo:
            return
        mid = int(lo + (hi - lo) / 2)
        Merge.__index_sort(a, index, aux, lo, mid)
        Merge.__index_sort(a, index, aux, mid + 1, hi)
        Merge.__index_merge(a, index, aux, lo, mid, hi)

    @staticmethod
    def __merge(a: list, aux: list, lo: int, mid: int, hi: int):
        if Merge.__is_sorted(a, lo, mid) or Merge.__is_sorted(a, mid + 1, hi):
            return True

        k = lo
        while k <= hi:
            aux[k] = a[k]
            k += 1

        i, j = lo, mid + 1
        k = lo
        while k <= hi:
            if i > mid:
                a[k] = aux[j]
                j += 1
            elif j > hi:
                a[k] = aux[i]
                i += 1
            elif Merge.__less(aux[j], aux[i]):
                a[k] = aux[j]
                j += 1
            else:
                a[k] = aux[i]
                i += 1
            k += 1

        # assert (Merge._is_sorted(a, lo, hi) is True)

    @staticmethod
    def __index_merge(a: list, index: list, aux: list, lo: int, mid: int, hi: int):
        k = lo
        while k <= hi:
            aux[k] = index[k]
            k += 1
        i, j = lo, mid + 1
        k = lo
        while k <= hi:
            if i > mid:
                index[k] = aux[j]
                j += 1
            elif j > hi:
                index[k] = aux[i]
                i += 1
            elif Merge.__less(a[aux[j]], a[aux[i]]):
                index[k] = aux[j]
                j += 1
            else:
                index[k] = aux[i]
                i += 1

    @staticmethod
    def __sort(a: list, aux: list, lo: int, hi: int):
        if hi <= lo:
            return
        mid = int(lo + (hi - lo) / 2)
        Merge.__sort(a, aux, lo, mid)
        Merge.__sort(a, aux, mid + 1, hi)
        Merge.__merge(a, aux, lo, mid, hi)

    @staticmethod
    def __less(v, w):
        return v < w

    @staticmethod
    def __is_sorted(a: list, lo: int, hi: int):
        i = lo + 1
        while i <= hi:
            if Merge.__less(a[i], a[i - 1]):
                return False

        return True


if __name__ == '__main__':
    string_list = ['jake', 'erin', 'jade', 'karen', 'fred', 'george', 'ammon', 'joseph', 'kim', 'lucy', 'xander',
                   'harry']
    for i in string_list:
        print(i)

    print('\n\n')
    Merge.sort(string_list)

    for i in string_list:
        print(i)
