import pygame, random
from tkinter import Tk
from tkinter import messagebox
from data_structures import LinkedQueue, LinkedStack

SIZE = 660
BLOCKS_EACH_LINE = 60
BLOCK_WIDTH = SIZE // BLOCKS_EACH_LINE
HALF_WIDTH = int(BLOCK_WIDTH / 2)

GRAY = (140, 160, 190)
YELLOW = (244, 242, 140)
GREEN = (10, 225, 20)



############################################
####### PATHFINDING VISUALIZER CLASS #######
#------------------------------------------#
# Create the GUI and visualize the path
# finding process for different algorithms
############################################

class PathfindingVisualizer:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Pathfinding Visualizer')        
        self.screen = pygame.display.set_mode((SIZE + 330, SIZE))   
        self.looping = True     # keep the mainloop run
        self.started = False    # if the user started to find path
        self.generated = False  # if random barriers are already generated
        self.pathfinder = None  # the pathfinder
        self.__create_blocks()          # create the blocks for the grid
        self.__show_instruction_text()  # show the instruction text
        self.__mainloop()              # main loop


    def __mainloop(self):
        while self.looping:
            self.__draw()    
            self.__input_handling()    
                       

    # handle mouse and keyboard input from user
    def __input_handling(self):
        if not self.started:
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
                self.looping = False
                pygame.display.quit()

            # If there is a Key pressed 
            elif event.type == pygame.KEYDOWN:
                # Esc Key -> quit and return to menu
                if event.key == pygame.K_ESCAPE:
                    self.looping = False
                    pygame.display.quit()
                
                # C -> reset the screen
                elif event.key == pygame.K_c:
                    self.__clear()
                
                elif not self.started:
                    # G -> randomly generate obstacles
                    if event.key == pygame.K_g and not self.generated:
                        self.generated = True
                        self.__generate_obstacles()

                    # number -> choose the corresponding searching algorithm
                    elif event.key == pygame.K_1:
                        self.__pick_algo(1)
                    elif event.key == pygame.K_2:
                        self.__pick_algo(2)
                    elif event.key == pygame.K_3:
                        self.__pick_algo(3)
                    elif event.key == pygame.K_4:
                        self.__pick_algo(4)
                    
                    # Return Key -> Start
                    elif event.key == pygame.K_RETURN:
                        # we check all the neighbors before we start the algorithm
                        self.started = True
                        self.__check_all_neighbors()
                        self.__start_finding()
 
            # If mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.started:
                pos = pygame.mouse.get_pos()
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl + right click -> set start point
                    if event.button == 1:
                        self.__update_block_clicked(pos, "start")
                    # Ctrl + left click -> set end point
                    else:
                        self.__update_block_clicked(pos, "end")
                

    # draw the components on the screen
    def __draw(self):
        pygame.display.update() 
        pygame.display.flip()
        self.clock.tick(60)


    # create and add the blocks on the grid
    def __create_blocks(self):
        self.grid = []
        for i in range(BLOCKS_EACH_LINE):
            self.grid.append([]) # make 2D array
            for j in range(BLOCKS_EACH_LINE):
                new_block = Block(self.screen, i, j)
                self.grid[i].append(new_block)
        self.__init_start_end_points()


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
            x = x // BLOCK_WIDTH
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
        self.started = False
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
        # clear out the blocks around the start and end blocks to guarantee a path can be found
        sx, sy = self.start_point
        ex, ey = self.end_point
        for i in range (-4, 4):
            for j in range (-4, 4):
                if sx+i >= 0 and sx+i <= BLOCKS_EACH_LINE-1 and sy+j >= 0 and sy+j <= BLOCKS_EACH_LINE-1:
                    if not self.grid[sx + i][sy + j].is_start_block():
                        self.grid[sx + i][sy + j].set_walkable()
                if ex+i >= 0 and ex+i <= BLOCKS_EACH_LINE-1 and ey+j >= 0 and ey+j <= BLOCKS_EACH_LINE-1:
                    if not self.grid[ex + i][ey + j].is_end_block():
                        self.grid[ex + i][ey + j].set_walkable()
    

    # put the start block to the top and the end block to the bottom of the screen
    def __init_start_end_points(self):
        self.start_point = (0, 0)
        self.end_point = (BLOCKS_EACH_LINE - 1, BLOCKS_EACH_LINE - 1)
        self.grid[0][0].set_start()
        self.grid[BLOCKS_EACH_LINE - 1][BLOCKS_EACH_LINE - 1].set_end()
        

    # check the neighbors for each block on the grid
    def __check_all_neighbors(self):
        for i in range(BLOCKS_EACH_LINE):
            for j in range(BLOCKS_EACH_LINE):
                self.grid[i][j].update_neighbors(self.grid)

    
    ##################################
    # start the path finding process #
    def __start_finding(self):
        x, y = self.start_point
        self.pathfinder = PathFinder(self.grid[x][y])
        if self.algo_picked == 1:
            self.pathfinder.a_star()
        elif self.algo_picked == 2:
            self.pathfinder.dijkstra()
        elif self.algo_picked == 3:
            self.pathfinder.breadth_first()
        else:
            self.pathfinder.depth_first()






########################################################################
########################### BLOCK CLASS ################################
# ---------------------------------------------------------------------#
# Represent a "pixel" on the map. Many of these blocks will make up our 
# map. Each block will have its own status such as visited, walkable, 
# barrier, etc. 
########################################################################

class Block():

    # we will use color to determine the status of the block
    SHORTEST_PATH = LIGHT_BLUE = (89, 205, 225)     # the block is part of the shortest path
    START = PINK = (248, 133, 244)                  # the block is the start point
    END = RED = (215, 17, 27)                       # the block is the end point
    BARRIER = DARK_BLUE = (31, 78, 110)             # the block is walkable
    WALKABLE = WHITE = (220, 220, 220)              # the block is a barrier       
    VISITED = LIGHT_YELLOW = (255, 205, 102)        # the block is already visited
    NEXT_TO_VISIT = LIGHT_ORANGE = (255, 178, 102)  # the block is the next one to be visited
    LIGHT_GREEN = (177, 235, 145)


    def __init__(self, screen, x, y) -> None:
        self.screen = screen
        # row and column where the block is at
        self.x, self.y = x, y
        # The actual position on the map (since each block has a width)
        self.pos_x , self.pos_y = (x * BLOCK_WIDTH) + HALF_WIDTH, (y * BLOCK_WIDTH) + HALF_WIDTH
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_WIDTH])
        self.was_visited = False
        # the list of neighbors. Most blocks will have 4 neighbors including up, down, right, left.
        self.neighbors = []
        self.parent = None
        # display the block 
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]
        self.set_walkable()  # initial status is walkable


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

    def set_parent(self, parent):
        self.parent = parent

    def reset(self):
        self.was_visited = False
        self.__update_status(self.WALKABLE)
        self.neighbors = []

    def set_visited(self):
        self.was_visited = True
        if self.is_walkable():
            self.__update_status(self.VISITED)

    def set_shortest_path(self):
        self.__update_status(self.SHORTEST_PATH)

    def set_barrier(self):
        self.__update_status(self.BARRIER)

    def set_walkable(self):
        self.__update_status(self.WALKABLE)

    def set_start(self):
        self.__update_status(self.START)

    def set_end(self):
        self.__update_status(self.END)


    def __update_status(self, color_status):
        self.color = color_status
        self.image.fill(color_status)
        pygame.draw.rect(self.screen, color_status, self.rect)
        if color_status is not self.WALKABLE:
            if color_status is self.SHORTEST_PATH:
                pygame.time.delay(5)
            pygame.display.update()


    # check the 4 sides (North, East, South, West) around the block
    # and add the neighbor block to this block list of neighbors if qualified
    def update_neighbors(self, grid):
        north_has_block = self.x > 0
        south_has_block = self.x < BLOCKS_EACH_LINE - 1
        west_has_block = self.y > 0
        east_has_block = self.y < BLOCKS_EACH_LINE - 1
        ######## Check the neighbors in clock wise order #########
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

            

####################################################################
####################### PATH FINDER CLASS ##########################
#------------------------------------------------------------------#
# This class will perform the finding algorithms to look for the 
# path between the start and end points
####################################################################

class PathFinder:

    def __init__(self, start_block) -> None:
        self.start_block = start_block

    
    #################################################
    #### use depth first search to find the path ####
    def depth_first(self):
        found = False
        stack = LinkedStack[Block]()
        self.start_block.set_visited()
        stack.push(self.start_block)

        while not stack.is_empty():
            current = stack.pop()
            if current.is_end_block():
                found = True
                break
            neighbor_list = current.get_neighbors()
            for neighbor in neighbor_list:
                if not neighbor.is_visited():
                    neighbor.set_visited()
                    neighbor.set_parent(current)
                    stack.push(neighbor)
        # backtrack to show the path if there is one
        if found:
            parent = current.get_parent()
            while not parent.is_start_block():
                parent.set_shortest_path()
                parent = parent.get_parent()
        # if there's no path, display the information
        else:
            self.__path_not_found()


    ############################################################
    #### use breadth first search to find the shortest path ####
    def breadth_first(self):
        found = False
        queue = LinkedQueue[Block]()
        self.start_block.set_visited()
        queue.enqueue(self.start_block)

        while not queue.is_empty():
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
        # backtrack to show the path if there is one
        if found:
            parent = current.get_parent()
            while not parent.is_start_block():
                parent.set_shortest_path()
                parent = parent.get_parent()
        # if there's no path, then display the information
        else:
            self.__path_not_found()


    ############################################################
    #### use dijkstra algorithm to search for shortest path ####
    def dijkstra(self):
        found = False


    ###########################################################
    #### use a start algorithm to search for shortest path ####
    def a_star(self):
        found = False


    # In case where there is no walkable path between start and end blocks    
    # we will create a pop up message to inform the user
    def __path_not_found(self):
        root = Tk()
        root.wm_withdraw()
        x = messagebox,messagebox.showinfo('', 'Path not found!')
        root.destroy()



if __name__ == "__main__":
    PathfindingVisualizer()

# https://www.youtube.com/watch?v=JtiK0DOeI4A