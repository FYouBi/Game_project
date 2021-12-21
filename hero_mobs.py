import random
import pygame
from pygame.sprite import AbstractGroup
from settings import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/hero_default_right.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.step_count = 1
        self.way = 'right'
        self.rect = self.image.get_rect()
        self.health = 5

    def move_right(self):
        self.rect.x += SPEED + 1
        self.way = 'right'

    def move_left(self):
        self.rect.x -= SPEED
        self.way = 'left'

    def move_up(self):
        self.rect.y -= SPEED

    def move_down(self):
        self.rect.y += SPEED + 1

    def do_step(self):
        self.image = pygame.image.load(f'images/hero_default_{self.way}_step_{self.step_count}.png')
        self.step_count += 1 if self.step_count == 1 else -1

    def hit(self):
        self.image = pygame.image.load(f'images/hero_default_{self.way}_hit.png')


hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/mob_right.png')
        self.spawn = (random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100))
        self.step_count = 1
        self.enemy = enemy
        self.can_hit = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.spawn[0], self.spawn[1]
        self.health = 3

    def run(self):
        self.hero_pos = (player.rect.centerx, player.rect.centery)
        self.mask_enemy = pygame.mask.from_surface(self.image)
        self.mask_hero = player.mask
        self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
        self.crash1 = (self.mask_enemy.overlap_area(self.mask_hero, self.offset)) + 150
        self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)
        for mob in mobs_sprite.sprites():
            if pygame.sprite.collide_mask(self, mob) and self != mob:
                if self.rect.x > mob.rect.x:
                    self.rect.x += 1
                    mob.rect.x -= 1
                elif self.rect.x < mob.rect.x:
                    self.rect.x -= 1
                    mob.rect.x += 1
                elif self.rect.y > mob.rect.y:
                    self.rect.y += 1
                    mob.rect.y -= 1
                else:
                    self.rect.y -= 1
                    mob.rect.y += 1
            else:
                pass

        # if self.can_hit:
        #     if self.hero_pos[0] < self.rect.x - 5:
        #         self.rect.x -= 1
        #     if self.hero_pos[0] > self.rect.x - 5:
        #         self.rect.x += 1
        #     if self.hero_pos[1] < self.rect.y - 5:
        #         self.rect.y -= 1
        #     if self.hero_pos[1] > self.rect.y - 5:
        #         self.rect.y += 1
        # else:
        #     if self.hero_pos[0] < self.rect.x - 5:
        #         self.rect.x += 1
        #     if self.hero_pos[0] > self.rect.x - 5:
        #         self.rect.x -= 1
        #     if self.hero_pos[1] < self.rect.y - 5:
        #         self.rect.y += 1
        #     if self.hero_pos[1] > self.rect.y - 5:
        #         self.rect.y -= 1
        # if self.crash > 0 and self.can_hit:
        #     self.can_hit = False
        #     player.health -= 1
        if 2400 > self.crash1 > 0:
            if self.hero_pos[0] > self.rect.x:
                if self.rect.topleft[0] > 0:
                    self.rect.x -= 1
            elif self.hero_pos[0] < self.rect.x:
                if self.rect.topright[0] < WIDTH:
                    self.rect.x += 1
            if self.hero_pos[1] > self.rect.y:
                if self.rect.topleft[1] > 0:
                    self.rect.y -= 1
            elif self.hero_pos[1] < self.rect.y:
                if self.rect.bottomleft[1] < HEIGHT:
                    self.rect.y += 1
        elif self.crash >= 0:
            print(mobs_sprite)
            vrag.enemy -= 1


mobs_sprite = pygame.sprite.Group()
vrag = Mob(mobs_sprite)
for _ in range(vrag.enemy):
    Mob(mobs_sprite)

