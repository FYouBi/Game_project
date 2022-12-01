import random

from settings import *
import pygame
from pygame.sprite import AbstractGroup

kill = True
# pyinstaller --onefile individual_project.py


def spawn_coin(pos):
    Coin(pos)


def create_particles(position, particle_count, x, y, gravity, color):
    # количество создаваемых частиц
    # возможные скорости
    velocity = range(int(x[0]), int(x[1])), range(int(y[0]), int(y[1]))
    for _ in range(particle_count):
        Particle1(position, random.choice(velocity[0]), random.choice(velocity[1]), gravity, color)


def create_particles2(position, particle_count, x, y, gravity, color):
    # количество создаваемых частиц
    # возможные скорости
    velocity = range(int(x[0]), int(x[1])), range(int(y[0]), int(y[1]))
    for _ in range(particle_count):
        Particle2(position, random.choice(velocity[0]), random.choice(velocity[1]), gravity, color)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.fl = False
        self.frame = 1
        self.count = 0
        self.coin = True
        self.image = pygame.image.load(f'images/coin{self.frame}.png')
        self.coin_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1] + 20
        coin_sprite.add(self)

    def update(self):
        self.frame += 1 if self.frame < 6 else -5
        self.image = pygame.image.load(f'images/coin{self.frame}.png')


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, screen, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/ground.png').convert_alpha(screen)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos[0], pos[1]


class AidKit(pygame.sprite.Sprite):
    def __init__(self, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(f'images/aid_kit.png').convert_alpha(screen)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos


class Particle1(pygame.sprite.Sprite):
    fire = []
    for scale in (3, 5):
        fire.append(pygame.transform.scale(pygame.Surface([5, 5]), (scale, scale)))

    def __init__(self, pos, dx, dy, gravity, color):
        super().__init__(coin_sprite)
        self.image = random.choice(self.fire)
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.coin = False
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = gravity
        particle_sprite.add(self)

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.image.fill(self.color)
        if not self.rect.colliderect((0, 0, WIDTH, HEIGHT)):
            self.kill()


class Particle2(pygame.sprite.Sprite):
    fire = []
    for scale in (3, 5):
        fire.append(pygame.transform.scale(pygame.Surface([5, 5]), (scale, scale)))

    def __init__(self, pos, dx, dy, gravity, color):
        super().__init__(coin_sprite)
        self.image = random.choice(self.fire)
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.coin = False
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = gravity
        particle_sprite.add(self)

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.image.fill(self.color)
        if not self.rect.colliderect((0, 0, WIDTH, HEIGHT)):
            self.kill()


ground_first = pygame.sprite.Group()
particle_sprite = pygame.sprite.Group()
coin_sprite = pygame.sprite.Group()
ground_second = pygame.sprite.Group()
aid_kit = pygame.sprite.Group()
