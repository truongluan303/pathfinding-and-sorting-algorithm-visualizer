from typing import Generic, TypeVar

T = TypeVar('T')


##############################
######### LINKED QUEUE #######
class Queue(Generic[T]):
    def __init__(self) -> None:
        self.reset()

    # check if the queue is empty
    def is_empty(self) -> bool:
        return self.size == 0

    # check if the queue is initialized
    def is_initialized(self) -> bool:
        return self.initialized

    # get the size of the queue
    def get_size(self) -> int:
        return self.size

    # insert a new node 
    def enqueue(self, value: T) -> None:
        new = Node[T](value)
        if self.is_empty():
            self.head = new
            self.initialized = True
        else:
            self.tail.set_next(new)
        self.tail = new
        self.size += 1

    # get the front value 
    def peek(self) -> T:
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty queue!!!")
        result = self.head.get_value()
        return result

    # pop the queue
    def dequeue(self) -> T:
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to dequeue an empty queue!!!")
        temp = self.peek()
        self.size -= 1
        self.head = self.head.get_next()
        if self.head is None:
            self.reset()       
        return temp

    # clear the queue
    def reset(self) -> None:
        self.initialized = False
        self.head = None
        self.tail = None
        self.size = 0



#############################
####### LINKED STACK ########
class Stack(Generic[T]):
    def __init__(self) -> None:
        self.head = None
        self.initialized = False
        self.size = 0

    # check if the stack is initialized
    def is_initialized(self) -> bool:
        return self.initialized

    # check if the stack is empty
    def is_empty(self) -> bool:
        return self.size == 0

    # add new node
    # time complexity: O(1)
    def push(self, item: T) -> None:
        self.size += 1
        self.initialized = True
        new = Node[T](item)
        new.set_next(self.head)
        self.head = new

    # get the value in the front
    # time complexity: O(1)
    def peek(self) -> T:
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to peek an empty stack!!!")
        return self.head.get_value()

    # pop the value
    def pop(self) -> T:
        if not self.is_initialized() or self.is_empty():
            raise Exception("Attempted to pop an empty stack!!!")
        top_value = self.peek()
        self.head = self.head.get_next()
        self.size -= 1
        return top_value

    # get the size of the stack
    def get_size(self) -> int:
        return self.size

    # clear the stack
    def clear(self) -> None:
        self.head = None
        self.size = 0



###################################
######### PRIORITY QUEUE ##########

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.reset()

    # add new node to the queue
    # The lower the priority is, the faster it gets to be poped
    def enqueue(self, val: T, priority:float=None) -> None:
        new_node = PriorityNode[T](val, priority)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            if priority is None or priority > self.tail.get_priority():
                self.tail.set_next(new_node)
                self.tail = new_node
            elif priority <= self.head.get_priority():
                new_node.set_next(self.head)
                self.head = new_node
            else:
                current = self.head
                # find the right place to put the new node in according to the priority
                while current.get_next() is not None and current.get_next().get_priority() < priority:
                    current = current.get_next()
                temp = current.get_next()
                current.set_next(new_node)
                new_node.set_next(temp)
        self.size += 1

    # pop the node at the top of the queue
    # time complexity: O(1)
    def dequeue(self) -> T:
        if self.is_empty():
            raise Exception('Attempted to dequeue an empty queue!!!')
        temp = self.peek()
        self.head = self.head.get_next()
        self.size -= 1
        # if the new head is None, it means the queue is empty
        if self.head is None:
            self.reset()
        return temp

    # get the value in the front of the queue
    # time complexity: O(1)
    def peek(self) -> T:
        if self.is_empty():
            raise Exception('Attempted to peek an empty queue!!!')
        return self.head.get_value()

    # get the size of the queue
    def get_size(self) -> int:
        return self.size

    # check if the queue is empty
    def is_empty(self) -> bool:
        return self.size == 0

    def reset(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0




#######################
######### NODE ########
class Node(Generic[T]):
    def __init__(self, value: T, next=None) -> None:
        self.value = value
        self.next = next

    def get_value(self) -> T:
        return self.value

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next



#######################
#### PRIORITY NODE ####
class PriorityNode(Generic[T]):
    def __init__(self, value: T, priority: float, next=None) -> None:
        self.value = value
        self.priority = priority
        self.next = next

    def get_value(self) -> T:
        return self.value

    def get_priority(self) -> float:
        return self.priority

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next


#>>>>>>>>>>>>>>>>>>>> end of data_structures.py <<<<<<<<<<<<<<<<<<<<
