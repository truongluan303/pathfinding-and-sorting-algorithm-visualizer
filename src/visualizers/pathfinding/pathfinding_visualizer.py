from __future__ import annotations

import random
from os import getcwd

import pygame
from pygame.constants import K_1
from pygame.constants import K_2
from pygame.constants import K_3
from pygame.constants import K_4

from . import BLOCK_WIDTH
from . import BLOCKS_EACH_LINE
from . import END_POS
from . import SIZE
from . import START_POS
from . import WIN_H
from . import WIN_W
from .block import Block
from .pathfinding_algorithms import a_star
from .pathfinding_algorithms import breadth_first
from .pathfinding_algorithms import depth_first
from .pathfinding_algorithms import dijkstra
from src.visualizers.base_visualizer import BaseVisualizer


# colors
BLACK = (0, 0, 0)
YELLOW = (244, 242, 140)
GREEN = (10, 225, 20)


class PathfindingVisualizer(BaseVisualizer):
    """
    The GUI to visualize the pathfinding process for different pathfinding algorithms
    """

    def __init__(self) -> None:
        ##### initialize variables #####
        self._grid = []  # the grid containing all the blocks
        self._cleared = True  # if the grid is cleared (all walkable)
        self._looping = True  # keep the mainloop running
        self._generated = False  # if random barriers are already generated

        ##### initialize the screen display #####
        icon_path = getcwd() + "/images/path_icon.ico"
        super().__init__(WIN_W, WIN_H, "Pathfinding Visualizer", BLACK, icon_path)
        self.__show_instruction_text()  # show the instruction text
        self.__create_blocks()  # create the blocks for the grid
        self.__mainloop()

    def __mainloop(self):
        while self._looping:
            super().draw()
            self.__input_handling()

    def __input_handling(self) -> None:
        """
        Handle mouse and keyboard input from user
        """
        # if the left mouse is pressed -> draw barrier
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos = pygame.mouse.get_pos()
            self.__update_block_clicked(pos, "barrier")
            self._cleared = False
        # if the right mouse is pressed -> delete
        elif pygame.mouse.get_pressed() == (0, 0, 1):
            pos = pygame.mouse.get_pos()
            self.__update_block_clicked(pos, "walkable")

        for event in pygame.event.get():
            # click exit -> quit and return to menu
            if event.type == pygame.QUIT:
                quit()

            # If there is a Key pressed
            elif event.type == pygame.KEYDOWN:

                # Esc Key -> quit and return to menu
                if event.key == pygame.K_ESCAPE:
                    quit()

                # C -> clear the grid
                elif event.key == pygame.K_c and not self._cleared:
                    self._generated = False
                    self._cleared = True
                    self.__clear()

                # G -> randomly generate obstacles
                elif event.key == pygame.K_r and not self._generated:
                    self._generated = True
                    self._cleared = False
                    self.__generate_obstacles()

                # Return Key -> Start
                elif event.key == pygame.K_RETURN:
                    self._generated = True
                    # Update the neighbors before running the algorithm
                    for row in self._grid:
                        for block in row:
                            block.update_neighbors(self._grid)
                    self.__start_finding()

                # number -> choose the corresponding algorithm
                else:
                    switch = {K_1: 1, K_2: 2, K_3: 3, K_4: 4}
                    chosen = switch.get(event.key, -1)
                    self.__pick_algo(chosen)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl + right click -> set start point
                    if event.button == 1:
                        self.__update_block_clicked(pos, "start")
                    # Ctrl + left click -> set end point
                    else:
                        self.__update_block_clicked(pos, "end")

    def __create_blocks(self) -> None:
        """
        create and add the blocks on the grid
        """
        # add new blocks
        for i in range(BLOCKS_EACH_LINE):
            self._grid.append([])
            for j in range(BLOCKS_EACH_LINE):
                # when the display is not fully initialized
                # no need to make expanding effect
                # so we set the effect to be False
                new_block = Block(self._screen, i, j, False)
                # add new block to the grid
                self._grid[i].append(new_block)
        # iniitalize the start and end blocks
        self.__init_start_end_points()

    def __show_instruction_text(self) -> None:
        """
        Display the instruction text on the right side of the grid
        """
        pos_y = 20
        self.font = pygame.font.SysFont("consolas", 16, bold=True)

        # the list of instructions to display
        instruction_list = [
            "Left Click: Draw Barrier",
            "Right Click: Remove Barrier",
            "Ctrl + Left Click: Set Start Point",
            "Ctrl + Right Click: Set End Point",
            "R: Generate Random Obstacle",
            "C: reset",
            "<Enter>: Start Finding Path",
            "ESC: Exit visualizer",
            "",
            "",
            "CHOOSE SEARCH ALGORITHM",
            "press a corressponding number:",
        ]

        # show all the instructions on the screen
        for string in instruction_list:
            text = self.font.render(string, False, GREEN)
            self._screen.blit(text, (SIZE + 10, pos_y))
            pos_y += 25

        ### display the list of algorithms to choose below the instruction text

        # list of algorithms' names
        self.algo_names = [
            "   1: A* algorithm",
            "   2: Dijkstra algorithm",
            "   3: Breadth First Search",
            "   4: Depth First Search",
        ]

        self.algo_text = []  # rendered text for the algorithms names
        self.algo_pos_y = []  # y position for each algorithm text

        for i in range(0, len(self.algo_names)):
            self.algo_pos_y.append(pos_y)
            self.algo_text.append(self.font.render(self.algo_names[i], False, GREEN))
            self._screen.blit(self.algo_text[i], (SIZE + 10, self.algo_pos_y[i]))
            pos_y += 25

        # default algorithm is A star
        self.algo_picked = 1
        self.__pick_algo(1)

    def __pick_algo(self, n: int) -> None:
        """
        Action made when the user chooses an algorithm to visualize
        Args:
            n (int): the number associated to the algorithm
        """
        if n != -1:
            # reset the previously chosen algorithm text to green
            self.algo_text[self.algo_picked - 1] = self.font.render(
                self.algo_names[self.algo_picked - 1], False, GREEN
            )
            self._screen.blit(
                self.algo_text[self.algo_picked - 1],
                (SIZE + 10, self.algo_pos_y[self.algo_picked - 1]),
            )

            # set the newly chosen algorithm text to yellow
            self.algo_text[n - 1] = self.font.render(
                self.algo_names[n - 1], False, YELLOW
            )
            self._screen.blit(
                self.algo_text[n - 1], (SIZE + 10, self.algo_pos_y[n - 1])
            )

            # set the chosen algorithm
            self.algo_picked = n

    def __update_block_clicked(self, pos: tuple, status: str) -> None:
        """
        Get the block that was clicked and change its status
        Args:
            pos (tuple): position of the block
            status (str): the status to be changed to
        """
        x, y = pos
        if x < SIZE and y < SIZE:
            # get the index of the block clicked
            x = x // BLOCK_WIDTH
            y = y // BLOCK_WIDTH

            if (x, y) != self.start_point and (x, y) != self.end_point:
                if status == "walkable":
                    self._grid[x][y].set_walkable()
                elif status == "barrier":
                    self._grid[x][y].set_barrier()
                elif status == "start":
                    if self.start_point != None:
                        i, j = self.start_point
                        self._grid[i][j].set_walkable()
                    self.start_point = (x, y)
                    self._grid[x][y].set_start()
                else:
                    if self.end_point != None:
                        i, j = self.end_point
                        self._grid[i][j].set_walkable()
                    self.end_point = (x, y)
                    self._grid[x][y].set_end()

    def __clear(self) -> None:
        """
        Reset the grids to its initial state
        """
        # reset all the blocks on the screen
        for i in range(BLOCKS_EACH_LINE):
            for j in range(BLOCKS_EACH_LINE):
                self._grid[i][j].reset()
        # put the start and end blocks to default locations
        self.__init_start_end_points()

    def __generate_obstacles(self) -> None:
        """
        Randomly generate the obstacles on the grid
        """
        # generate the obstacles randomly
        for _ in range(SIZE * 4 // 3):
            rand_x = random.randint(0, BLOCKS_EACH_LINE - 1)
            rand_y = random.randint(0, BLOCKS_EACH_LINE - 1)
            if self._grid[rand_x][rand_y].is_walkable():
                self._grid[rand_x][rand_y].set_barrier()
        sx, sy = self.start_point
        ex, ey = self.end_point

        # clear the blocks around the start and end blocks so the they won't be covered
        for i in range(-4, 4):
            for j in range(-4, 4):
                # make sure the index that we are going to clear is in the valid range
                if sx + i >= 0 and sx + i <= BLOCKS_EACH_LINE - 1:
                    if sy + j >= 0 and sy + j <= BLOCKS_EACH_LINE - 1:
                        if not self._grid[sx + i][sy + j].is_start_block():
                            if not self._grid[sx + i][sy + j].is_end_block():
                                self._grid[sx + i][sy + j].set_walkable()
                if ex + i >= 0 and ex + i <= BLOCKS_EACH_LINE - 1:
                    if ey + j >= 0 and ey + j <= BLOCKS_EACH_LINE - 1:
                        if not self._grid[ex + i][ey + j].is_start_block():
                            if not self._grid[ex + i][ey + j].is_end_block():
                                self._grid[ex + i][ey + j].set_walkable()

    def __init_start_end_points(self) -> None:
        """
        Put the start and end blocks to their default locations
        """
        self.start_point = START_POS
        self.end_point = END_POS
        self._grid[START_POS[0]][START_POS[1]].set_start()
        self._grid[END_POS[0]][END_POS[1]].set_end()

    def __start_finding(self) -> None:
        """
        Start the pathfinind process
        """
        self._cleared = False
        start_block = self._grid[self.start_point[0]][self.start_point[1]]

        def input_handling() -> None:
            """
            Handle mouse and keyboard input when the pathfininding process is running
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    # Esc Key -> quit and return to menu
                    if event.key == pygame.K_ESCAPE:
                        self._looping = False
                        pygame.display.quit()

        if self.algo_picked == 1:
            a_star(
                self._grid,
                start_block,
                self.end_point,
                input_handling,
                lambda: self._looping,
            )
        elif self.algo_picked == 2:
            dijkstra(self._grid, start_block, input_handling, lambda: self._looping)
        elif self.algo_picked == 3:
            breadth_first(start_block, input_handling, lambda: self._looping)
        elif self.algo_picked == 4:
            depth_first(start_block, input_handling, lambda: self._looping)
        else:
            raise Exception("Invalid Algorithm Choice!")
