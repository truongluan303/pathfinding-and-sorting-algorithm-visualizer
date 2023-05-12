from typing import Generic
from typing import TypeVar

from .nodes import Node

T = TypeVar("T")


class Queue(Generic[T]):
    """Linked Queue"""

    def __init__(self) -> None:
        self.reset()

    def is_empty(self) -> bool:
        """check if the queue is empty"""
        return self._size == 0

    def is_initialized(self) -> bool:
        """check if the queue is initialized"""
        return self._initialized

    def get_size(self) -> int:
        """get the size of the queue"""
        return self._size

    def enqueue(self, value: T) -> None:
        """insert a new node to the end of the queue"""
        new = Node[T](value)
        if self.is_empty():
            self._head = new
            self._initialized = True
        else:
            self._tail.set_next(new)
        self._tail = new
        self._size += 1

    def peek(self) -> T:
        """get the element on the top of the queue"""
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty queue!!!")
        result = self._head.get_value()
        return result

    def dequeue(self) -> T:
        """remove and return the element on top of the queue"""
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to dequeue an empty queue!!!")
        temp = self.peek()
        self._size -= 1
        self._head = self._head.get_next()
        if self._head is None:
            self.reset()
        return temp

    def reset(self) -> None:
        """clear the queue"""
        self._initialized = False
        self._head = None
        self._tail = None
        self._size = 0
