import pygame
from os import path

###############################################
### THE PARENT CLASS FOR THE TWO VISUALIZER ###
#---------------------------------------------#
class Visualizer:
    def __init__(self, width, height, title, color=(0,0,0), icon_path=None) -> None:
        # initialize pygame
        pygame.init()               
        # initialize the display
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(color)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)
        if icon_path is not None:
            if path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
        

    def draw(self):
        pygame.display.update()
        self.clock.tick(60)
