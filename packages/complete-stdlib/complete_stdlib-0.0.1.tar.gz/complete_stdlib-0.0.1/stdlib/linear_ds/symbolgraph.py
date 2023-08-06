from stdlib.non_linear_ds.graph import Graph
from stdlib.utils.inn import In


class SymbolGraph(object):
    def __init__(self, filename: str, delimiter: str):
        self.st = {}
        self.keys = []
        self.G = None
        inn = In(filename)

        while not inn.__empty__():
            a = inn.read_line().split(delimiter)
            for i in range(len(a)):
                if not a[i] in self.st.keys():
                    self.st[a[i]] = len(self.st)

        print("Done reading {0}".format(filename))

        self.keys = [] * len(self.st)
        for name in self.st.keys():
            self.keys[self.st.get(name)] = name

        self.G = Graph(len(self.st))
        inn = In(filename)
        while inn.has_next_line():
            a = inn.read_line().split(delimiter)
            v = self.st.get(a[0])
            for i in range(1, len(a)):
                w = self.st.get(a[i])
                self.G.add_edge(v, w)

    def __contains__(self, item):
        return item in self.st

    def index_of(self, item: str) -> int:
        return self.st.get(item)

    def name_of(self, v: int) -> str:
        self.__validate_vertex(v)
        return self.keys[v]

    def graph(self):
        return self.G

    def __validate_vertex(self, v: int) -> None:
        V = self.G.V
        if v < 0 or v >= V:
            raise IndexError("vertex {0} is not between 0 and {1}".format(v, V - 1))


def main():
    import os
    from stdlib.stdlib.stdin import StdIn
    dirpath = os.getcwd()
    filename = '{0}/tests/tinyEWD.txt'.format(dirpath)
    delimiter = ' '
    sg = SymbolGraph(filename, delimiter)
    graph = sg.graph()
    while StdIn.has_next_line():
        src = StdIn.read_line()
        if sg.__contains__(src):
            s = sg.index_of(src)
            for v in graph.adj(s):
                print("   {0}".format(sg.name_of(v)))

        else:
            print("Input does not contain {0}".format(src))


if __name__ == '__main__':
    main()
