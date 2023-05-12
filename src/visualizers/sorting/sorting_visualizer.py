from os import getcwd
from random import randint

import pygame
from pygame.constants import K_1
from pygame.constants import K_2
from pygame.constants import K_3
from pygame.constants import K_4
from pygame.constants import K_5
from pygame.constants import K_6
from pygame.font import SysFont

from src.visualizers.base_visualizer import BaseVisualizer


BAR_WIDTH = 2
NUM_OF_BARS = 500
SCREEN_BORDER = 10
SCREEN_W = BAR_WIDTH * NUM_OF_BARS
SCREEN_H = NUM_OF_BARS
SHIFT_DOWN = 150
NUM_OG_ALGOS = 6

WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (244, 242, 30)
GREEN = (10, 225, 20)
RED = (255, 0, 0)

_font = None
_looping = True  # keep the mainloop run
_is_sorted = False  # check if the bar list is already _is_sorted
_stop_sorting = False  # check whether to stop the sorting process without quitting


class SortingVisualizer(BaseVisualizer):
    """
    The GUI to visualize the sorting process.
    """

    def __init__(self) -> None:
        icon_path = getcwd() + "/images/sort_icon.ico"
        super().__init__(
            SCREEN_W,
            SCREEN_H + SHIFT_DOWN,
            "Sorting Algorithms Visualizer",
            BLACK,
            icon_path,
        )
        global _looping, bar_list, _font, bar_color, _is_sorted, _stop_sorting
        #######  initialize variables  #######
        _font = SysFont("consolas", 16, bold=True)  # the text font
        self._algo_text_colors = [GREEN] * NUM_OG_ALGOS  # generate the bars' colors
        self._bar_list = None  # list of bars to display
        self._bar_color = None  # the color for each bar
        self._algo = 1
        _looping = True
        _is_sorted = False
        #######  get the visualizer run  #######
        self.__choose_algo(1)
        self.__shuffle()
        self.__mainloop()

    def __mainloop(self) -> None:
        """
        mainloop to keep the screen displayed
        """
        while _looping:
            super().draw()
            self.__input_handling()

    def __input_handling(self) -> None:
        """
        handle the keyboard and mouse input before the sorting begins
        """
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
                elif event.key == pygame.K_RETURN and not _is_sorted:
                    self.__start()
                else:
                    switch = {K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6}
                    self.__choose_algo(switch.get(event.key, -1))

    def __create_instruction(self) -> None:
        """
        create the text instruction on the top of the screen
        """
        y = 30
        pos_x1 = 700
        self.pos_x2 = 30
        self.pos_y = []
        display_text(self._screen, "C: Shuffle", pos_x1, 10)
        display_text(self._screen, "<Enter>: Start", pos_x1, 30)
        display_text(self._screen, "ESC: Exit visualizer", pos_x1, 50)
        display_text(
            self._screen,
            "Press a corresponding number " "to choose algorithm",
            self.pos_x2,
            10,
        )

        # create the algorithm names for the user to choose
        self._algo_names = [
            "1. Merge Sort",
            "2. Quick Sort",
            "3. Heap Sort",
            "4. Insertion Sort",
            "5. Selection Sort",
            "6. Bubble Sort",
        ]
        for i in range(NUM_OG_ALGOS):
            self.pos_y.append(y)
            display_text(
                self._screen,
                self._algo_names[i],
                self.pos_x2,
                y,
                self._algo_text_colors[i],
            )
            y += 20

    def __choose_algo(self, chosen) -> None:
        """
        pick the algorithm to run
        Args:
            chosen ([type]): the chosen algorithm
        """
        if chosen != -1:
            self._algo_text_colors[
                self._algo - 1
            ] = GREEN  # unhighlight the previously chosen
            self._algo = chosen  # set the newly chosen one
            self._algo_text_colors[
                chosen - 1
            ] = YELLOW  # highlight the newly chosen one
            self.__create_instruction()  # update the display

    def __shuffle(self) -> None:
        """
        shuffle the bars
        """
        global _is_sorted
        self._bar_list = list(range(1, NUM_OF_BARS + 1))  # generate the bars
        _is_sorted = False  # set un_is_sorted
        self._bar_color = [WHITE] * NUM_OF_BARS  # reset bar colors
        for i in range(NUM_OF_BARS):
            rand = randint(0, NUM_OF_BARS - 1)  # generate a random index
            swap_bars(self._bar_list, i, rand)  # swap to shuffle

        # update the screen display after shuffling
        show_bars(self._screen, self._bar_list, self._bar_color)  # show the bar list
        self.__create_instruction()  # show the text

    def __start(self) -> None:
        """
        start the sorting process
        """
        global _is_sorted, _stop_sorting
        _is_sorted = True
        _stop_sorting = False
        switcher = {
            1: lambda screen, bar_list, bar_color: merge_sort(
                screen, bar_list, bar_color
            ),
            2: lambda screen, bar_list, bar_color: quick_sort(
                screen, bar_list, bar_color
            ),
            3: lambda screen, bar_list, bar_color: heap_sort(
                screen, bar_list, bar_color
            ),
            4: lambda screen, bar_list, bar_color: insertion_sort(
                screen, bar_list, bar_color
            ),
            5: lambda screen, bar_list, bar_color: selection_sort(
                screen, bar_list, bar_color
            ),
            6: lambda screen, bar_list, bar_color: bubble_sort(
                screen, bar_list, bar_color
            ),
        }
        # use the algorithm corresponding to the number chosen
        switcher.get(self._algo)(self._screen, self._bar_list, self._bar_color)

        # refresh the screen display
        if _looping:
            show_bars(self._screen, self._bar_list, self._bar_color)
            self.__create_instruction()
            pygame.display.update()

        # if the bars are all _is_sorted, we add the running effect
        if _looping and not _stop_sorting:
            for i in range(NUM_OF_BARS):
                self._bar_color[i] = YELLOW
                pygame.time.delay(1)
                # update the display
                show_bars(self._screen, self._bar_list, self._bar_color)
                self.__create_instruction()
                pygame.display.update()


def display_text(screen, string, pos_x, pos_y, color=GREEN) -> None:
    """
    display the text on the screen
    Args:
        screen ([type]): the screen to show the text on
        string ([type]): the text
        pos_x ([type]): the x-coordinate where the text is located
        pos_y ([type]): the y-coordinate where the text is located
        color ([type], optional): text color (defaults to green)
    """
    text = _font.render(string, False, color)
    screen.blit(text, (pos_x, pos_y))


def swap_bars(arr, idx1, idx2) -> None:
    """
    swap 2 bars
    Args:
        arr ([type]): the array
        idx1 ([type]): the index of the 1st bar
        idx2 ([type]): the index of the 2nd bar
    """
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]


def show_bars(screen, bar_list, bar_color) -> None:
    """
    update the bars on the screen
    Args:
        screen ([type]): the screen
        bar_list ([type]): the list of the bars
        bar_color ([type]): the bars' color
    """
    # since we cannot clear a specific object on the pygame display,
    # we must clear the screen and then re-display the bar list to show the changes on the list
    screen.fill(BLACK)
    for i in range(len(bar_list)):
        __create_bar(screen, bar_list[i], i, bar_color[i])


def quit() -> None:
    """
    quit the visualize and go back to the menu screen
    """
    global _looping, _stop_sorting
    _looping = False
    _stop_sorting = True
    pygame.display.quit()


def __show_running_instruction(screen) -> None:
    """
    display the instruction text when the sorting process has already begun
    Args:
        screen ([type]): the screen
    """
    if not _stop_sorting and _looping:
        display_text(screen, "ECS: Exit visualizer", 30, 10)
        display_text(screen, "C: Stop sorting", 30, 30)


def __create_bar(screen, value, index, color) -> None:
    """
    create a bar with a specific characteristics
    Args:
        screen ([type]): the screen to put the bar on
        value ([type]): the value of the bar (which is also used to determine the bar's height)
        index ([type]): the bar's index
        color ([type]): the color of the bar
    """
    pos_x = index * BAR_WIDTH + BAR_WIDTH
    pos_y = SCREEN_H + SHIFT_DOWN
    height = value
    # generate the bar with the desired characteristics
    image = pygame.Surface([BAR_WIDTH, height])
    rect = image.get_rect()
    rect.bottomright = [pos_x, pos_y]
    pygame.draw.rect(screen, color, rect)


def __input_handling() -> None:
    """
    handle the keyboard and mouse input after the sorting has already begun
    """
    global _stop_sorting, _is_sorted
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            # C -> stop sorting
            elif event.key == pygame.K_c:
                _stop_sorting = True
                _is_sorted = False


def __update_display(screen, bar_list, bar_color) -> None:
    """
    update the screen display (including the bar list display, the text display,
    and also handle the user's input)
    Args:
        screen ([type]): the screen
        bar_list ([type]): the list of bars
        bar_color ([type]): the color of the bars
    """
    if _looping:
        show_bars(screen, bar_list, bar_color)
        __show_running_instruction(screen)
        pygame.display.update()
        __input_handling()


#######################################################################################
######################### S O R T I N G   A L G O R I T H M S #########################
#######################################################################################


def selection_sort(screen, array, bar_color) -> None:
    for i in range(0, len(array)):
        min = array[i]
        for j in range(i, len(array)):
            if not _stop_sorting:
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


def bubble_sort(screen, array, bar_color) -> None:
    for i in range(0, len(array)):
        for j in range(0, len(array) - i - 1):
            if not _stop_sorting:
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


def insertion_sort(screen, arr, bar_color) -> None:
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key < arr[j] and not _stop_sorting:
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


def merge_sort(screen, arr, bar_color) -> None:
    __merge_sort(screen, arr, bar_color, 0, len(arr) - 1)


def __merge_sort(screen, arr, bar_color, begin, end):
    if begin < end and not _stop_sorting:
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
            if _stop_sorting:
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
            if _stop_sorting:
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
            if _stop_sorting:
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
        if not _stop_sorting:
            while i < right_lim + 1:
                # update the display
                bar_color[i] = RED
                arr[i] = temp[j]
                pygame.time.delay(3)
                __update_display(screen, arr, bar_color)
                bar_color[i] = WHITE
                i += 1
                j += 1


def quick_sort(screen, arr, bar_color) -> None:
    __quick_sort(screen, arr, bar_color, 0, len(arr) - 1)


def __quick_sort(screen, arr, bar_color, begin, end) -> None:
    if begin < end:
        pivot = arr[end]
        j = begin - 1

        for i in range(begin, end):
            if not _stop_sorting:
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


def heap_sort(screen, arr, bar_color):
    def heapify(size: int, idx: int):
        """
        An inner helper function to perform max heapify process
        Args:
            arr (list): the array
            size (int): the size limit
            idx (int):  current index
        """
        if _stop_sorting:
            return

        max_idx = idx  # set the max index to be the current index
        lidx = idx * 2 + 1  # the left child's index
        ridx = idx * 2 + 2  # the right child's index

        # find the biggest element among the root and 2 children
        if lidx < size and arr[lidx] > arr[max_idx]:
            max_idx = lidx
        if ridx < size and arr[ridx] > arr[max_idx]:
            max_idx = ridx

        # if the max index has been changed
        if max_idx != idx:
            # swap the elements at current index and max index
            swap_bars(arr, idx, max_idx)

            # update the display
            bar_color[idx] = GREEN
            bar_color[max_idx] = RED
            __update_display(screen, arr, bar_color)
            pygame.time.delay(1)
            bar_color[idx] = WHITE
            bar_color[max_idx] = WHITE

            # continue heapifying the affected subtree
            heapify(size, max_idx)

    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(len(arr), i)

    for i in range(len(arr) - 1, -1, -1):
        swap_bars(arr, 0, i)  # move the root to the end of the array
        heapify(i, 0)  # max heapify the reduced heap
