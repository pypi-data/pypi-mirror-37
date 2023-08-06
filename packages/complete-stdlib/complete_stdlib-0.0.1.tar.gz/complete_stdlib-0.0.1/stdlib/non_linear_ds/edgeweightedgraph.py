import random
from typing import Iterable

from stdlib.linear_ds.bag import Bag
from stdlib.non_linear_ds.edge import Edge
from stdlib.utils.inn import In
from stdlib.linear_ds.stack import Stack


class EdgeWeightedGraph(object):
    def __init__(self, V: int = None, E: int = None, inn: In = None, G = None):
        self.V = V
        self.E = E

        if V:
            if V < 0:
                raise ValueError("number of vertices must be non negative")
            self.V = V
            self.E = 0
            self._adj = [Bag() for i in range(V)]

        elif E and not V:
            raise ValueError("parameter V needs to be provided if you are providing E")

        elif V and E:
            self.__init__(V=V)
            if E < 0:
                raise ValueError("number of edges must be non negative")

            for i in range(E):
                v = random.randint(0, V)
                w = random.randint(0, V)
                weight = float(round(100 * random.randint()) / 100.0)
                e = Edge(v, w, weight)
                self.add_edge(e)

        elif inn:
            self.__init__(V=inn.read_int())
            E = inn.read_int()
            if E < 0:
                raise ValueError("number of edges must be non negative")

            for i in range(E):
                v = inn.read_int()
                w = inn.read_int()
                self.__validate_vertex(v)
                self.__validate_vertex(w)
                weight = inn.read_float()
                e = Edge(v, w, weight)
                self.add_edge(e)

        elif G:
            self.__init__(V=G.V)
            self.E = G.E
            for v in range(G.V):
                reverse = Stack()
                for e in G.adj(v):
                    reverse.push(e)

                for e in reverse:
                    self._adj[v].add(e)

    def add_edge(self, e: Edge):
        v = e.either()
        w = e.other(v)
        self._adj[v].add(e)
        self._adj[w].add(e)
        self.E += 1

    def adj(self, v: int) -> Iterable:
        self.__validate_vertex(v)
        return self._adj[v]

    def degree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self._adj[v].__sizeof__()

    def edges(self) -> Iterable:
        list = Bag()
        for v in range(self.V):
            self_loops = 0
            for e in self.adj(v):
                if e.other(v) > v:
                    list.add(e)

                elif e.other(v) == v:
                    if self_loops % 2 == 0:
                        list.add(e)
                    self_loops += 1

        return list

    def __validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self.V:
            raise ValueError("vertex {0} is not between 0 and {1}".format(v, self.V - 1))

    def __str__(self):
        s = '{0} {1}\n'.format(self.V, self.E)
        for v in range(self.V):
            s += '{0}: '.format(v)
            for e in self._adj[v]:
                s += '{0} '.format(e)

            s += '\n'

        return s


def main():
    import os
    dirpath = os.getcwd()
    inn = In('{0}/tests/tinyEWD.txt'.format(dirpath))
    ewg = EdgeWeightedGraph(inn=inn)
    print(ewg)


if __name__ == '__main__':
    main()
