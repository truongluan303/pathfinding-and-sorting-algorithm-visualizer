import sys
import time
from os import path

import pygame

from .pathfinding_visualizer import PathfindingVisualizer
from .sorting_visualizer import SortingVisualizer


BLACK = (10, 10, 10)
GREEN = (10, 225, 20)
DARK_GRAY = (60, 60, 60)
LIGHT_GRAY = (100, 100, 100)


class HomeWindow:
    def __init__(self) -> None:

        pygame.init()

        self._stop = False
        self._width = 600
        self._height = 480
        self._screen = pygame.display.set_mode((self._width, self._height))

        if path.exists("./images/algo_icon.ico"):
            icon = pygame.image.load("./images/algo_icon.ico")
            pygame.display.set_icon(icon)

        self.__init_components()

        while not self._stop:
            self.__mainloop()

    def __mainloop(self) -> None:

        self._screen.fill(BLACK)

        mouse = pygame.mouse.get_pos()

        # render the instruction message
        self._screen.blit(self._message, (self._message_w[0], self._message_h[0]))

        # if mouse is hovered on a button then change the button color to light gray

        if self.__check_mouse_hovered(self._btn1_w, self._btn1_h, mouse):
            self.__draw_button(
                self._screen, LIGHT_GRAY, self._btn1_w[0], self._btn1_h[0]
            )
        else:
            self.__draw_button(
                self._screen, DARK_GRAY, self._btn1_w[0], self._btn1_h[0]
            )

        if self.__check_mouse_hovered(self._btn2_w, self._btn2_h, mouse):
            self.__draw_button(
                self._screen, LIGHT_GRAY, self._btn2_w[0], self._btn2_h[0]
            )
        else:
            self.__draw_button(
                self._screen, DARK_GRAY, self._btn2_w[0], self._btn2_h[0]
            )

        if self.__check_mouse_hovered(self._exit_btn_w, self._exit_btn_h, mouse):
            self.__draw_button(
                self._screen, LIGHT_GRAY, self._exit_btn_w[0], self._exit_btn_h[0]
            )
        else:
            self.__draw_button(
                self._screen, DARK_GRAY, self._exit_btn_w[0], self._exit_btn_h[0]
            )

        # adding the text to the buttons
        self._screen.blit(
            self._exit_text, (self._exit_btn_w[0] + 150, self._exit_btn_h[0] + 15)
        )
        self._screen.blit(self._btn1_text, (self._btn1_w[0] + 30, self._btn1_h[0] + 15))
        self._screen.blit(self._btn2_text, (self._btn2_w[0] + 60, self._btn2_h[0] + 15))

        # updates the frames of the game
        pygame.display.update()

        self.__event_handling(mouse)

    def __event_handling(self, mouse) -> None:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                sys.exit(0)

            # if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if self.__check_button_clicked(
                    self._exit_btn_w, self._exit_btn_h, mouse
                ):
                    sys.exit(0)

                if self.__check_button_clicked(self._btn1_w, self._btn1_h, mouse):
                    self._stop = True
                    time.sleep(0.2)
                    PathfindingVisualizer()
                    break

                if self.__check_button_clicked(self._btn2_w, self._btn2_h, mouse):
                    self._stop = True
                    time.sleep(0.2)
                    SortingVisualizer()
                    break

    def __init_components(self):

        self._btn_width = 350
        self._btn_height = 60
        half_btn_w = self._btn_width // 2
        half_win_w = self._width // 2

        self._small_font = pygame.font.SysFont("Corbel", 35)

        self._btn1_text = self._small_font.render("pathfinding visualizer", True, GREEN)
        self._btn2_text = self._small_font.render("sorting visualizer", True, GREEN)
        self._exit_text = self._small_font.render("exit", True, GREEN)
        self._message = self._small_font.render(
            "Pick the type of visualizer", True, GREEN
        )

        self._message_w = (half_win_w - half_btn_w, half_win_w + half_btn_w)
        self._message_h = (70, 70 + self._btn_height)

        self._btn1_w = (half_win_w - half_btn_w, half_win_w + half_btn_w)
        self._btn1_h = (150, 150 + self._btn_height)

        self._btn2_w = (half_win_w - half_btn_w, half_win_w + half_btn_w)
        self._btn2_h = (250, 250 + self._btn_height)

        self._exit_btn_w = (half_win_w - half_btn_w, half_win_w + half_btn_w)
        self._exit_btn_h = (350, 350 + self._btn_height)

    def __draw_button(self, master, color, x, y):
        pygame.draw.rect(master, color, [x, y, self._btn_width, self._btn_height])

    def __check_mouse_hovered(self, width_interval, height_interval, mouse_pos):
        x, y = mouse_pos
        w_beg, w_end = width_interval
        h_low, h_high = height_interval
        return w_beg <= x <= w_end and h_low <= y <= h_high

    def __check_button_clicked(self, width_interval, height_interval, clicked_pos):
        x, y = clicked_pos
        w_beg, w_end = width_interval
        h_low, h_high = height_interval
        return w_beg <= x <= w_end and h_low <= y <= h_high
