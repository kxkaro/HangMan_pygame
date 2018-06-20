import os 
import string
import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *
from cls.game import *


# Set fonts for drawing 
pygame.init()
pygame.font.init() 

# Set game window frame, background amd fonts for printing
background_image = pygame.image.load("graphics/7.bmp")
size = width, height = background_image.get_rect().width, background_image.get_rect().height
screen = pygame.display.set_mode(size)
screen.blit(background_image, (0, 0))

Keyword.initialize_list(["aaaaaaaaaaaaaaaaaaaaaa"])

done = False
clock = pygame.time.Clock()
game_state = Menu()

while not done:
    if game_state.__class__ != game_state.process_events().__class__: 
        
        game_state = game_state.process_events()

    game_state.run_level(screen)

    game_state.display_frame(screen)
    
    clock.tick(60)


#pygame.quit()