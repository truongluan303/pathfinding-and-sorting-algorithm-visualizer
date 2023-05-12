from __future__ import annotations

from enum import Enum

import pygame

from . import BLOCK_WIDTH
from . import BLOCKS_EACH_LINE
from . import HALF_WIDTH


class Block:
    """
    Represents a node on the map. The map will be made up of multiple blocks.
    Each block will have a status, which is also its color.
    """

    class ColorStatus(Enum):
        """
        Represents the status/color of the block.
        """

        PATH = (89, 205, 225)  # is part of the shortest path
        START = (248, 133, 244)  # is the start point
        END = (215, 17, 27)  # is the end point
        BARRIER = (31, 78, 110)  # is walkable
        WALKABLE = (220, 220, 220)  # is a barrier
        VISITED = (255, 205, 102)  # is already visited
        NEXT_TO_VISIT = (195, 255, 105)  # is in the waitlist to be visited

    def __init__(self, screen, x, y, effect=True) -> None:
        """
        Args:
            screen ([type]): the screen where the block will be placed on
            x ([type]): the x-coordinate of the block
            y ([type]): the y-coordinate of the block
            effect (bool, optional): true to make the expanding effect (defaults to True)
        """
        self._screen = screen  # root screen to dislay the block
        self.x, self.y = x, y  # row and column index where the block is at
        self.neighbors = []  # the list of neighbors
        self.parent = None  # the parent of the block
        self.was_visited = False  # if the block is visited or not

        ### The actual position on the map (since each block has a width) ###
        self.pos_x = (x * BLOCK_WIDTH) + HALF_WIDTH
        self.pos_y = (y * BLOCK_WIDTH) + HALF_WIDTH

        ### display the block ###
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_WIDTH])  # the size of the block
        self.rect = self.image.get_rect()  # generate the block as a rectangle
        self.rect.center = [self.pos_x, self.pos_y]  # put the rectangle in its position
        self.__update_status(
            self.ColorStatus.WALKABLE, effect
        )  # initial status is walkable

    def is_walkable(self) -> bool:
        return self.color == self.ColorStatus.WALKABLE

    def is_barrier(self) -> bool:
        return self.color == self.ColorStatus.BARRIER

    def is_next(self) -> bool:
        return self.color == self.ColorStatus.NEXT_TO_VISIT

    def is_visited(self) -> bool:
        return self.color == self.ColorStatus.VISITED or self.was_visited

    def is_start_block(self) -> bool:
        return self.color == self.ColorStatus.START

    def is_end_block(self) -> bool:
        return self.color == self.ColorStatus.END

    def get_position(self) -> tuple[int]:
        return self.x, self.y

    def get_color(self) -> tuple[int]:
        return self.color

    def get_neighbors(self) -> list[Block]:
        return self.neighbors

    def get_parent(self) -> Block:
        return self.parent

    def __update_status(self, color_status: ColorStatus, effect=True) -> None:
        """
        Update the color status for the block
        Args:
            color_status ([type]): the new color of the block
            effect (bool, optional): true to make the expanding effect (defaults to True)
        """
        self.color = color_status  # set the color_status
        pygame.draw.rect(
            self._screen, color_status.value, self.rect
        )  # draw block with new color

        # make the expanding effect
        if effect:
            pygame.display.update()
        if color_status is self.ColorStatus.PATH:
            pygame.time.delay(5)  # if a block is path, slow the expanding effect down

    def set_path(self) -> None:
        """
        Set the status of the current block to be a part of the path
        """
        self.__update_status(self.ColorStatus.PATH)

    def set_barrier(self) -> None:
        """
        Set the status of the current block to be an obstacle/barrier
        """
        self.__update_status(self.ColorStatus.BARRIER)

    def set_walkable(self) -> None:
        """
        Set the current block's status to be walkable
        """
        self.__update_status(self.ColorStatus.WALKABLE)

    def set_start(self) -> None:
        """
        Set the current block to be the start block
        """
        self.__update_status(self.ColorStatus.START)

    def set_end(self) -> None:
        """
        Set the current block to be the end block
        """
        self.__update_status(self.ColorStatus.END)

    def set_next(self) -> None:
        """
        Set the status to be the next block
        """
        if self.is_walkable():
            self.__update_status(self.ColorStatus.NEXT_TO_VISIT)

    def set_parent(self, parent) -> None:
        """
        Set the parent block for the current block
        """
        self.parent = parent

    def set_visited(self) -> None:
        """
        Set the status to be visited
        """
        self.was_visited = True
        if self.is_walkable() or self.is_next():
            self.__update_status(self.ColorStatus.VISITED)

    def reset(self) -> None:
        """
        Reset the block
        """
        self.__update_status(self.ColorStatus.WALKABLE, False)
        self.was_visited = False
        self.neighbors = []
        self.parent = None

    def update_neighbors(self, grid) -> None:
        """
        Check the 4 directions (N, E, S, W) around the block and add the neighbor
        block to this block's list of neighbors if qualified
        Args:
            grid ([type]): the grid containing all blocks
        """
        # make sure the index does not go out of the array's range
        north_has_block = self.x > 0
        south_has_block = self.x < BLOCKS_EACH_LINE - 1
        west_has_block = self.y > 0
        east_has_block = self.y < BLOCKS_EACH_LINE - 1

        # check the neighbors in clock-wise order
        # if the block is not a barrier, then add it to the neighbor list
        # check north
        if north_has_block:
            if not grid[self.x - 1][self.y].is_barrier():
                self.neighbors.append(grid[self.x - 1][self.y])
        # check east:
        if east_has_block:
            if not grid[self.x][self.y + 1].is_barrier():
                self.neighbors.append(grid[self.x][self.y + 1])
        # check south
        if south_has_block:
            if not grid[self.x + 1][self.y].is_barrier():
                self.neighbors.append(grid[self.x + 1][self.y])
        # check west:
        if west_has_block:
            if not grid[self.x][self.y - 1].is_barrier():
                self.neighbors.append(grid[self.x][self.y - 1])
