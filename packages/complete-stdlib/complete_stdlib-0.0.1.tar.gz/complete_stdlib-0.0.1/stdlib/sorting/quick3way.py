import random

from stdlib.utils.randomwordgenerator import RandomWordGenerator


class QuickSort3Way(object):
    def __init__(self):
        pass

    @classmethod
    def sort(cls, a):
        random.shuffle(a)
        cls._sort(a, 0, len(a) - 1)
        assert (cls.is_sorted(a) is True)

    @staticmethod
    def _less(v, w):
        return v < w

    @staticmethod
    def _exch(a: list, i: int, j: int):
        swap = a[i]
        a[i] = a[j]
        a[j] = swap

    @staticmethod
    def _sort(a: list, lo: int, hi: int):
        if hi <= lo:
            return
        lt, gt = lo, hi
        v = a[lo]
        i = lo + 1
        while i <= gt:
            if a[i] < v:
                QuickSort3Way._exch(a, lt, i)
                lt += 1
                i += 1
            elif a[i] > v:
                QuickSort3Way._exch(a, i, gt)
                gt -= 1
            else:
                i += 1

        QuickSort3Way._sort(a, lo, lt - 1)
        QuickSort3Way._sort(a, gt + 1, hi)

    @classmethod
    def is_sorted(cls, a: list):
        return QuickSort3Way._is_sorted(a, 0, len(a) - 1)

    @staticmethod
    def _is_sorted(a: list, lo: int, hi: int):
        i = lo + 1
        while i <= hi:
            if QuickSort3Way._less(a[i], a[i - 1]):
                return False
            i += 1
        return True


if __name__ == '__main__':
    a = RandomWordGenerator.generate_word_list(15)
    QuickSort3Way.sort(a)
    print(QuickSort3Way.is_sorted(a))
    # import sys
    #
    # string_list = []
    # arg1 = None
    # try:
    #     arg1 = sys.argv[1]
    # except IndexError:
    #     arg1 = None
    #
    # if arg1 is not None:
    #     with open(sys.argv[1], 'r') as f:
    #         for i in f.read().split('\n'):
    #             string_list.append(i)
    # else:
    #     string_list = ['jake', 'erin', 'jade', 'karen', 'fred', 'george', 'ammon', 'joseph', 'kim', 'lucy', 'xander',
    #                    'harry']
    #
    # for i in string_list:
    #     print(i)
    #
    # print('\n\n')
    # QuickSort3Way.sort(string_list)
    #
    # for i in string_list:
    #     print(i)
    #
    # if 'erin' > 'ammon':
    #     print('erin is greater than ammon')
