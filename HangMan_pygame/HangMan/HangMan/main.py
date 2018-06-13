import os 
import string
import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *
from cls.game import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set fonts for drawing 
pygame.init()
pygame.font.init() 

# Set game window frame, background amd fonts for printing
background_image = pygame.image.load("graphics/7.bmp")
size = width, height = background_image.get_rect().width, background_image.get_rect().height
screen = pygame.display.set_mode(size)
screen.blit(background_image, (0, 0))

done = False
clock = pygame.time.Clock()
game = Game()

while not done:

    done = game.process_events()

    game.run_level(background_image)

    game.display_frame(screen)

    clock.tick(60)


pygame.quit()