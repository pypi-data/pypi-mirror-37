import math
from typing import List


class Stats(object):

    @classmethod
    def max(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> (float, int):
        cls.__validate_not_none(a)

        max_val = float("-inf")
        if lo and hi:
            for i in range(lo, hi):
                if math.isnan(a[i]):
                    return math.nan
                if a[i] > max_val:
                    max_val = a[i]

            return max_val
        else:
            for i in range(len(a)):
                if math.isnan(a[i]):
                    return math.nan
                if a[i] > max_val:
                    max_val = a[i]

            return max_val

    @classmethod
    def min(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> (float, int):
        cls.__validate_not_none(a)
        min_val = float("inf")

        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            for i in range(lo, hi):
                if math.isnan(a[i]):
                    return math.nan
                if a[i] < min_val:
                    min_val = a[i]

            return min_val
        else:
            for i in range(len(a)):
                if math.isnan(a[i]):
                    return math.nan
                if a[i] < min_val:
                    min_val = a[i]

            return min_val

    @classmethod
    def mean(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> float:
        cls.__validate_not_none(a)
        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            length = hi - lo
            if length == 0:
                return math.nan

            sum = cls.sum(a, lo, hi)
            return sum / length
        else:
            if len(a) == 0:
                return math.nan
            sum = cls.sum(a)
            return sum / len(a)

    @classmethod
    def variance(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> float:
        cls.__validate_not_none(a)

        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            length = hi - lo
            if length == 0:
                return math.nan
            avg = cls.mean(a, lo, hi)
            sum = 0.0
            for i in range(lo, hi):
                sum += (a[i] - avg) * (a[i] - avg)

            return sum / (length - 1)
        else:
            if len(a) == 0:
                return math.nan
            avg = cls.mean(a)
            sum = 0.0
            for i in range(len(a)):
                sum += (a[i] - avg) * (a[i] - avg)

            return sum / (len(a) - 1)

    @classmethod
    def variancep(cls, a: List[float], lo: int = None, hi: int = None) -> float:
        cls.__validate_not_none(a)

        sum = 0.0
        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            length = hi - lo
            if length == 0:
                return math.nan

            avg = cls.mean(a, lo, hi)
            for i in range(lo, hi):
                sum += math.pow((a[i] - avg), 2)

            return sum / length
        else:
            if len(a) == 0:
                return math.nan
            avg = cls.mean(a)
            for i in range(len(a)):
                sum += math.pow((a[i] - avg), 2)

            return sum / len(a)

    @classmethod
    def stddev(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> float:
        cls.__validate_not_none(a)

        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            return math.sqrt(cls.variance(a, lo, hi))
        else:
            return math.sqrt(cls.variance(a))

    @classmethod
    def stddevp(cls, a: List[float], lo: int = None, hi: int = None) -> float:
        cls.__validate_not_none(a)

        if lo and hi:
            cls.__validate_subarr_indicies(lo, hi, len(a))
            return math.sqrt(cls.variancep(a, lo, hi))
        else:
            return math.sqrt(cls.variancep(a))

    @classmethod
    def sum(cls, a: List[(float, int)], lo: int = None, hi: int = None) -> (float, int):
        cls.__validate_not_none(a)

        if lo and hi:
            sum = 0.0
            for i in range(lo, hi):
                sum += a[i]

            return sum
        else:
            sum = 0
            for i in range(len(a)):
                sum += a[i]

            return sum

    @classmethod
    def plot_points(cls, a: List[float]) -> None:
        pass
        # cls.__validate_not_none(a)
        # n = len(a)

    @classmethod
    def plot_lines(cls, a: List[float]) -> None:
        pass

    @classmethod
    def plot_bars(cls, a: List[float]) -> None:
        pass

    @classmethod
    def __validate_not_none(cls, x: object):
        if x is None:
            raise ValueError("argument is None")

    @classmethod
    def __validate_subarr_indicies(cls, lo: int, hi: int, length: int):
        if lo < 0 or hi > length or lo > hi:
            raise ValueError("subarray indices out of bounds: [ {}, {} )".format(lo, hi))


if __name__ == '__main__':
    print()