from typing import Iterable

from stdlib.non_linear_ds.digraph import Digraph
from stdlib.non_linear_ds.edgeweighteddigraph import EdgeWeightedDigraph
from stdlib.linear_ds.queue import Queue
from stdlib.linear_ds.stack import Stack


class DepthFirstOrder(object):
    def __init__(self, G: Digraph = None, EWG: EdgeWeightedDigraph = None):
        self._marked = [False for i in range(G.V)]
        self._pre = [0 for i in range(G.V)]
        self._post = [0 for i in range(G.V)]
        self._preorder = Queue()
        self._postorder = Queue()
        self._pre_counter = 0
        self._post_counter = 0

        if G:
            for v in range(G.V):
                if not self._marked[v]:
                    self.dfs(v, G=G)

            assert self.__check()

        elif EWG:
            for v in range(EWG.V):
                if not self._marked[v]:
                    self.dfs(v, EWG=EWG)

    def dfs(self, v: int, G: Digraph = None, EWG: EdgeWeightedDigraph = None):
        if not G and not EWG:
            raise ValueError("You have to provide a digraph or edge weighted digraph")

        self._marked[v] = True
        self._pre[v] = self._pre_counter
        self._pre_counter += 1
        self._preorder.enqueue(v)
        if G:
            for w in G.adj(v):
                if not self._marked[w]:
                    self.dfs(w, G=G)

        elif EWG:
            for e in EWG.adj(v):
                w = e.to()
                if not self._marked[w]:
                    self.dfs(w, EWG=EWG)

        self._postorder.enqueue(v)
        self._post[v] = self._post_counter
        self._post_counter += 1

    def pre(self, v: int = None) -> int or Queue:
        if not v:
            return self._preorder
        else:
            self.__validate_vertex(v)
            return self._pre[v]

    def post(self, v: int = None) -> int or Queue:
        if not v:
            return self._postorder
        else:
            self.__validate_vertex(v)
            return self._post[v]

    def reverse_post(self) -> Iterable:
        reverse = Stack()
        for v in self._postorder:
            reverse.push(v)

        return reverse

    def __check(self) -> bool:
        r = 0
        for v in self.post():
            if self.post(v) != r:
                print("post(v) and post() inconsistent")
                return False

            r += 1

        r = 0
        for v in self.pre():
            if self.pre(v) != r:
                print("pre(v) and pre() inconsistent")
                return False

            r += 1

        return True

    def __validate_vertex(self, v: int) -> None:
        V = len(self._marked)
        if v < 0 or v >= V:
            raise ValueError("vertex {} is not between 0 and {}".format(v, V - 1))


def main():
    import os
    from stdlib.utils.inn import In
    dirpath = os.getcwd()
    inn = In('{0}/tests/tinyDG.txt'.format(dirpath))
    g = Digraph(inn=inn)

    dfs = DepthFirstOrder(G=g)
    print("   v  pre post")
    print("--------------")
    s = ''
    for v in range(g.V):
        s += '\t{} \t{} \t{}\n'.format(v, dfs.pre(v), dfs.post(v))

    s += 'Preorder: '
    for v in dfs.pre():
        s += '{} '.format(v)

    s += '\nPostorder: '
    for v in dfs.post():
        s += '{} '.format(v)

    s += '\nReverse postorder: '
    for v in dfs.reverse_post():
        s += '{} '.format(v)

    print(s)


if __name__ == '__main__':
    main()
