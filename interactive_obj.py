import pygame
from pygame.sprite import AbstractGroup


class Coin(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.fl = False
        self.frame = 1
        self.image = pygame.image.load(f'images/coin{self.frame}.png')
        self.coin_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 100


coin_sprite = pygame.sprite.Group()
coin = Coin(coin_sprite)
