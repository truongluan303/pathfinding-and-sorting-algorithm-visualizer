from typing import Generic
from typing import TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Linked List Node"""

    def __init__(self, value: T, next=None) -> None:
        self._value = value
        self._next = next

    def get_value(self) -> T:
        return self._value

    def get_next(self):
        return self._next

    def set_next(self, next):
        self._next = next


class PriorityNode(Node):
    """Priority Node"""

    def __init__(self, value, priority: float, next_node=None) -> None:
        super().__init__(value, next_node)
        self._priority = priority

    def get_priority(self) -> float:
        return self._priority
