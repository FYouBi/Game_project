import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__(border_sprite)
        self.add(border_sprite)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


border_sprite = pygame.sprite.Group()
