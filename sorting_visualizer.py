import pygame
from random import randint
from visualizer import Visualizer
from pygame.constants import K_1, K_2, K_3, K_4, K_5
from pygame.font import SysFont

BAR_WIDTH = 2
NUM_OF_BARS = 500
SCREEN_BORDER = 10
SCREEN_W = BAR_WIDTH * NUM_OF_BARS
SCREEN_H = NUM_OF_BARS
SHIFT_DOWN = 150
NUM_OG_ALGOS = 5

WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (244, 242, 30)
GREEN = (10, 225, 20)
RED = (255, 0 , 0)

font = None
looping = True          # keep the mainloop run
sorted = False          # check if the bar list is already sorted
stop_sorting = False    # check whether to stop the sorting process without quitting


#############################################################################
######################### SORTING VISUALIZER CLASS ##########################
# create the GUI and visualize the sorting process for different algorithms #
#---------------------------------------------------------------------------#
class SortingVisualizer(Visualizer):

    def __init__(self) -> None:
        super().__init__(SCREEN_W, SCREEN_H + SHIFT_DOWN, 
                        'Sorting Algorithms Visualizer', BLACK)
        #######  initialize variables  #######
        global looping, bar_list, font, bar_color, sorted, stop_sorting
        font = SysFont('consolas', 16, bold=True)       # the text font
        self.algo_text_colors = [GREEN] * NUM_OG_ALGOS  # generate the bars' colors
        self.bar_list = None                            # list of bars to display
        self.bar_color = None                           # the color for each bar
        self.algo = 1    
        looping = True         
        sorted = False         
        #######  get the visualizer run  #######
        self.__choose_algo(1)
        self.__shuffle()
        self.__mainloop()

    #
    # looping to show the display
    #
    def __mainloop(self):
        while looping:
            super().draw()
            self.__input_handling()

    #
    # handle keyboard and mouse input for the sorting begins
    #
    def __input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                # ESC -> back to menu screen
                if event.key == pygame.K_ESCAPE:
                    quit()
                # C -> shuffle
                elif event.key == pygame.K_c:
                    self.__shuffle()
                # Enter -> start sort
                elif event.key == pygame.K_RETURN and not sorted:
                    self.__start()
                else:
                    switch = {K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5}
                    self.__choose_algo(switch.get(event.key, -1))

    #
    # create the text instruction on top of the screen
    #
    def __create_instruction(self):
        y = 30
        pos_x1 = 700
        self.pos_x2 = 30
        self.pos_y = []
        display_text(self.screen, "C: Shuffle", pos_x1, 10)
        display_text(self.screen, "<Enter>: Start", pos_x1, 30)
        display_text(self.screen, "ESC: Exit visualizer", pos_x1, 50)
        display_text(self.screen, "Press a corresponding number " 
                     "to choose algorithm", self.pos_x2, 10)

        # create the algorithm names for the user to choose
        self.algo_names = ["1. Merge Sort", "2. Quick Sort", "3. Insertion Sort",
                           "4. Selection Sort", "5. Bubble Sort"]
        for i in range(NUM_OG_ALGOS):
            self.pos_y.append(y)
            display_text(self.screen, self.algo_names[i], 
                        self.pos_x2, y, self.algo_text_colors[i])
            y += 20

    #
    # pick the algorithm to run
    #
    def __choose_algo(self, chosen):
        if chosen != -1:
            self.algo_text_colors[self.algo-1] = GREEN  # unhighlight the previously chosen
            self.algo = chosen                          # set the newly chosen one
            self.algo_text_colors[chosen-1] = YELLOW    # highlight the newly chosen one
            self.__create_instruction()                 # update the display
            
        
    #
    # shuffle the bars
    #
    def __shuffle(self):
        global sorted
        self.bar_list = list(range(1, NUM_OF_BARS+1))   # generate the bars
        sorted = False                                  # set unsorted
        self.bar_color = [WHITE] * NUM_OF_BARS          # reset bar colors
        for i in range(NUM_OF_BARS):
            rand = randint(0, NUM_OF_BARS - 1)      # generate a random index
            swap_bars(self.bar_list, i, rand)            # swap to shuffle

        # update the screen display after shuffling
        show_bars(self.screen, self.bar_list, self.bar_color)   # show the bar list
        self.__create_instruction()                             # show the text


    #################
    # start sorting
    #
    def __start(self):
        global sorted, stop_sorting
        sorted = True
        stop_sorting = False 
        switcher = {
            1: lambda screen, bar_list, bar_color: 
                merge_sort(screen, bar_list, bar_color),
            2: lambda screen, bar_list, bar_color: 
                quick_sort(screen, bar_list, bar_color),
            3: lambda screen, bar_list, bar_color: 
                insertion_sort(screen, bar_list, bar_color),
            4: lambda screen, bar_list, bar_color: 
                selection_sort(screen, bar_list, bar_color),
            5: lambda screen, bar_list, bar_color: 
                bubble_sort(screen, bar_list, bar_color)
        }
        # use the algorithm corresponding to the number chosen
        switcher.get(self.algo)(self.screen, self.bar_list, self.bar_color)

        # refresh the screen display
        if looping:
            show_bars(self.screen, self.bar_list, self.bar_color)
            self.__create_instruction()
            pygame.display.update()

        # if the bars are all sorted, we add the running effect
        if looping and not stop_sorting:
            for i in range(NUM_OF_BARS):
                self.bar_color[i] = YELLOW
                pygame.time.delay(1)
                # update the display
                show_bars(self.screen, self.bar_list, self.bar_color)
                self.__create_instruction()
                pygame.display.update()
        

####################  end of Sorting Visualizer Class  ####################
###########################################################################

#
# display the text on the screen
#
def display_text(screen, string, pos_x, pos_y, color=GREEN):
    text = font.render(string, False, color)
    screen.blit(text, (pos_x, pos_y))

#
# swap two bars
#
def swap_bars(arr, idx1, idx2):
    # swap the element in the array
    temp = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = temp

#
# since we cannot clear a specific object on the pygame display, 
# we must clear the screen and re-display the bar list to show the changes on the list
#
def show_bars(screen, bar_list, bar_color):
    screen.fill(BLACK)
    for i in range(len(bar_list)):
        __create_bar(screen, bar_list[i], i, bar_color[i])
                
#
# quit the visualizer and go back to menu screen
#
def quit():
    global looping, stop_sorting
    looping = False
    stop_sorting = True
    pygame.display.quit()

#
# display instruction text when the sorting process already begins
#
def __show_running_instruction(screen):
    if not stop_sorting and looping:
        display_text(screen, 'ECS: Exit visualizer', 30, 10)
        display_text(screen, 'C: Stop sorting', 30, 30)

#
# create the a bar with specific characteristics
#
def __create_bar(screen, value, index, color):
    pos_x = index * BAR_WIDTH + BAR_WIDTH
    pos_y = SCREEN_H + SHIFT_DOWN
    height = value
    # generate the bar with the desired characteristics
    image = pygame.Surface([BAR_WIDTH, height])
    rect = image.get_rect()                             
    rect.bottomright = [pos_x, pos_y]               
    pygame.draw.rect(screen, color, rect)

#
# handle keyboard and mouse input after the sorting begins
#
def __input_handling():
    global stop_sorting, sorted
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            # C -> stop sorting
            elif event.key == pygame.K_c:
                stop_sorting = True
                sorted = False

#
# update the screen display
# including update the bar list display, the text display, and handle input
#
def __update_display(screen, bar_list, bar_color):
    if looping:
        show_bars(screen, bar_list, bar_color)
        __show_running_instruction(screen)
        pygame.display.update()
        __input_handling()


#######################################################################################
######################### S O R T I N G   A L G O R I T H M S #########################
#######################################################################################


######################### SELECTION SORT #########################

def selection_sort(screen, array, bar_color):
    for i in range (0, len(array)):
        min = array[i]
        for j in range (i, len(array)):
            if not stop_sorting:
                bar_color[i] = GREEN
                bar_color[j] = RED
                # if a new minimum is found then swap the old min and the new value
                if array[j] < min:
                    temp = min
                    min = array[j]
                    array[j] = temp
                    array[i] = min
                __update_display(screen, array, bar_color)           
            bar_color[j] = WHITE
            bar_color[i] = WHITE
            

######################### BUBBLE SORT #############################

def bubble_sort(screen, array, bar_color):
    for i in range (0, len(array)):
        for j in range (0, len(array) - i - 1):
            if not stop_sorting:
                bar_color[j] = RED
                bar_color[len(array) - i - 1] = GREEN
                # compare the elements by pair
                if array[j] > array[j + 1]:
                    # swap to correct the order
                    swap_bars(array, j, j + 1)
                    # show bars on display
                    __update_display(screen, array, bar_color)
                bar_color[len(array) - i - 1] = WHITE
                bar_color[j] = WHITE


########################## INSERTION SORT ############################

def insertion_sort(screen, arr, bar_color):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >= 0 and key < arr[j] and not stop_sorting:
            bar_color[i] = GREEN
            bar_color[j] = RED
            arr[j + 1] = arr[j]
            j -= 1
            # display the bars      
            __update_display(screen, arr, bar_color)
            bar_color[j + 1] = WHITE
            bar_color[NUM_OF_BARS - 1] = WHITE
        arr[j + 1] = key
        bar_color[i] = WHITE


############################# MERGE SORT ##########################

def merge_sort(screen, arr, bar_color):
    __merge_sort(screen, arr, bar_color, 0, len(arr)-1)

def __merge_sort(screen, arr, bar_color, begin, end):
    if begin < end and not stop_sorting:
        # find the mid point
        mid = (begin + end) // 2
        # keeps dividing the chunks in halves
        __merge_sort(screen, arr, bar_color, begin, mid)
        __merge_sort(screen, arr, bar_color, mid + 1, end)
        # merge the halves together
        l = begin
        r = mid + 1
        left_lim = mid
        right_lim = end
        temp = []

        # merge process
        while l <= left_lim and r <= right_lim:
            if stop_sorting:
                break
            # compare and put the smaller values in first
            if arr[l] < arr[r]:
                # update the display
                bar_color[l] = GREEN
                temp.append(arr[l])
                pygame.time.delay(1)
                __update_display(screen, arr, bar_color)
                bar_color[l] = WHITE
                l += 1
            else:
                # update the display
                bar_color[r] = GREEN
                temp.append(arr[r])
                pygame.time.delay(1)
                __update_display(screen, arr, bar_color)
                bar_color[r] = WHITE
                r += 1

        # adding the leftover from the left subarray
        while l <= left_lim:
            if stop_sorting:
                break
            bar_color[l] = GREEN
            pygame.time.delay(3)
            bar_color[l] = WHITE
            # add to the array
            temp.append(arr[l])
            __update_display(screen, arr, bar_color)
            l += 1

        # adding the leftover from the right subarray
        while r <= right_lim:
            if stop_sorting:
                break
            # update the display
            bar_color[r] = GREEN
            pygame.time.delay(3)
            bar_color[r] = WHITE
            # add to the array
            temp.append(arr[r])
            __update_display(screen, arr, bar_color)
            r += 1

        i, j = begin, 0
        # copy the temp to the array
        if not stop_sorting:
            while i < right_lim + 1:
                # update the display
                bar_color[i] = RED
                arr[i] = temp[j]
                pygame.time.delay(3)
                __update_display(screen, arr, bar_color)
                bar_color[i] = WHITE
                i += 1
                j += 1



############################# QUICK SORT ############################

# helper function
def quick_sort(screen, arr, bar_color):
    __quick_sort(screen, arr, bar_color, 0, len(arr)-1)


def __quick_sort(screen, arr, bar_color, begin, end):
    if (begin < end):
        pivot = arr[end]
        j = begin - 1

        for i in range (begin, end):
            if not stop_sorting:
                bar_color[i] = RED
                bar_color[j] = GREEN
                if arr[i] < pivot:
                    bar_color[j] = WHITE
                    # increase j
                    j += 1
                    bar_color[j] = GREEN
                    # then swap arr[j] with arr[i]
                    swap_bars(arr, i, j)

                # display the bars
                pygame.time.delay(3)
                __update_display(screen, arr, bar_color)
                bar_color[i] = WHITE
                bar_color[j] = WHITE

        # the position for the pivot is where left values are less than and
        # the right values are greater than the value at the pivot position
        arr[end] = arr[j + 1]
        arr[j + 1] = pivot
        pivot_index = j + 1

        # do the same process to the left partition and right partition
        __quick_sort(screen, arr, bar_color, pivot_index + 1, end)
        __quick_sort(screen, arr, bar_color, begin, pivot_index - 1)


#>>>>>>>>>>>>>>>>>>>>>>>>>> end of sorting_visualizer.py <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
