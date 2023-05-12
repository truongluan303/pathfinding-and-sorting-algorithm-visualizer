from typing import Generic
from typing import TypeVar

from .nodes import PriorityNode

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """Priority Queue"""

    def __init__(self) -> None:
        self.reset()

    # add new node to the queue
    # The lower the priority is, the faster it gets to be poped
    def enqueue(self, val: T, priority: float = None) -> None:
        new_node = PriorityNode(val, priority)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            if priority is None or priority > self._tail.get_priority():
                self._tail.set_next(new_node)
                self._tail = new_node
            elif priority <= self._head.get_priority():
                new_node.set_next(self._head)
                self._head = new_node
            else:
                current = self._head
                # find the right place to put the new node in according to the priority
                while (
                    current.get_next() is not None
                    and current.get_next().get_priority() < priority
                ):
                    current = current.get_next()
                temp = current.get_next()
                current.set_next(new_node)
                new_node.set_next(temp)
        self._size += 1

    # pop the node at the top of the queue
    # time complexity: O(1)
    def dequeue(self) -> T:
        if self.is_empty():
            raise Exception("Attempted to dequeue an empty queue!!!")
        temp = self.peek()
        self._head = self._head.get_next()
        self._size -= 1
        # if the new head is None, it means the queue is empty
        if self._head is None:
            self.reset()
        return temp

    # get the value in the front of the queue
    # time complexity: O(1)
    def peek(self) -> T:
        if self.is_empty():
            raise Exception("Attempted to peek an empty queue!!!")
        return self._head.get_value()

    # get the size of the queue
    def get_size(self) -> int:
        return self._size

    # check if the queue is empty
    def is_empty(self) -> bool:
        return self._size == 0

    def reset(self) -> None:
        self._head = None
        self._tail = None
        self._size = 0
