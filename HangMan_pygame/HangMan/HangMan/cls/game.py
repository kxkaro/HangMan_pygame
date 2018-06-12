import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *

class Letter(pygame.sprite.Sprite):

    def __init__(self, image_path, letter = ''):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.letter = letter.upper()

class Player(pygame.sprite.Sprite):

    def __init__(self, image_path, speed = 0):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        self.speed = speed


    def move(self, width, height):

        keystate = pygame.key.get_pressed()

        if keystate[K_RIGHT] and self.rect.x < (width - self.rect.width): self.rect.x += self.speed
        if keystate[K_LEFT] and self.rect.x > 400: self.rect.x += self.speed * (-1)
        if keystate[K_DOWN] and self.rect.y < (height - self.rect.height): self.rect.y += self.speed
        if keystate[K_UP] and self.rect.y > 0: self.rect.y += self.speed * (-1)

        #self.collider_rect.x += self.speed * direction[0]
        #self.collider_rect.y += self.speed * direction[1]