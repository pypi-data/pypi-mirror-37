import time

from stdlib.linear_ds.queue import Queue


class Singleton(object):
    __instance = None

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("This class is definitely a singleton! And has been initialized")
        else:
            Singleton.__instance = self

    @staticmethod
    def get_instance():
        if Singleton.__instance is None:
            Singleton()

        return Singleton.__instance

    @staticmethod
    def set_instance(item):
        Singleton.__instance = item


if __name__ == '__main__':
    s = Singleton()
    print(s)
    s.set_instance(Queue())
    print(type(s))
    time.sleep(5)
    s.get_instance().enqueue("help")
    print(s.get_instance())
