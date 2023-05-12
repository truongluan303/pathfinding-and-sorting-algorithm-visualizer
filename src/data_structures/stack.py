from typing import Generic
from typing import TypeVar

from .nodes import Node

T = TypeVar("T")


class Stack(Generic[T]):
    """Linked Stack"""

    def __init__(self) -> None:
        self.clear()

    def is_initialized(self) -> bool:
        """check if stack is initialized"""
        return self._initialized

    def is_empty(self) -> bool:
        """check if stack is empty"""
        return self._size == 0

    def push(self, item: T) -> None:
        """add a new node to the stack
        args:
            item:
                the new item to be added
        """
        self._size += 1
        self._initialized = True
        new = Node[T](item)
        new.set_next(self._head)
        self._head = new

    def peek(self) -> T:
        """get the value on top of the stack"""
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty stack!!!")
        return self._head.get_value()

    def pop(self) -> T:
        """remove and return the top value of the stack"""
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to pop an empty stack!!!")
        top_value = self.peek()
        self._head = self._head.get_next()
        self._size -= 1
        return top_value

    def get_size(self) -> int:
        """get the size of the stack"""
        return self._size

    def clear(self) -> None:
        """clear the stack"""
        self._head = None
        self._initialized = False
        self._size = 0
