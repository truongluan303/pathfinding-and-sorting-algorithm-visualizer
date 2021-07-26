from typing import Generic, TypeVar

T = TypeVar('T')


##############################
######### LINKED QUEUE #######
class LinkedQueue(Generic[T]):
    def __init__(self):
        self.size = 0
        self.initialized = False
        self.topNode: Node[T] = None
        self.lastNode: Node[T] = None
    def is_empty(self):
        return self.size == 0

    def is_initialized(self):
        return self.initialized

    def get_size(self):
        return self.size

    def enqueue(self, value):
        newNode = Node[T](value)
        if self.is_empty():
            self.topNode = newNode
            self.initialized = True
        else:
            self.lastNode.set_next(newNode)
        self.lastNode = newNode
        self.size += 1

    def get_front(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty queue!!!")
        result = self.topNode.get_value()
        return result

    def dequeue(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to dequeue an empty queue!!!")
        temp = self.get_front()
        self.topNode = self.topNode.get_next()
        if self.topNode is None:
            self.lastNode = None
        self.size -= 1
        return temp

    def clear(self):
        self.topNode = Node[T](None)
        self.lastNode = Node[T](None)
        self.size = 0



#############################
####### LINKED STACK ########
class LinkedStack(Generic[T]):
    def __init__(self):
        self.topNode = Node[T](None)
        self.initialized = False
        self.size = 0

    def is_initialized(self):
        return self.initialized

    def is_empty(self):
        return self.size == 0

    def push(self, item: T):
        self.size += 1
        self.initialized = True
        newNode = Node(item)
        newNode.set_next(self.topNode.get_next())
        self.topNode.set_next(newNode)

    def peek(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty stack!!!")
        return self.topNode.get_next().get_value()

    def pop(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to pop an empty stack!!!")
        topValue = self.peek()
        self.topNode.set_next(self.topNode.get_next().get_next())
        self.size -= 1
        return topValue

    def get_size(self):
        return self.size

    def clear(self):
        self.topNode = None
        self.size = 0



#######################
######### NODE ########
class Node(Generic[T]):
    def __init__(self, value: T = None):
        self.value = value
        self.next = None

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next

    def set_value(self, value):
        self.value = value

    def set_next(self, next):
        self.next = next