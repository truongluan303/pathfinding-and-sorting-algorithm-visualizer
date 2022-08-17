from typing import Generic
from typing import TypeVar

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
