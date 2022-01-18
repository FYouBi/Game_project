import random
from pygame.sprite import AbstractGroup
import interactive_obj
from settings import *
from interactive_obj import coin_sprite


def flip(img, x_flip=False, y_flip=False):
    return pygame.transform.flip(img, x_flip, y_flip)


class Hero(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/hero_default_right.png').convert_alpha(screen)
        self.mask = pygame.mask.from_surface(self.image)
        self.step_count = 1
        self.coin_count = 0
        self.way = 'right'
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 100

        self.health = default_HEALTH_PLAYER
        self.velocity = SPEED
        self.stamina = ENDURANCE
        self.can_jump = JUMP_Y
        self.can_jump_flag = False
        self.heal = default_HEALTH_PLAYER2
        self.update_render_player = True
        self.pause = False
        self.block = False
        self.left = False

    def jump(self):
        if self.can_jump > 0:
            self.can_jump -= 1
            self.rect.y -= 10
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
        if not self.pause:
            self.stamina += PIXEL_SEC / FPS + 0.5

    def move_right(self):
        if not self.pause:
            if self.update_render_player:
                self.rect.x += self.velocity + 1

    def move_left(self):
        if not self.pause:
            if self.update_render_player:
                self.rect.x -= self.velocity + 1

    def do_step(self):
        if not self.pause:
            if self.update_render_player:
                self.image = pygame.image.load(f'images/hero_default_right_step_{self.step_count}.png')
                if self.left:
                    self.image = flip(self.image, x_flip=True)
                self.step_count += 1 if self.step_count == 1 else -1

    def hit(self, mouse_pos):
        if not self.pause:
            if self.update_render_player:
                if self.stamina >= 36:
                    self.stamina -= 36
                    self.image = pygame.image.load(f'images/hero_default_{self.way}_hit.png')
                    for mob in mobs_sprite.sprites():
                        if pygame.sprite.collide_mask(mouse_pos, mob) or pygame.sprite.collide_mask(self, mob):
                            mob.check_health()

    def check_collide_with_coin(self):
        for sprite in coin_sprite:
            if pygame.sprite.collide_mask(sprite, self):
                print(pygame.sprite.collide_mask(sprite, self))
                self.coin_count += random.randrange(9, 103)
                coin_sprite.remove(sprite)
        return self.coin_count

    def check_collide_with_ground(self):
        for sprite in interactive_obj.ground_first:
            if pygame.sprite.collide_mask(sprite, self):
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
            for mob in mobs_sprite.sprites():
                mob.freeze_func()


class Mob(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = None
        self.step_count = 1
        self.can_hit = True
        self.freeze = False
        self.rect = None
        self.health = default_HEALTH_MOB
        self.mask_hero = player.mask

    # def run(self):
    #     if not player.pause:
    #         if not self.freeze:
    #             self.hero_pos = (player.rect.centerx, player.rect.centery)
    #             self.mask_enemy = pygame.mask.from_surface(self.image)
    #             self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
    #             self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)
    #
    #             for mob in mobs_sprite.sprites():
    #                 if pygame.sprite.collide_mask(self, mob) and self != mob:
    #                     if self.rect.x > mob.rect.x:
    #                         self.rect.x += 1
    #                         mob.rect.x -= 1
    #                     else:
    #                         self.rect.x -= 1
    #                         mob.rect.x += 1
    #
    #             if self.can_hit:
    #                 if self.hero_pos[0] < self.rect.x - 1:
    #                     self.rect.x -= 1
    #                     self.image = pygame.image.load(f'images/mob_left1.png')
    #                 if self.hero_pos[0] > self.rect.x - 1:
    #                     self.rect.x += 1
    #                     self.image = pygame.image.load(f'images/mob_right1.png')
    #             else:
    #                 if self.hero_pos[0] < self.rect.x - 1:
    #                     self.rect.x += 1
    #                     self.image = pygame.image.load(f'images/mob_right1.png')
    #                 if self.hero_pos[0] > self.rect.x - 1:
    #                     self.rect.x -= 1
    #                     self.image = pygame.image.load(f'images/mob_left1.png')
    #
    #             if self.crash > 0 and self.can_hit:
    #                 self.can_hit = False
    #                 self.image = pygame.image.load(f'images/mob_left3.png')
    #                 if not player.block:
    #                     player.check_health()

    def check_collide_with_ground(self):
        for sprite in interactive_obj.ground_first:
            if pygame.sprite.collide_mask(sprite, self):
                return True
        return False

    def check_health(self):
        if not player.pause:
            self.health -= default_DAMAGE_PLAYER
            if self.health <= 0:
                if random.randrange(0, 2) == 1:
                    interactive_obj.spawn_coin((self.rect.centerx, self.rect.centery))
                mobs_sprite.remove(self)

    def freeze_func(self):
        if not player.pause:
            self.freeze = not self.freeze


class Slime(Mob):
    def __init__(self, pos, color, groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/{color}_slime.png').convert_alpha(screen)
        self.health = STATS_MOB_SLIME[color][1]
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.direction = None
        mobs_sprite.add(self)

    def run(self, distance):
        if not player.pause:
            if not self.freeze:
                if 350 < distance < 500:
                    self.hero_pos = (player.rect.centerx, player.rect.centery)
                    self.mask_enemy = pygame.mask.from_surface(self.image)
                    self.offset = (player.rect.x - self.rect.x + 5, player.rect.y - self.rect.y + 5)
                    self.crash = self.mask_enemy.overlap_area(self.mask_hero, self.offset)

                    if self.can_hit:
                        if self.hero_pos[0] < self.rect.x - 1:
                            self.rect.x -= 1
                            self.direction = 'left'

                        if self.hero_pos[0] > self.rect.x - 1:
                            self.rect.x += 1
                            self.direction = 'right'

                if distance < 350:
                    if self.hero_pos[0] < self.rect.x - 1:
                        self.rect.x += 1

                    if self.hero_pos[0] > self.rect.x - 1:
                        self.rect.x -= 1

                if distance < 500 and self.can_hit:
                    self.attack()
                    self.can_hit = False

    def attack(self):
        SlimeBall(self.color, (self.rect.centerx, self.rect.centery - 15), self.direction)


class SlimeBall(pygame.sprite.Sprite):
    def __init__(self, color, pos, direction, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/{color}_ball.png').convert_alpha(screen)
        self.damage = STATS_MOB_SLIME[color][0]
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        balls_sprite.add(self)

    def move(self):
        if self.direction == 'left':
            self.rect = self.rect.move(-8, 0)
        elif self.direction == 'right':
            self.rect = self.rect.move(8, 0)
        if pygame.sprite.collide_mask(player, self):
            player.check_health(self.damage)
            balls_sprite.remove(self)


hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)

balls_sprite = pygame.sprite.Group()
mobs_sprite = pygame.sprite.Group()
for _ in range(1):
    Slime((500, 100), 'green', mobs_sprite)
