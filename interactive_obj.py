import random

from settings import *
import pygame
from pygame.sprite import AbstractGroup

kill = True


def spawn_coin(pos):
    Coin(pos)


def create_particles(position, particle_count, x, y, gravity):
    # количество создаваемых частиц
    # возможные скорости
    velocity = range(int(x[0]), int(x[1])), range(int(y[0]), int(y[1]))
    for _ in range(particle_count):
        Particle(position, random.choice(velocity[0]), random.choice(velocity[1]), gravity)


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


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = []
    for scale in (3, 5):
        fire.append(pygame.transform.scale(pygame.image.load('images/box.png'), (scale, scale)))

    def __init__(self, pos, dx, dy, gravity):
        super().__init__(coin_sprite)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.coin = False
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = gravity
        particle_sprite.add(self)

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, WIDTH, HEIGHT)):
            self.kill()


ground_first = pygame.sprite.Group()
particle_sprite = pygame.sprite.Group()
coin_sprite = pygame.sprite.Group()
ground_second = pygame.sprite.Group()
aid_kit = pygame.sprite.Group()
