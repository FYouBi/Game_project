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
        KEY = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
    if KEY[pygame.K_d]:
        player.move_right()
    if KEY[pygame.K_a]:
        player.move_left()
    if KEY[pygame.K_w]:
        player.move_up()
    if KEY[pygame.K_s]:
        player.move_down()

    screen.fill(BLACK)
    hero_sprite.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
