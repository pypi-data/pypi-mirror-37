import random
from typing import Iterable

from stdlib.linear_ds.bag import Bag
from stdlib.non_linear_ds.directededge import DirectedEdge
from stdlib.utils.inn import In
from stdlib.linear_ds.stack import Stack


class EdgeWeightedDigraph(object):
    def __init__(self, V: int = None, E: int = None, inn: In = None, G=None):
        self.__V = V
        self.__E = E
        self.__indegree = []

        if V:
            if V < 0:
                raise ValueError("number of vertices must be non negative")
            self.__V = V
            self.__E = 0
            self.__indegree = [0 for i in range(V)]
            self.__adj = [Bag() for i in range(V)]

        elif E and not V:
            raise ValueError("parameter V needs to be provided if you are providing E")

        elif V and E:
            self.__init__(V=V)
            if E < 0:
                raise ValueError("number of edges must be non negative")

            for i in range(E):
                v = random.randint(0, V)
                w = random.randint(0, V)
                weight = float(0.01 * random.randint(0, 100))
                e = DirectedEdge(v, w, weight)
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
                self.add_edge(DirectedEdge(v, w, weight))

        elif G:
            self.__init__(V=G.V)
            self.__E = G.E
            for v in range(G.V):
                self.__indegree[v] = G.indegree(v)

            for v in range(G.V):
                reverse = Stack()
                for e in G.adj(v):
                    reverse.push(e)

                for e in reverse:
                    self.__adj[v].add(e)

    def __validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self.__V:
            raise ValueError("vertex {0} is not between 0 and {1}".format(v, self.__V - 1))

    def V(self) -> int:
        return self.__V

    def E(self) -> int:
        return self.__E

    def add_edge(self, e: DirectedEdge) -> None:
        v = e.fromm()
        w = e.to()
        self.__validate_vertex(v)
        self.__validate_vertex(w)
        self.__adj[v].add(e)
        self.__indegree[w] += 1
        self.__E += 1

    def adj(self, v: int) -> Iterable:
        self.__validate_vertex(v)
        return self.__adj[v]

    def outdegree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self.__adj[v].__sizeof__()

    def indegree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self.__indegree[v]

    def edges(self) -> Iterable:
        _list = Bag()
        for v in range(self.__V):
            for e in self.adj(v):
                _list.add(e)

        return _list

    def __str__(self):
        s = '{} {}\n'.format(self.__V, self.__E)
        for v in range(self.__V):
            s += '{}: '.format(v)
            for e in self.__adj[v]:
                s += '{} '.format(e)

            s += '\n'

        return s


def main():
    import os
    dir_path = os.getcwd()
    inn = In('{0}/tests/tinyEWD.txt'.format(dir_path))
    ewd = EdgeWeightedDigraph(inn=inn)
    print(ewd)


if __name__ == '__main__':
    main()
