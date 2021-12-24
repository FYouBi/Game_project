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
        self.health = default_HEALTH_PLAYER
        self.velocity = SPEED
        self.stamina = 160
        self.update_render_player = True

    def sprint(self):
        if self.update_render_player:
            if self.stamina > 0:
                if self.velocity > SPEED:
                    self.velocity = self.velocity
                elif self.velocity <= SPEED:
                    self.velocity *= 1.5
                self.stamina -= PIXEL_SEC / FPS + 0.2

    def up_stamina(self):
        self.stamina += PIXEL_SEC / FPS + 0.5

    def right_mouse(self):
        if self.update_render_player:
            self.way = 'right'

    def left_mouse(self):
        if self.update_render_player:
            self.way = 'left'

    def move_right(self):
        if self.update_render_player:
            self.rect.x += self.velocity + 1

    def move_left(self):
        if self.update_render_player:
            self.rect.x -= self.velocity + 1

    def move_up(self):
        if self.update_render_player:
            self.rect.y -= self.velocity + 1

    def move_down(self):
        if self.update_render_player:
            self.rect.y += self.velocity + 1

    def do_step(self):
        if self.update_render_player:
            self.image = pygame.image.load(f'images/hero_default_{self.way}_step_{self.step_count}.png')
            self.step_count += 1 if self.step_count == 1 else -1

    def hit(self):
        if self.update_render_player:
            self.image = pygame.image.load(f'images/hero_default_{self.way}_hit.png')
            for mob in mobs_sprite.sprites():
                if pygame.sprite.collide_mask(self, mob):
                    mob.check_health()

    def check_health(self):
        if self.update_render_player:
            self.health -= default_DAMAGE_MOB
            if self.health <= 0:
                self.health = 0
                self.update_render_player = False

    def the_world(self):
        for mob in mobs_sprite.sprites():
            mob.freeze_func()


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/mob_right.png')
        self.spawn = (random.randrange(WIDTH // 2, WIDTH - 100), random.randrange(100, HEIGHT - 100))
        self.step_count = 1
        self.can_hit = True
        self.freeze = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.spawn[0], self.spawn[1]
        self.health = default_HEALTH_MOB

    def run(self):
        if not self.freeze:
            self.hero_pos = (player.rect.centerx, player.rect.centery)
            self.mask_enemy = pygame.mask.from_surface(self.image)
            self.mask_hero = player.mask
            self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
            self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)

            for mob in mobs_sprite.sprites():
                if pygame.sprite.collide_mask(self, mob) and self != mob:
                    if self.rect.x > mob.rect.x:
                        self.rect.x += 1
                        mob.rect.x -= 1
                    else:
                        self.rect.x -= 1
                        mob.rect.x += 1

            if self.can_hit:
                if self.hero_pos[0] < self.rect.x - 1:
                    self.rect.x -= 1
                    self.image = pygame.image.load(f'images/mob_left.png')
                if self.hero_pos[0] > self.rect.x - 1:
                    self.rect.x += 1
                    self.image = pygame.image.load(f'images/mob_right.png')
                if self.hero_pos[1] < self.rect.y - 1:
                    self.rect.y -= 1
                if self.hero_pos[1] > self.rect.y - 1:
                    self.rect.y += 1
            else:
                if self.hero_pos[0] < self.rect.x - 1:
                    self.rect.x += 1
                    self.image = pygame.image.load(f'images/mob_right.png')
                if self.hero_pos[0] > self.rect.x - 1:
                    self.rect.x -= 1
                    self.image = pygame.image.load(f'images/mob_left.png')
                if self.hero_pos[1] < self.rect.y - 1:
                    self.rect.y += 1
                if self.hero_pos[1] > self.rect.y - 1:
                    self.rect.y -= 1

            if self.crash > 0 and self.can_hit:
                self.can_hit = False
                self.image = pygame.image.load(f'images/mob_left3.png')
                player.check_health()

    def check_health(self):
        self.health -= default_DAMAGE_PLAYER
        if self.health <= 0:
            mobs_sprite.remove(self)

    def freeze_func(self):
        self.freeze = not self.freeze


hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)

mobs_sprite = pygame.sprite.Group()
for _ in range(4):
    Mob(mobs_sprite)
