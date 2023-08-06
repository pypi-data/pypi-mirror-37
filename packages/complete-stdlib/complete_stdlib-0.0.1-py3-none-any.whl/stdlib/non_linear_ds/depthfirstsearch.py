from stdlib.non_linear_ds.graph import Graph


class DepthFirstSearch(object):
    def __init__(self, G: Graph, s: int):
        self._count = 0
        self._marked = [False for i in range(G.V)]
        self.__validate_vertex(s)
        self.__dfs(G, s)

    def __dfs(self, G: Graph, v: int) -> None:
        self._count += 1
        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self.__dfs(G, w)

    def marked(self, v: int) -> bool:
        self.__validate_vertex(v)
        return self._marked[v]

    def count(self) -> int:
        return self._count

    def __validate_vertex(self, v: int) -> None:
        V = len(self._marked)
        if v < 0 or v >= V:
            raise ValueError("vertex {0} is not between 0 and {1}".format(v, V - 1))


def main():
    import os
    from stdlib.utils.inn import In
    dirpath = os.getcwd()
    inn = In('{0}/tests/tinyDG.txt'.format(dirpath))
    g = Graph(inn=inn)
    s = 0
    search = DepthFirstSearch(g, s)
    for v in range(g.V):
        if search.marked(v):
            print('{0} '.format(v))

    print()
    if search.count() != g.V:
        print("NOT connected")
    else:
        print('connected')


if __name__ == '__main__':
    main()
