import math


class DirectedEdge(object):
    def __init__(self, v: int = 0, w: int = 0, weight: float = 0):
        if v < 0:
            raise ValueError("vertex must be non negative integer")
        if w < 0:
            raise ValueError("vertex must be non negative integer")
        if math.isnan(weight):
            raise ValueError("weight is NaN")
        self.__v = v
        self.__w = w
        self.__weight = weight

    def fromm(self):
        return self.__v

    def to(self):
        return self.__w

    def weight(self) -> float:
        return self.__weight

    def __str__(self):
        return '{}->{} {:.2}    '.format(self.__v, self.__w, self.__weight)


def main():
    e = DirectedEdge(12, 34, 5.67)
    print(e)


if __name__ == '__main__':
    main()
