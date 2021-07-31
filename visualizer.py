import pygame

###############################################
### THE PARENT CLASS FOR THE TWO VISUALIZER ###
#---------------------------------------------#
class Visualizer:
    def __init__(self, width, height, title) -> None:
        # initialize pygame
        pygame.init()               
        # initialize the display
        self.screen = pygame.display.set_mode((width, height)) 
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        

    def draw(self):
        pygame.display.update()
        self.clock.tick(60)