import pygame
from pygame.sprite import AbstractGroup
from hero_and_mobs import player


class Coin(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.fl = False
        self.frame = 1
        self.image = pygame.image.load(f'images/coin{self.frame}.png')
        self.coin_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 100

    def play_animation_coin(self):
        self.frame = 1
        self.fl = False
        if 4 >= self.frame >= 1 and not self.fl:
            self.frame += 1
            if self.frame == 4:
                self.fl = True
        elif self.fl:
            self.fl -= 1
            if self.frame == 1:
                self.fl = False


coin_sprite = pygame.sprite.Group()
coi = Coin(coin_sprite)
