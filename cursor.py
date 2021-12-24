import pygame
from pygame.sprite import AbstractGroup


class Cursor(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load("images/trigger.png")
        self.rect = self.image.get_rect()
        self.aim = 0
        self.have_target = False

    def change_aim(self):
        self.aim = 1 if self.aim == 0 else 0
        if self.aim:
            self.image = pygame.image.load("images/auto_aim_trigger.png")
        else:
            self.image = pygame.image.load("images/trigger.png")


trigger = pygame.sprite.Group()
cursor = Cursor(trigger)
