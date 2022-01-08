from settings import *
import pygame
from pygame.sprite import AbstractGroup

kill = True


def spawn_coin(pos):
    Coin(pos, coin_sprite)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.fl = False
        self.frame = 1
        self.count = 0
        self.image = pygame.image.load(f'images/coin{self.frame}.png')
        self.coin_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos

    def update(self):
        self.frame += 1 if self.frame < 6 else -5
        self.image = pygame.image.load(f'images/coin{self.frame}.png')


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, screen, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/crow-export.png').convert_alpha(screen)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos[0], pos[1]


class Dirt(pygame.sprite.Sprite):
    def __init__(self, pos, screen, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/gryaz-export.png').convert_alpha(screen)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = pos


dirt = pygame.sprite.Group()
ground = pygame.sprite.Group()
coin_sprite = pygame.sprite.Group()
