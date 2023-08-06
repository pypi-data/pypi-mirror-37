from typing import Generic

from stdlib.linear_ds.treemap import TreeMap
from stdlib.abstracts.comparable import Comparable
from stdlib.abstracts.iterable import Iterable


class SymbolTable(Comparable, Iterable):
    def compare_to(self, other) -> int:
        pass

    def __iter__(self):
        pass

    def __init__(self):
        self.__st = TreeMap()

    def get(self, key: Generic) -> Generic:
        if key is None:
            raise ValueError("calls get() with None key")
        return self.__st.get(key)

    def put(self, key: Generic, val: Generic) -> None:
        if key is None:
            raise ValueError("called put() with None key")

        if val is None:
            self.__st.remove(key)