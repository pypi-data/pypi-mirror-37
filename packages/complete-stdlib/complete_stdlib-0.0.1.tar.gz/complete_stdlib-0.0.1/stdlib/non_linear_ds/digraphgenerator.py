import random

from stdlib.abstracts.comparable import Comparable
from stdlib.non_linear_ds.digraph import Digraph
from stdlib.non_linear_ds.edge import Edge


class DigraphGenerator(object):
    class Edge(Comparable):
        def __init__(self, v: int, w: int):
            self.v = None
            self.w = None

        def compare_to(self, other: Edge):
            if self.v < other.v or self.w < other.w:
                return False

            if self.v > other.v or self.w > other.w:
                return True

    def simple(self, V: int, E: int) -> Digraph:
        if E > V * (V - 1):
            raise ValueError("Too many edges")

        if E < 0:
            raise ValueError("Too few edges")

        g = Digraph(V)
        s = set()
        while g.E < E:
            v = random.uniform(V)
            w = random.uniform(V)
            e = Edge(v, w)
            if v != w and e not in s:
                s.add(e)
                g.add_edge(v, w)

        return g

    def _simple(self, V: int, p: float) -> Digraph:
        if p < 0.0 or p > 1.0:
            raise ValueError("Probability must be between 0 and 1")

        g = Digraph(V)

        for v in range(V):
            for w in range(V):
                if v != w:
                    if random.uniform() < p:
                        g.add_edge(v, w)

        return g

    def complete(self, V: int) -> Digraph:
        return self.simple(V, V * (V - 1))

    def dag(self, V: int, E: int) -> Digraph:
        if E > V * (V - 1) / 2:
            raise ValueError("Too many edges")

        if E < 0:
            raise ValueError("Too few edges")

        g = Digraph(V)
        s = set()
        vertices = [i for i in range(V)]
        random.shuffle(vertices)
        while g.E < E:
            v = random.uniform(V)
            w = random.uniform(V)
            e = Edge(v, w)
            if v < w and e not in s:
                s.add(e)
                g.add_edge(vertices[v], vertices[w])

        return g

    def tournament(self, V: int) -> Digraph:
        g = Digraph(V)
        for v in range(g.V):
            for w in range(v + 1, g.V):
                if random.uniform() < 0.5:
                    g.add_edge(v, w)

                else:
                    g.add_edge(w, v)

        return g

