import pygame, random
from tkinter import Tk
from tkinter import messagebox
from visualizer import Visualizer
from pygame.constants import K_1, K_2, K_3, K_4
from data_structures import Queue, Stack, PriorityQueue


########### Global constants ##########
SIZE = 650                                  # size of the grid displayed on screen
BLOCKS_EACH_LINE = 50                       # number of blocks on each line
BLOCK_WIDTH = SIZE // BLOCKS_EACH_LINE      # width of each block
HALF_WIDTH = int(BLOCK_WIDTH / 2)           # 1/2 width of each block
WIN_W = SIZE + 330                          # width of the screen (extra 330 for text)
WIN_H = SIZE                                # height of the screen

START_POS = (6, 6)                                      # index for start block
END_POS = (BLOCKS_EACH_LINE - 7, BLOCKS_EACH_LINE - 7)  # index for end block

# colors
YELLOW = (244, 242, 140)
GREEN = (10, 225, 20)

looping = True     # keep the mainloop run


############################################
####### PATHFINDING VISUALIZER CLASS #######
#------------------------------------------#
# Create the GUI and visualize the path
# finding process for different algorithms
############################################

class PathfindingVisualizer(Visualizer):

    def __init__(self) -> None:
        ##### initialize variables #####
        global looping
        self.grid = []                  # the grid containing all the blocks 
        self.generated = False          # if random barriers are already generated
        self.pathfinder = None          # the pathfinder
        looping = True                  # keep the mainloop running

        ##### initialize the screen display #####
        super().__init__(WIN_W, WIN_H, 'Pathfinding Visualizer')
        self.__show_instruction_text()    # show the instruction text
        self.__create_blocks()            # create the blocks for the grid
        self.__mainloop()


    def __mainloop(self):
        while looping:
            super().draw() 
            self.__input_handling()    
                       

    # handle mouse and keyboard input from user
    def __input_handling(self):
        global looping
        # if the left mouse is pressed -> draw barrier
        if pygame.mouse.get_pressed() == (1,0,0):
            pos = pygame.mouse.get_pos()
            self.__update_block_clicked(pos, "barrier")
        # if the right mouse is pressed -> delete
        elif pygame.mouse.get_pressed() == (0,0,1):
            pos = pygame.mouse.get_pos()
            self.__update_block_clicked(pos, "walkable")

        for event in pygame.event.get():
            # click exit -> quit and return to menu
            if event.type == pygame.QUIT:
                looping = False
                pygame.display.quit()

            # If there is a Key pressed 
            elif event.type == pygame.KEYDOWN:

                # Esc Key -> quit and return to menu
                if event.key == pygame.K_ESCAPE:
                    looping = False
                    pygame.display.quit()

                # C -> reset the screen
                elif event.key == pygame.K_c:
                    self.__clear()

                # G -> randomly generate obstacles
                elif event.key == pygame.K_g and not self.generated:
                    self.generated = True
                    self.__generate_obstacles()

                # Return Key -> Start
                elif event.key == pygame.K_RETURN:
                    self.generated = True
                    # we check all the neighbors before we start the algorithm
                    self.__check_all_neighbors()
                    self.__start_finding()

                # number -> choose the corresponding searching algorithm
                else:
                    switch = {
                        K_1: 1,
                        K_2: 2,
                        K_3: 3,
                        K_4: 4
                    }
                    chosen = switch.get(event.key, -1)
                    self.__pick_algo(chosen)
 
            # If mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl + right click -> set start point
                    if event.button == 1:
                        self.__update_block_clicked(pos, "start")
                    # Ctrl + left click -> set end point
                    else:
                        self.__update_block_clicked(pos, "end")


    # create and add the blocks on the grid
    def __create_blocks(self):
        for i in range(BLOCKS_EACH_LINE):
            self.grid.append([])                    # make 2D array
            for j in range(BLOCKS_EACH_LINE):
                new_block = Block(self.screen, i, j)
                self.grid[i].append(new_block)      # add new block to the grid
        self.__init_start_end_points()              # iniitalize the start and end blocks


    # display the instruction text on the side of our grid 
    def __show_instruction_text(self):
        pos_y = 20
        self.font = pygame.font.SysFont('consolas', 16, bold=True)
        # the list of instructions to display
        instruction_list = [
            "Left Click: draw barrier",
            "Right Click: remove barrier",
            "Ctrl + Left Click: set start point",
            "Ctrl + Right Click: set end point",
            "G: generate random obstacle",
            "C: reset",
            "<Enter>: start finding path",
            "ESC: Exit visualizer",
            "", "",
            "CHOOSE SEARCH ALGORITHM",
            "press a corressponding number:",]
        # show all the instructions on the screen
        for string in instruction_list:
            text = self.font.render(string, False, GREEN)
            self.screen.blit(text, (SIZE + 10, pos_y))
            pos_y += 25
        ### display the list of algorithms to choose below the instruction text
        # list of algorithms' names
        self.algo_names = [
            "   1: A* algorithm",
            "   2: Dijkstra algorithm",
            "   3: Breadth First Search",
            "   4: Depth First Search"]
        self.algo_text = []     # rendered text for the algorithms names
        self.algo_pos_y = []    # y position for each algorithm text
        for i in range (0, len(self.algo_names)):
            self.algo_pos_y.append(pos_y)
            self.algo_text.append(self.font.render(self.algo_names[i], False, GREEN))
            self.screen.blit(self.algo_text[i], (SIZE + 10, self.algo_pos_y[i]))
            pos_y += 25
        # default algorithm is A star
        self.algo_picked = 1
        self.__pick_algo(1)


    # actions made when a user choose an algorithm
    def __pick_algo(self, n):
        if n != -1:
            # reset the previously chosen algorithm text to green
            self.algo_text[self.algo_picked - 1] = self.font.render(self.algo_names[self.algo_picked - 1], False, GREEN)
            self.screen.blit(self.algo_text[self.algo_picked - 1], (SIZE + 10, self.algo_pos_y[self.algo_picked - 1]))
            # set the newly chosen algorithm text to yellow
            self.algo_text[n - 1] = self.font.render(self.algo_names[n - 1], False, YELLOW)
            self.screen.blit(self.algo_text[n - 1], (SIZE + 10, self.algo_pos_y[n - 1]))
            # set the chosen algorithm
            self.algo_picked = n


    # get the block that was clicked and change its status
    def __update_block_clicked(self, pos, status):
        x, y = pos
        if x < SIZE and y < SIZE:
            x = x // BLOCK_WIDTH        # get the index of the block clicked
            y = y // BLOCK_WIDTH

            if ((x, y) != self.start_point and (x, y) != self.end_point):
                if status == "walkable":
                    self.grid[x][y].set_walkable()
                elif status == "barrier":
                    self.grid[x][y].set_barrier()
                elif status == "start":
                    if self.start_point != None:
                        i, j = self.start_point
                        self.grid[i][j].set_walkable()
                    self.start_point = (x, y)
                    self.grid[x][y].set_start()
                else:
                    if self.end_point != None:
                        i, j = self.end_point
                        self.grid[i][j].set_walkable()
                    self.end_point = (x, y)
                    self.grid[x][y].set_end()


    # reset the grids to initial state (no barriers, start and end blocks are at top and bottom)
    def __clear(self):
        self.generated = False
        # reset all the blocks on the screen
        for i in range(BLOCKS_EACH_LINE):
            for j in range(BLOCKS_EACH_LINE):
                self.grid[i][j].reset()
        # put the start and end blocks to default locations
        self.__init_start_end_points()

    
    # randomly generate barrier/obstacles on the grid
    def __generate_obstacles(self):
        # generate the barrier randomly
        for _ in range(SIZE * 4 // 3):
            rand_x = random.randint(0, BLOCKS_EACH_LINE - 1)
            rand_y = random.randint(0, BLOCKS_EACH_LINE - 1)
            if self.grid[rand_x][rand_y].is_walkable():
                self.grid[rand_x][rand_y].set_barrier()
        sx, sy = self.start_point
        ex, ey = self.end_point
        # clear out the blocks around the start and end blocks to guarantee the point won't be covered
        for i in range (-4, 4):
            for j in range (-4, 4):
                # make sure the index that we are going to clear is valid
                if sx+i >= 0 and sx+i <= BLOCKS_EACH_LINE-1 and sy+j >= 0 and sy+j <= BLOCKS_EACH_LINE-1:
                    if not self.grid[sx + i][sy + j].is_start_block():
                        self.grid[sx + i][sy + j].set_walkable()
                if ex+i >= 0 and ex+i <= BLOCKS_EACH_LINE-1 and ey+j >= 0 and ey+j <= BLOCKS_EACH_LINE-1:
                    if not self.grid[ex + i][ey + j].is_end_block():
                        self.grid[ex + i][ey + j].set_walkable()
    

    # put the start block to the top and the end block to the bottom of the screen
    def __init_start_end_points(self):
        self.start_point = START_POS
        self.end_point = END_POS
        self.grid[START_POS[0]][START_POS[1]].set_start()
        self.grid[END_POS[0]][END_POS[1]].set_end()
        

    # check the neighbors for each block on the grid
    def __check_all_neighbors(self):
        for i in range(BLOCKS_EACH_LINE):
            for j in range(BLOCKS_EACH_LINE):
                self.grid[i][j].update_neighbors(self.grid)

    
    ##################################
    # start the path finding process #
    def __start_finding(self):
        start_block = self.grid[self.start_point[0]][self.start_point[1]]
        switch = {
            1: lambda grid, start_block: a_star(grid, start_block),
            2: lambda grid, start_block: dijkstra(grid, start_block),
            3: lambda _, start_block: breadth_first(start_block),
            4: lambda _, start_block: depth_first(start_block)
        }
        switch.get(self.algo_picked)(self.grid, start_block)



########################################################################
########################### BLOCK CLASS ################################
# ---------------------------------------------------------------------#
# Represent a "pixel" on the map. Many of these blocks will make up our 
# map. Each block will have its own status such as visited, walkable, 
# barrier, etc. 
########################################################################

class Block():

    # we will use color to determine the status of the block
    PATH = LIGHT_BLUE = (89, 205, 225)     # the block is part of the shortest path
    START = PINK = (248, 133, 244)              # the block is the start point
    END = RED = (215, 17, 27)                   # the block is the end point
    BARRIER = DARK_BLUE = (31, 78, 110)         # the block is walkable
    WALKABLE = WHITE = (220, 220, 220)          # the block is a barrier       
    VISITED = LIGHT_YELLOW = (255, 205, 102)    # the block is already visited
    NEXT_TO_VISIT = ORANGE = (255, 178, 102)    # the block is the next one to be visited
    LIGHT_GREEN = (177, 235, 145)


    def __init__(self, screen, x, y) -> None:
        self.screen = screen        # root screen to dislay the block
        self.x, self.y = x, y       # row and column where the block is at
        self.neighbors = []         # the list of neighbors
        self.parent = None          # the parent of the block
        self.was_visited = False    # if the block is visited or not

        ### The actual position on the map (since each block has a width) ###
        self.pos_x , self.pos_y = (x * BLOCK_WIDTH) + HALF_WIDTH, (y * BLOCK_WIDTH) + HALF_WIDTH

        ### display the block ###
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_WIDTH]) # the size of the block
        self.rect = self.image.get_rect()                       # generate the block as a rectangle
        self.rect.center = [self.pos_x, self.pos_y]             # put the rectangle in its position
        self.set_walkable()                                     # the block's initial status is walkable


    def is_walkable(self):
        return self.color == self.WALKABLE

    def is_barrier(self):
        return self.color == self.BARRIER

    def is_visited(self):
        return self.color == self.VISITED or self.was_visited

    def is_start_block(self):
        return self.color == self.START

    def is_end_block(self):
        return self.color == self.END

    def get_row_col(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def get_neighbors(self):
        return self.neighbors

    def get_parent(self):
        return self.parent

    def reset(self):
        self.was_visited = False
        self.__update_status(self.WALKABLE)
        self.neighbors = []
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def set_visited(self):
        self.was_visited = True
        if self.is_walkable():
            self.__update_status(self.VISITED)

    def set_path(self):
        self.__update_status(self.PATH)

    def set_barrier(self):
        self.__update_status(self.BARRIER)

    def set_walkable(self):
        self.__update_status(self.WALKABLE)

    def set_start(self):
        self.__update_status(self.START)

    def set_end(self):
        self.__update_status(self.END)


    # update the color status for the block on the screen
    def __update_status(self, color_status):
        self.color = color_status                               # set the color_status
        pygame.draw.rect(self.screen, color_status, self.rect)  # draw the block with the new color
        
        if self.color is not self.WALKABLE: # if a block is updated as walkable, no expanding effect is needed
            pygame.display.update()         # otherwise, update each block at a time to show the expanding effect
        if color_status is self.PATH:
            pygame.time.delay(5)            # if a block is updated as path, slow the expanding effect down 


    # check the 4 directions (North, East, South, West) around the block
    # and add the neighbor block to this block's list of neighbors if qualified
    def update_neighbors(self, grid):
        # make sure the index does not go out of the array's range
        north_has_block = self.x > 0
        south_has_block = self.x < BLOCKS_EACH_LINE - 1
        west_has_block = self.y > 0
        east_has_block = self.y < BLOCKS_EACH_LINE - 1

        # check the neighbors in clock-wise order
        # if the block is not a barrier, then add it to the neighbor list
         # check north
        if north_has_block:
            if grid[self.x - 1][self.y].get_color() is not self.BARRIER:
                self.neighbors.append(grid[self.x - 1][self.y])
        # check east:
        if east_has_block:
            if grid[self.x][self.y + 1].get_color() is not self.BARRIER:
                 self.neighbors.append(grid[self.x][self.y + 1])
        # check south
        if south_has_block:
            if grid[self.x + 1][self.y].get_color() is not self.BARRIER:
                self.neighbors.append(grid[self.x + 1][self.y])
        # check west:
        if west_has_block:
            if grid[self.x][self.y - 1].get_color() is not self.BARRIER:
                self.neighbors.append(grid[self.x][self.y - 1])        
            


#######################################################################################
####################  P A T H F I N D I N G   A L G O R I T H M S  ####################
#######################################################################################


############################
#### DEPTH FIRST SEARCH ####

def depth_first(start_block):
    found = False
    stack = Stack()
    start_block.set_visited()
    stack.push(start_block)

    while not stack.is_empty() and looping:
        current: Block = stack.pop()
        if current.is_end_block():
            found = True
            break
        neighbor_list = current.get_neighbors()
        for neighbor in neighbor_list:
            if not neighbor.is_visited():
                neighbor.set_visited()
                neighbor.set_parent(current)
                stack.push(neighbor)
        __input_handling()
    if looping:
        if found:
            # backtrack to show the path
            __backtrack(current.get_parent())
        # if there's no path, display the information
        else:
            __path_not_found()


##############################
#### BREADTH FIRST SEARCH ####

def breadth_first(start_block):
    found = False
    queue = Queue()
    start_block.set_visited()
    queue.enqueue(start_block)

    while not queue.is_empty() and looping:
        current: Block = queue.dequeue()
        if current.is_end_block():
            found = True
            break
        neighbor_list = current.get_neighbors()
        for neighbor in neighbor_list:
            if not neighbor.is_visited():
                neighbor.set_visited()
                neighbor.set_parent(current)
                queue.enqueue(neighbor)
        __input_handling()
    if looping:
        if found:
            # backtrack to show the path
            __backtrack(current.get_parent())
        # if there's no path, then display the information
        else:
            __path_not_found()


############################
#### DIJKSTRA ALGORITHM ####

def dijkstra(grid, start_block):
    found = False
    prio_queue = PriorityQueue()
    # initially assign infinity to the distance from each block to start block
    dis = {block: (float('inf')) for row in grid for block in row}
    dis[start_block] = 0

    # add each block to the priority queue, the priority being the shortest distance
    for i in range(BLOCKS_EACH_LINE):
        for j in range(BLOCKS_EACH_LINE):
            cur = grid[i][j]
            prio_queue.enqueue(cur, dis[cur])

    # loop through the queue
    while not prio_queue.is_empty() and looping:
        current: Block = prio_queue.dequeue()
        # if the end block is found then stop
        if current.is_end_block():
            found = True
            break
        # else, set the current block to be visited
        current.set_visited()
        for neighbor in current.get_neighbors():
            if not neighbor.is_visited():
                neighbor.set_parent(current)
                # let temp be the distance from current to start plus the distance to the next neighbor
                temp = dis[current] + 1
                dis[neighbor] = min(temp, dis[neighbor])
    if looping:
        if found:
            __backtrack(current.get_parent())
        else:
            __path_not_found()


######################
#### A* ALGORITHM ####

def a_star(grid, start_pos):
    found = False
    if found:
        pass
    else:
        __path_not_found()

#########################################################################################

# backtracking to show the shortest path
def __backtrack(root: Block):
    while not root.is_start_block():
        root.set_path()
        root = root.get_parent()


# handle mouse and keyboard input when the pathfinding process is running
def __input_handling():
    global looping
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False
            pygame.display.quit()
        elif event.type == pygame.KEYDOWN:
            # Esc Key -> quit and return to menu
            if event.key == pygame.K_ESCAPE:
                looping = False
                pygame.display.quit()


# In case where there is no walkable path between start and end blocks,
# create a pop up message to inform the user
def __path_not_found():
    root = Tk()
    root.wm_withdraw()  # hide the tkinter window so only the pop up screen shows up
    messagebox.showinfo('', 'No valid Path available')
    root.destroy()



if __name__ == "__main__":
    PathfindingVisualizer()

# https://www.youtube.com/watch?v=JtiK0DOeI4A

# https://medium.com/@nicholas.w.swift/easy-dijkstras-pathfinding-324a51eeb0f
