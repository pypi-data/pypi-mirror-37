from typing import Iterable

from stdlib.linear_ds.bag import Bag
from stdlib.utils.inn import In
from stdlib.linear_ds.stack import Stack


class Digraph(object):
    def __init__(self, V: int=None, inn: In=None, G=None):
        self.V = V
        self.E = 0
        self._adj = None
        self._indegree = None

        if V:
            if V < 0:
                raise ValueError("Number of vertices must be non negative")
            self.V = V
            self._adj = [Bag() for i in range(V)]
            self._indegree = [0 for i in range(V)]

        elif inn:
            try:
                self.V = inn.read_int()
                if self.V < 0:
                    raise ValueError("Number of vertices must be non negative")
                self._indegree = [0 for i in range(self.V)]
                self._adj = [Bag() for i in range(self.V)]
                E = inn.read_int()
                if E < 0:
                    raise ValueError("number of edges must be non negative")

                for i in range(E):
                    v = inn.read_int()
                    w = inn.read_int()
                    self.add_edge(v, w)

            except (IndexError, ValueError, TypeError, KeyError, ArithmeticError):
                raise ValueError("Invalid input format in constructor")

        elif G:
            self.__init__(V=G.V)
            self.E = G.E
            self._adj = [Bag() for i in range(self.V)]
            self._indegree = [0 for i in range(self.V)]
            for v in range(self.V):
                self._indegree[v] = G.indegree(v)

            for v in range(G.V):
                reverse = Stack()
                for w in G._adj[v]:
                    reverse.push(w)

                for w in reverse:
                    self._adj[v].add(w)

    def add_edge(self, v: int, w: int) -> None:
        self.__validate_vertex(v)
        self.__validate_vertex(w)
        self._adj[v].add(w)
        self._indegree[w] += 1
        self.E += 1

    def __validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self.V:
            raise ValueError("vertex {0} is not between 0 and {1}".format(v, self.V - 1))

    def adj(self, v: int) -> Iterable:
        self.__validate_vertex(v)
        return self._adj[v]

    def outdegree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self._adj[v].__sizeof__()

    def indegree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self._indegree[v]

    def reverse(self):
        reverse = self.__init__(self.V)
        for v in range(self.V):
            for w in self.adj(v):
                reverse.add_edge(w, v)

        return reverse

    def __str__(self):
        s = ''
        s += "{0} vertices, {1} edges \n".format(self.V, self.E)
        for v in range(self.V):
            s += "{0}: ".format(v)
            for w in self._adj[v]:
                s += "{0} ".format(w)

            s += "\n"

        return s


def main():
    import os
    dirpath = os.getcwd()
    inn = In('{0}/tests/tinyDG.txt'.format(dirpath))
    g = Digraph(inn=inn)
    print(g)


if __name__ == '__main__':
    main()
