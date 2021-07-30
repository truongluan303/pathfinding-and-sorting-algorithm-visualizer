from typing import Generic, TypeVar

T = TypeVar('T')


##############################
######### LINKED QUEUE #######
class Queue:
    def __init__(self):
        self.size = 0
        self.initialized = False
        self.head = None
        self.tail = None

    # check if the queue is empty
    def is_empty(self):
        return self.size == 0

    # check if the queue is initialized
    def is_initialized(self):
        return self.initialized

    # get the size of the queue
    def get_size(self):
        return self.size

    # insert a new node 
    def enqueue(self, value):
        new = Node(value)
        if self.is_empty():
            self.head = new
            self.initialized = True
        else:
            self.tail.set_next(new)
        self.tail = new
        self.size += 1

    # get the front value 
    def peek(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty queue!!!")
        result = self.head.get_value()
        return result

    # pop the queue
    def dequeue(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to dequeue an empty queue!!!")
        temp = self.peek()
        self.head = self.head.get_next()
        if self.head is None:
            self.tail = None
        self.size -= 1
        return temp

    # clear the queue
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0



#############################
####### LINKED STACK ########
class Stack:
    def __init__(self):
        self.head = Node(None)
        self.initialized = False
        self.size = 0

    # check if the stack is initialized
    def is_initialized(self):
        return self.initialized

    # check if the stack is empty
    def is_empty(self):
        return self.size == 0

    # add new node
    def push(self, item: T):
        self.size += 1
        self.initialized = True
        new = Node(item)
        new.set_next(self.head.get_next())
        self.head.set_next(new)

    # get the value in the front
    def peek(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty stack!!!")
        return self.head.get_next().get_value()

    # pop the value
    def pop(self):
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to pop an empty stack!!!")
        topValue = self.peek()
        self.head.set_next(self.head.get_next().get_next())
        self.size -= 1
        return topValue

    # get the size of the stack
    def get_size(self):
        return self.size

    # clear the stack
    def clear(self):
        self.head = None
        self.size = 0



###################################
######### PRIORITY QUEUE ##########
class PriorityQueue:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    # add new node to the queue
    # The lower the priority is, the faster it gets to be out
    def enqueue(self, val, priority):
        new_node = PriorityNode(val, priority)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            if priority > self.tail.get_priority():
                self.tail.set_next(new_node)
                self.tail = new_node
            elif priority < self.head.get_priority():
                new_node.set_next(self.head)
                self.head = new_node
            else:
                current = self.head
                while current.get_next() is not None and current.get_next().get_priority() <= priority:
                    current = current.get_next()
                temp = current.get_next()
                current.set_next(new_node)
                new_node.set_next(temp)
        self.size += 1

    # pop the node at the top of the queue
    def dequeue(self):
        if self.is_empty():
            raise Exception('Attempted to dequeue an empty queue!!!')
        # pop the head
        temp = self.head
        self.head = self.head.get_next()
        temp.set_next(None)
        self.size -= 1
        return temp.get_value()

    # get the value in the front of the queue
    def peek(self):
        if self.is_empty():
            raise Exception('Attempted to peek an empty queue!!!')
        return self.head.get_value()

    # get the size of the queue
    def get_size(self):
        return self.size

    # check if the queue is empty
    def is_empty(self):
        return self.size == 0



#######################
######### NODE ########
class Node:
    def __init__(self, value = None):
        self.value = value
        self.next = None

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next



#######################
#### PRIORITY NODE ####
class PriorityNode:
    def __init__(self, value, priority, next=None):
        self.value = value
        self.priority = priority
        self.next = next

    def get_value(self):
        return self.value

    def get_priority(self):
        return self.priority

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next
