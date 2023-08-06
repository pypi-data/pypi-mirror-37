import os
from stdlib.abstracts.iterable import Iterable

from stdlib.linear_ds.stack import Stack
from stdlib.linear_ds.bag import Bag
from stdlib.utils.inn import In


class Graph(object):
    def __init__(self, V: int = None, inn: In = None, G=None):
        self.__NEWLINE = '\n'
        self.V = V
        self.E = 0

        if V:
            if V < 0:
                raise ValueError("Number of vertices must be non-negative")
            self.V = V
            self.E = 0
            self._adj = [Bag() for i in range(V)]

        elif inn:
            try:
                self.V = inn.read_int()
                if self.V < 0:
                    raise ValueError("Number of vertices must be non-negative")

                self._adj = [Bag() for i in range(self.V)]

                E = inn.read_int()
                if E < 0:
                    raise ValueError("Number of edges in a Graph must be non-negative")

                # Iterate through each line in the file
                for i in range(E):
                    v = inn.read_int()
                    w = inn.read_int()
                    self.__validate_vertex(v)
                    self.__validate_vertex(w)
                    self.add_edge(v, w)

            except (IndexError, ValueError) as e:
                raise IndexError("Invalid input format in Graph contructor")

        elif G:
            self.__init__(V=G.V)
            self.E = G.E
            for v in range(G.V):
                reverse = Stack()
                for w in G.adj[v]:
                    reverse.push(w)

                for w in reverse:
                    self._adj[v].add(w)

    def __validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self.V:
            raise ValueError("vertex {0} is not between 0 and {1}".format(v, self.V - 1))

    def add_edge(self, v: int, w: int) -> None:
        self.__validate_vertex(v)
        self.__validate_vertex(w)
        self.E += 1
        self._adj[v].add(w)
        self._adj[w].add(v)

    def adj(self, v: int) -> Iterable:
        self.__validate_vertex(v)
        return self._adj[v]

    def degree(self, v: int) -> int:
        self.__validate_vertex(v)
        return self._adj[v].__sizeof__()

    def __str__(self):
        s = ''
        s += "{0} vertices {1} edges\n".format(self.V, self.E)
        for v in range(self.V):
            s += '{0}: '.format(v)
            for w in self._adj[v]:
                s += "{0} ".format(w)

            s += '\n'

        return s


def main():
    dirpath = os.getcwd()
    inn = In('{0}/tests/tinyDG.txt'.format(dirpath))
    g = Graph(inn=inn)
    print(g)


if __name__ == '__main__':
    main()
