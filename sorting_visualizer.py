import pygame
from random import randint


BAR_WIDTH = 2
NUM_OF_BARS = 500
SCREEN_W = BAR_WIDTH * NUM_OF_BARS
WHITE = (200, 200, 200)
SCREEN_H = NUM_OF_BARS
SHIFT_DOWN = 150


###########################################
######### SORTING VISUALIZER CLASS ########
#-----------------------------------------#
# create the GUI and visualize the sorting 
# process for different sorting algorithms
###########################################

class SortingVisualizer:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sorting Algorithms Visualizer')
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H + SHIFT_DOWN))
        self.looping = True
        self.__create_bars()
        self.__main_loop()

    
    def __main_loop(self):
        while self.looping:
            self.__draw()
            self.__input_handling()


    def __create_bars(self):
        self.bar_list = []
        x_positions = list(range(1, NUM_OF_BARS + 1)) # list of x positions for the bars  
        # Shuffle the values in the array
        for i in range (NUM_OF_BARS):
            rand = randint(0, NUM_OF_BARS - 1)  # generate a random number
            # swap the values between index i and the index of the random number 
            temp = x_positions[i]
            x_positions[i] = x_positions[rand]
            x_positions[rand] = temp

        for value in range (1, NUM_OF_BARS + 1):
            new_bar = Bar(self.screen, x_positions[value - 1], SCREEN_H + SHIFT_DOWN, WHITE, BAR_WIDTH, value)
            self.bar_list.append(new_bar)


    def __input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.looping = False
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.looping = False
                    pygame.display.quit()


    def __draw(self):
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick()



###############################################
################# BAR CLASS ###################
#---------------------------------------------#
class Bar():

    def __init__(self, screen, index, pos_y, color, width, height) -> None:
        self.screen = screen
        self.index = index
        self.pos_x = index * BAR_WIDTH
        self.pos_y = pos_y
        self.height = height
        self.image = pygame.Surface([width, self.height])
        self.image.fill(color)
        # display the bar
        self.rect = self.image.get_rect()
        self.rect.bottomright = [self.pos_x, pos_y]
        self.__update()
        
    
    def get_height(self):
        return self.height
    
    def move_to(self, pos_x):
        self.pos_x = pos_x

    def __update(self):
        pygame.draw.rect(self.screen, WHITE, self.rect)

        



if __name__ == "__main__":
    SortingVisualizer()