import pygame
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):

    def __init__(self, image_path, speed = 0, letter = ''):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        self.speed = speed
        self.letter = letter.upper()

    def move(self, direction):
        self.rect.x += self.speed * direction[0]
        self.rect.y += self.speed * direction[1]

        #self.collider_rect.x += self.speed * direction[0]
        #self.collider_rect.y += self.speed * direction[1]
