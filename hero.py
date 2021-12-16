import pygame
from pygame.sprite import AbstractGroup
from settings import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load('hero_default_right.png')
        self.rect = self.image.get_rect()

    def move_right(self):
        self.rect.x += SPEED
        self.image = pygame.image.load('hero_default_right.png')

    def move_left(self):
        self.rect.x -= SPEED
        self.image = pygame.image.load('hero_default_left.png')

    def move_up(self):
        self.rect.y -= SPEED

    def move_down(self):
        self.rect.y += SPEED
