import pygame
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):

    def __init__(self, image_path, width, height, speed = 0, letter = ''):
        super().__init__()

        #self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.letter = letter

    def move(self, direction):
        self.rect.x += self.speed * direction[0]
        self.rect.y += self.speed * direction[1]
