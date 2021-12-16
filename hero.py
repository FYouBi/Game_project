import pygame
from pygame.sprite import AbstractGroup
from settings import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/hero_default_right.png')
        self.step_count = 1
        self.way = 'right'
        self.rect = self.image.get_rect()

    def move_right(self):
        self.rect.x += SPEED + 1
        self.way = 'right'

    def move_left(self):
        self.rect.x -= SPEED
        self.way = 'left'

    def move_up(self):
        self.rect.y -= SPEED

    def move_down(self):
        self.rect.y += SPEED

    def do_step(self):
        self.image = pygame.image.load(f'images/hero_default_{self.way}_step_{self.step_count}.png')
        self.step_count += 1 if self.step_count == 1 else -1

