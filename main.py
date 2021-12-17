import pygame
from settings import *
from hero import Hero

pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)

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
        if event.type == STEP_EVENT:
            player.do_step()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.hit()

    if KEY[pygame.K_d]:
        if player.rect.topright[0] < WIDTH:
            player.move_right()
    if KEY[pygame.K_a]:
        if player.rect.topleft[0] > 0:
            player.move_left()
    if KEY[pygame.K_w]:
        if player.rect.topleft[1] > 0:
            player.move_up()
    if KEY[pygame.K_s]:
        if player.rect.bottomleft[1] < HEIGHT:
            player.move_down()

    screen.fill(WHITE)
    hero_sprite.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
