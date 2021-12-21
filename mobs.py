import random
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from hero import player


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/mob_right.png')
        self.spawn = (random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100))
        self.step_count = 1
        self.can_hit = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.spawn[0], self.spawn[1]
        self.health = 3

    def run(self):
        self.hero_pos = (player.rect.centerx, player.rect.centery)
        self.mask_enemy = pygame.mask.from_surface(self.image)
        self.mask_hero = player.mask
        self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
        self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)
        if self.can_hit:
            if self.hero_pos[0] < self.rect.x - 5:
                self.rect.x -= 1
            if self.hero_pos[0] > self.rect.x - 5:
                self.rect.x += 1
            if self.hero_pos[1] < self.rect.y - 5:
                self.rect.y -= 1
            if self.hero_pos[1] > self.rect.y - 5:
                self.rect.y += 1
        else:
            if self.hero_pos[0] < self.rect.x - 5:
                self.rect.x += 1
            if self.hero_pos[0] > self.rect.x - 5:
                self.rect.x -= 1
            if self.hero_pos[1] < self.rect.y - 5:
                self.rect.y += 1
            if self.hero_pos[1] > self.rect.y - 5:
                self.rect.y -= 1
        if self.crash > 0 and self.can_hit:
            self.can_hit = False
            player.health -= 1


mobs_sprite = pygame.sprite.Group()
for _ in range(3):
    Mob(mobs_sprite)
