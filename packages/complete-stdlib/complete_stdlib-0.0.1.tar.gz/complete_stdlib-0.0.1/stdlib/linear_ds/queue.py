from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator

from typing import Generic


class Queue(Iterable):
    class Node(object):
        def __init__(self):
            self.item = None
            self.next = type(self)

    class ListIterator(Iterator):
        def __remove__(self):
            raise NotImplementedError()

        def __has_next__(self) -> bool:
            return type(self.__current.next).__name__ == 'Node'

        def __init__(self, first):
            self.__current = first

        def __next__(self) -> Generic:
            if not self.__has_next__():
                raise StopIteration

            item = self.__current.item
            self.__current = self.__current.next
            return item

    def __init__(self):
        self.__first = self.Node()  # this is of type Node. It needs to be its own instantiated object
        self.__last = self.Node()
        self.__n = 0

    def __iter__(self):
        return self.ListIterator(self.__first)

    def __empty__(self) -> bool:
        return self.__first.item is None

    def __sizeof__(self) -> int:
        return self.__n

    def peek(self):
        if self.__empty__():
            raise IndexError("Queue underflow")
        return self.__first.item

    def enqueue(self, item: object):
        oldlast = self.__last
        self.__last = self.Node()
        self.__last.item = item
        self.__last.next = self.Node()
        if self.__empty__():
            self.__first = self.__last
        else:
            oldlast.next = self.__last
        self.__n += 1

    def put(self, item: object):
        oldlast = self.__last
        self.__last = self.Node()
        self.__last.item = item
        self.__last.next = self.Node()
        if self.__empty__():
            self.__first = self.__last
        else:
            oldlast.next = self.__last
        self.__n += 1

    def dequeue(self):
        if self.__empty__():
            raise IndexError("Queue underflow")
        item = self.__first.item
        self.__first = self.__first.next
        self.__n -= 1
        if self.__empty__():
            self.__last = None
        return item

    def __str__(self) -> str:
        s = ''
        for item in self:
            s += str(item)
            s += ' '

        return s


if __name__ == '__main__':
    queue = Queue()
    test = ['help', 'me', 'im', 'starving', 'please', 'sir']
    for item in test:
        if item != '-':
            queue.enqueue(item)

    for item in queue:
        print(item)

    while not queue.__empty__():
        print(queue.dequeue())
        print(queue.__sizeof__())
