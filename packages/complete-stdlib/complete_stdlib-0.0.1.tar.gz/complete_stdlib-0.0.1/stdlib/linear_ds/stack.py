from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator
import typing


class Stack(Iterable):
    # __first = ...  # type: Node

    class Node(object):
        # item = ...  # type: object

        def __init__(self):
            self.item = None
            self.next = self

    def __init__(self):
        self.__first = None
        self.__n = 0

    def __empty__(self) -> bool:
        return self.__first is None

    def __sizeof__(self) -> int:
        return self.__n

    def push(self, item: object):
        old_first = self.__first
        self.__first = self.Node()
        self.__first.item = item
        self.__first.next = old_first
        self.__n += 1

    def pop(self) -> object:
        if self.__empty__():
            raise IndexError("stack underflow")

        item = self.__first.item
        self.__first = self.__first.next
        self.__n -= 1
        return item

    def peek(self) -> object:
        if self.__empty__():
            raise IndexError("Stack underflow")
        return self.__first.item

    def __str__(self):
        s = ' '
        for item in self:
            s += str(item)
            s += ' '

        return s

    def __iter__(self):
        return ListIterator(self.__first)


class ListIterator(Iterator):
    def __init__(self, first):
        self.__current = first

    def __remove__(self):
        raise NotImplementedError()

    def __has_next__(self) -> bool:
        return self.__current is not None

    def __next__(self) -> typing.Generic:
        if not self.__has_next__():
            raise StopIteration

        item = self.__current.item
        self.__current = self.__current.next
        return item


if __name__ == '__main__':
    stack = Stack()
    a = ['help', 'me', 'im', 'starving', 'please', 'sir']
    for i in a:
        stack.push(i)

    for i in stack:
        print(stack.pop())

    print(stack.__sizeof__())
