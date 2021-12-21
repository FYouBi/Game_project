import pygame
from pygame.sprite import AbstractGroup
from settings import *
from hero import player


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/mob_right.png')
        self.spawn = 450, 340
        self.step_count = 1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.spawn[0], self.spawn[1]
        radius = 50
        self.had_seen = False
        # dist = ((int(self.hero_x) - int(self.rect.x)) ** 2 + (int(self.hero_y) - int(self.rect.y)) ** 2) ** 0.5
        # if dist <= (int(radius) + int(50)):
        #     self.run()
        self.run()

    def run(self):
        self.hero_pos = (player.rect.x, player.rect.y)
        print(self.hero_pos[0], self.hero_pos[1])
        if self.hero_pos[0] < self.rect.x:
            self.rect.x -= 1.3
        elif self.hero_pos[0] > self.rect.x:
            self.rect.x += 1.3

        if self.hero_pos[1] < self.rect.y:
            self.rect.y -= 1.3
        elif self.hero_pos[1] > self.rect.y:
            self.rect.y += 1.3
        if self.hero_pos[0] == self.rect.x and self.hero_pos[1] == self.rect.y:
            BACKGROUND = (255, 0, 0)


mobs_sprite = pygame.sprite.Group()
mob = Mob(mobs_sprite)
