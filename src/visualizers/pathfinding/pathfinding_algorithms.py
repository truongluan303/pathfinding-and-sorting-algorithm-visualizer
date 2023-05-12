import sys

from .block import Block
from src.data_structures import PriorityQueue
from src.data_structures import Queue
from src.data_structures import Stack


def depth_first(start_block: Block, input_handling, is_running) -> None:
    """
    Depth first search algorithm
    Args:
        start_block (Block): the start block
    """
    found = False
    stack = Stack()
    stack.push(start_block)  # initialize the stack with the stack block

    while not stack.is_empty() and is_running():
        current: Block = stack.pop()

        if current.is_end_block():
            found = True
            break
        for neighbor in current.get_neighbors():
            if not neighbor.is_visited() and not neighbor.is_next():
                neighbor.set_next()
                neighbor.set_parent(current)
                stack.push(neighbor)
        current.set_visited()
        input_handling()

    if found:
        __backtrack(current.get_parent(), is_running)  # backtrack to show the path


def breadth_first(start_block: Block, input_handling, is_running) -> None:
    """
    Breadth first search algorithm
    Args:
        start_block (Block): the start block
    """
    found = False
    queue = Queue()
    queue.enqueue(start_block)  # initialize the queue with the start block

    while not queue.is_empty() and is_running():
        current: Block = queue.dequeue()

        if current.is_end_block():
            found = True
            break
        for neighbor in current.get_neighbors():
            if not neighbor.is_visited() and not neighbor.is_next():
                neighbor.set_parent(current)
                neighbor.set_next()
                queue.enqueue(neighbor)
        current.set_visited()
        input_handling()

    if found:
        __backtrack(current.get_parent(), input_handling)  # backtrack to show the path


def dijkstra(grid, start_block: Block, input_handling, is_running) -> None:
    """
    Dijkstra algorithm
    Args:
        grid ([type]): the grid containing all blocks
        start_block (Block): the start block
    """
    found = False
    prio_queue = PriorityQueue()
    # initially assign infinity to the distance from each block to start block
    dis = {block: sys.maxsize for row in grid for block in row}
    dis[start_block] = 0

    # initialize the queue with the start block
    prio_queue.enqueue(start_block, dis[start_block])

    # loop through the queue
    while not prio_queue.is_empty() and is_running():
        current: Block = prio_queue.dequeue()

        if current.is_end_block():
            found = True
            break
        for neighbor in current.get_neighbors():
            if not neighbor.is_visited() and not neighbor.is_next():
                # temp is the distance from current to start,
                # plus the distance from the neighbor to current block,
                # which will be 1 since all blocks are next to each other
                temp = dis[current] + 1
                # if temp is better, make it the distance
                if temp < dis[neighbor]:
                    dis[neighbor] = temp
                    neighbor.set_parent(current)
                    neighbor.set_next()
                    prio_queue.enqueue(neighbor, dis[neighbor])
        current.set_visited()
        input_handling()

    if found:
        __backtrack(current.get_parent(), is_running)


def a_star(
    grid, start_block: Block, end_pos: tuple, input_handling, is_running
) -> None:
    """
    A* algorithm
    Args:
        grid ([type]): the grid containing all blocks
        start_block (Block): the starting block
        end_pos (tuple): the position of the end block
    """
    found = False

    # for each block on the grid
    # g cost = distance to the starting block
    # h cost (heuristic) = distance to the end block
    # f cost (which is our priority) = g cost + h cost
    g_cost = {block: sys.maxsize for row in grid for block in row}
    g_cost[start_block] = 0
    h_cost = {block: __get_heuristic(block, end_pos) for row in grid for block in row}
    f_cost = {block: (g_cost[block] + h_cost[block]) for row in grid for block in row}

    p_queue = PriorityQueue()
    p_queue.enqueue(
        start_block, f_cost[start_block]
    )  # initalize the queue with the start block

    while not p_queue.is_empty() and is_running():
        current: Block = p_queue.dequeue()

        if current.is_end_block():
            found = True
            break
        for neighbor in current.get_neighbors():
            if not neighbor.is_visited() and not neighbor.is_next():
                # since each block is next to each other,
                # the g cost of neighbor is simply 1 more than that of current
                g_temp = g_cost[current] + 1
                # since h cost is constant
                # f cost only varies based on g cost
                if g_temp < g_cost[neighbor]:
                    g_cost[neighbor] = g_temp
                    f_cost[neighbor] = g_temp + h_cost[neighbor]
                    neighbor.set_parent(current)
                    neighbor.set_next()
                    p_queue.enqueue(neighbor, f_cost[neighbor])
        current.set_visited()
        input_handling()

    if found:
        __backtrack(current.get_parent(), is_running)


def __get_heuristic(block: Block, end_pos: tuple) -> float:
    """
    Calculate the heuristic distance for a block
    """
    block_pos = block.get_position()
    x = abs(block_pos[0] - end_pos[0])
    y = abs(block_pos[1] - end_pos[1])
    return x + y


def __backtrack(root: Block, is_running) -> None:
    """
    Backtrack to highlight the shortest path
    Args:
        root (Block): the previous block visitted
    """
    while not root.is_start_block() and is_running:
        root.set_path()  # set the block to be part of the path
        root = root.get_parent()  # keep backtracking
