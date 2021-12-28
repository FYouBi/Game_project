import pygame


class Sound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.die_hero = pygame.mixer.Sound('sounds/dead.wav')
        self.hit_hero = pygame.mixer.Sound('sounds/hit.wav')

    def play_hit(self):
        pass
