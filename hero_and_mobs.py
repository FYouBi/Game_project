import random

import pygame.sprite
from pygame.sprite import AbstractGroup
import interactive_obj
from settings import *


def flip(img, x_flip=False, y_flip=False):
    return pygame.transform.flip(img, x_flip, y_flip)


def cut_sheet(object, sheet, columns, rows):
    object.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (object.rect.w * i, object.rect.h * j)
            object.frames.append(sheet.subsurface(pygame.Rect(frame_location, object.rect.size)).convert_alpha(screen))


class Hero(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.frames = []
        self.cur_frame = 0
        cut_sheet(self, pygame.image.load(f'images/hero_walk_sheet.png'), 2, 1)
        # self.image = pygame.image.load(f'images/hero_default_right.png').convert_alpha(screen)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.step_count = 1
        self.coin_count = 0
        self.way = 'right'
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 100
        self.health = default_HEALTH_PLAYER
        self.damage = default_DAMAGE_PLAYER
        self.velocity = SPEED
        self.stamina = ENDURANCE
        self.can_jump = JUMP_Y
        self.can_jump_flag = False
        self.heal = default_HEALTH_PLAYER
        self.update_render_player = True
        self.pause = False
        self.block = False
        self.left = False
        self.rotate = False
        self.time_stop = False

    def jump(self):
        if self.update_render_player:
            if not self.pause:
                if self.can_jump > 0 and self.stamina > 40:
                    self.can_jump -= 1
                    player.stamina -= 2

                    self.rect.y -= 45
                else:
                    self.can_jump_flag = False
                    self.can_jump = JUMP_Y

    def paus(self):
        self.pause = not self.pause

    def heal_up(self):
        if not self.pause:
            if self.update_render_player:
                if self.heal > 0:
                    if self.health < 100:
                        self.health += 1
                        self.heal -= PIXEL_SEC / FPS + 1

    def sprint(self):
        if not self.pause:
            if self.update_render_player:
                if self.stamina > 0:
                    if self.velocity > SPEED:
                        self.velocity = self.velocity
                    elif self.velocity <= SPEED:
                        self.velocity *= 1.5
                    self.stamina -= PIXEL_SEC / FPS + 0.2

    def velocity_dawn(self):
        if not self.pause:
            self.velocity = SPEED

    def up_stamina(self):
        if not self.pause and not self.rotate:
            self.stamina += PIXEL_SEC / FPS + 0.8

    def move_right(self):
        if not self.pause:
            if self.update_render_player:
                self.rect.x += self.velocity + 1

    def move_left(self):
        if not self.pause:
            if self.update_render_player:
                self.rect.x -= self.velocity + 1

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha(screen)
        self.image = pygame.transform.scale(self.image, (16 * 3, 60))
        if self.left:
            self.image = flip(self.image, True)

    def hit(self, mouse_pos):
        if not self.pause:
            if self.update_render_player:
                if self.stamina >= 36:
                    self.rotate = True
                    for mob in mobs_sprite.sprites():
                        print(self.rect.centerx - mob.rect.centerx)
                        if -136 <= self.rect.centerx - mob.rect.centerx <= 166 \
                                and -136 <= self.rect.centery - mob.rect.centery <= 136:
                            print(True)
                            kill = mob.check_health()
                            if not kill:
                                mob.back_damage()
                            else:
                                return mob.check_health()
        return 0

    def check_collide_with_aid_kit(self):
        if self.heal != default_HEALTH_PLAYER:
            if pygame.sprite.spritecollide(self, interactive_obj.aid_kit, True):
                self.heal = 100

    def check_collide_with_coin(self):
        for sprite in interactive_obj.coin_sprite.sprites():
            if pygame.sprite.collide_mask(sprite, self) and sprite.coin:
                self.coin_count += random.randrange(9, 103)
                sprite.kill()

        return self.coin_count

    def check_collide_with_ground(self):
        if pygame.sprite.spritecollide(self, interactive_obj.ground_first, False):
            return True
        return False

    def check_health(self, damage):
        if not self.pause:
            if self.update_render_player:
                self.health -= damage
                if self.health <= 0:
                    self.health = 0
                    self.update_render_player = False

    def the_world(self):
        if not self.pause:
            player.time_stop = not player.time_stop
            for mob in mobs_sprite.sprites():
                mob.freeze_func()


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.damage_visual = False
        self.frames = []
        self.cur_frame = 0
        self.image = None
        self.limit_x = 100
        self.limit_y = 200
        self.step_count = 1
        self.can_hit = True
        self.freeze = False
        self.rect = None
        self.health = default_HEALTH_MOB
        self.mask_hero = player.mask

    def check_pos_y(self):
        if self.rect.y > 800:
            return True
        return False

    def check_collide_with_ground(self):
        for sprite in interactive_obj.ground_first:
            if pygame.sprite.collide_mask(sprite, self):
                return True
        return False

    def check_health(self):
        if not player.pause:
            self.health -= player.damage
            self.damage_visual = True
            if self.health <= 0:
                if random.randrange(0, 2) == 1:
                    interactive_obj.spawn_coin((self.rect.centerx, self.rect.centery))
                mobs_sprite.remove(self)
                return 1
            return 0

    def freeze_func(self):
        if not player.pause:
            self.freeze = not self.freeze


class Slime(Mob):
    def __init__(self, pos, color, groups: AbstractGroup):
        super().__init__()
        cut_sheet(self, pygame.image.load(f'images/slime_walk.png'), 6, 1)
        self.health = STATS_MOB_SLIME[color][1]
        self.color = color
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.direction = None
        self.right = False
        mobs_sprite.add(self)

    def run(self, distance):
        if not player.pause:
            if not self.freeze:
                self.hero_pos = (player.rect.centerx, player.rect.centery)
                self.mask_enemy = pygame.mask.from_surface(self.image)
                self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
                self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)

                if self.hero_pos[0] < self.rect.x:
                    self.direction = 'left'
                    self.right = False

                if self.hero_pos[0] > self.rect.x:
                    self.direction = 'right'
                    self.right = True

                if 350 < distance < 500:
                    if self.can_hit:
                        if self.hero_pos[0] < self.rect.x - 1:
                            self.rect.x -= 5

                        if self.hero_pos[0] > self.rect.x - 1:
                            self.rect.x += 5

                if distance < 350:
                    if self.hero_pos[0] < self.rect.x - 1:
                        self.rect.x += 5

                    if self.hero_pos[0] > self.rect.x - 1:
                        self.rect.x -= 5

                if distance < 700 and self.can_hit:
                    self.attack()
                    self.can_hit = False

    def back_damage(self):
        self.rect.y -= 52
        if self.direction == 'right':
            self.rect.x -= 30
        else:
            self.rect.x += 30

    def attack(self):
        SlimeBall(self.color, (self.rect.centerx, self.rect.centery - 15), self.direction)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image = self.image.convert_alpha(screen)
        if self.right:
            self.image = flip(self.image, True)


class SlimeBall(pygame.sprite.Sprite):
    def __init__(self, color, pos, direction, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/slime_ball.png').convert_alpha(screen)
        self.damage = STATS_MOB_SLIME[color][0]
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1] + 5
        balls_sprite.add(self)

    def move(self):
        if not player.pause:
            if self.direction == 'left':
                self.rect = self.rect.move(-20, 0)
            elif self.direction == 'right':
                self.rect = self.rect.move(20, 0)
            if pygame.sprite.collide_mask(player, self):
                player.check_health(self.damage)
                balls_sprite.remove(self)
                return self.damage
        return 0


hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)

balls_sprite = pygame.sprite.Group()
mobs_sprite = pygame.sprite.Group()