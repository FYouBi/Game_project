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
    def __init__(self, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/crow-export.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = pos, 793


class Dirt(pygame.sprite.Sprite):
    def __init__(self, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/gryaz-export.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = pos
        if not self.rect.colliderect(screen_rect):
            self.kill()


screen_rect = (0, 0, WIDTH, HEIGHT)
x = -880
y = 893
dirt = pygame.sprite.Group()
ground = pygame.sprite.Group()
while kill:
    Ground(x, ground)
    Dirt((x, y), dirt)
    x += 80
    if x == 1200:
        kill = False
        x = 0
    else:
        kill = True
coin_sprite = pygame.sprite.Group()