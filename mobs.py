import random
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from hero import player


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/mob_right.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn = (random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100))
        self.step_count = 1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.spawn[0], self.spawn[1]

    def run(self):
        self.hero_pos = (player.rect.x, player.rect.y)
        print(self.hero_pos[0], self.hero_pos[1])
        if self.hero_pos[0] < self.rect.x:
            self.rect.x -= 1
        if self.hero_pos[0] > self.rect.x:
            self.rect.x += 1
        if self.hero_pos[1] < self.rect.y:
            self.rect.y -= 1
        if self.hero_pos[1] > self.rect.y:
            self.rect.y += 1


mobs_sprite = pygame.sprite.Group()
for _ in range(3):
    Mob(mobs_sprite)
