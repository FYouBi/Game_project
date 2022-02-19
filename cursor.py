import pygame
from pygame.sprite import AbstractGroup


class Cursor(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load("images/trigger.png")
        self.rect = self.image.get_rect()
        self.aim = 0
        self.have_target = False

trigger = pygame.sprite.Group()
cursor = Cursor(trigger)

