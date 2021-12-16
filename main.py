import pygame
from settings import *
from hero import Hero

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(FPS)
    screen.fill(BLACK)
    hero_sprite.draw(screen)
    pygame.display.flip()
pygame.quit()
