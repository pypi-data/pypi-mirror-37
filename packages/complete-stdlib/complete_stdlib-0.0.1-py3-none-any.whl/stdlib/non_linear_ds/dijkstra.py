import math

from stdlib.non_linear_ds.directededge import DirectedEdge
from stdlib.non_linear_ds.edgeweighteddigraph import EdgeWeightedDigraph
from stdlib.linear_ds.indexminpq import IndexMinPQ
from stdlib.linear_ds.stack import Stack


class Dijkstra:
    def __init__(self, G: EdgeWeightedDigraph, s: int):
        for e in G.edges():
            if e.weight() < 0:
                raise ValueError("edge {0} has negative weight.".format(e))

        self.__dist_to = [math.inf for i in range(G.V())]
        self.__edge_to = [DirectedEdge() for i in range(G.V())]

        self.__validate_vertex(s)
        self.__dist_to[s] = 0.0

        self.__pq = IndexMinPQ(G.V())
        self.__pq.insert(s, self.__dist_to[s])
        while not self.__pq.__empty__():
            v = self.__pq.del_min()
            for e in G.adj(v):
                self.__relax(e)

        assert self.__check(G, s)

    def dist_to(self, v: int) -> float:
        self.__validate_vertex(v)
        return self.__dist_to[v]

    def has_path_to(self, v: int) -> bool:
        self.__validate_vertex(v)
        return self.__dist_to[v] < math.inf

    def path_to(self, v: int) -> DirectedEdge:
        self.__validate_vertex(v)
        if not self.has_path_to(v):
            return None

        path = Stack.Stack()
        e = self.__edge_to[v]
        while e is not None:
            path.push(e)
            e = self.__edge_to[e.fromm()]

        return path

    def __check(self, G: EdgeWeightedDigraph, s: int) -> bool:
        for e in G.edges():
            if e.weight() < 0:
                print("Negative edge weight detected")
                return False

        if self.__dist_to[s] != 0.0 or self.__edge_to[s] is not None:
            print("dist_to[{0}] and edge_to[{0}] are inconsistent".format(s))
            return False

        for v in range(G.V()):
            if v == s:
                continue

            if self.__edge_to[v] is None and self.__dist_to[s] != math.inf:
                print("dist_to and edge_to are inconsistent")
                return False

        for w in range(G.V()):
            if self.__edge_to[w] is None:
                continue

            e = self.__edge_to[w]
            v = e.fromm()
            if w != e.to():
                return False

            if self.__dist_to[v] + e.weight() != self.__dist_to[w]:
                print("edge {} on shortest path not tight".format(e))
                return False

        return True

    def __relax(self, e: DirectedEdge.DirectedEdge) -> None:
        v, w = e.fromm(), e.to()
        if self.__dist_to[w] > self.__dist_to[v] + e.weight():
            self.__dist_to[w] = self.__dist_to[v] + e.weight()
            self.__edge_to[w] = e
            if self.__pq.__contains__(w):
                print(v, w, 'contains')
                self.__pq.decrease_key(w, self.__dist_to[w])

            else:
                print(v, w, 'does not contain')
                self.__pq.insert(w, self.__dist_to[w])

    def __validate_vertex(self, v: int) -> None:
        V = len(self.__dist_to)
        if v < 0 or v >= V:
            raise IndexError("vertex {} is not between 0 and {}".format(v, V - 1))


def main():
    import stdlib.utils.inn as In
    import os
    dir_path = os.getcwd()
    inn = In.In('{0}/tests/tinyEWD.txt'.format(dir_path))
    g = EdgeWeightedDigraph.EdgeWeightedDigraph(inn=inn)
    s = 1
    sp = Dijkstra(g, s)

    for t in range(g.V()):
        if sp.has_path_to(t):
            print("{} to {} {:.2f} ".format(s, t, sp.dist_to(t)))
            for e in sp.path_to(t):
                print("{} ".format(e))

            print()

        else:
            print("{} to {}\tno path\n".format(s, t))


if __name__ == '__main__':
    main()
