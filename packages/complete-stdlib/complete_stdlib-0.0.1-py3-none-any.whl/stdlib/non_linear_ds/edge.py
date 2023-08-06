class Edge(object):
    def __init__(self, v: int, w: int, weight: float = 0.0):
        if v < 0:
            raise ValueError("vertex must be non negative integer")
        if w < 0:
            raise ValueError("vertex must be non negative integer")
        self.v = v
        self.w = w
        self.weight = weight

    def either(self) -> int:
        return self.v

    def other(self, vertex: int) -> int:
        if vertex == self.v:
            return self.w
        elif vertex == self.w:
            return self.v
        else:
            raise ValueError("Illegal endpoint!!")

    def compare_to(self, that) -> int:
        return self.weight > that.weight

    def __str__(self):
        return "{}-{} {:.5}".format(self.v, self.w, self.weight)


def main():
    e = Edge(12, 34, 5.67)
    print(e)


if __name__ == '__main__':
    main()
