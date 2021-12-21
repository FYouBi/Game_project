import pygame
from settings import *
from hero import player, hero_sprite
from mobs import mobs_sprite

pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)

HIT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(HIT_EVENT, 3000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == STEP_EVENT:
            player.do_step()
        if event.type == HIT_EVENT:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True
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

    for mob in mobs_sprite.sprites():
        distance = ((int(player.rect.centerx) - int(mob.rect.centerx)) ** 2 +
                    (int(player.rect.centery) - int(mob.rect.centery)) ** 2) ** 0.5
        print(mob.can_hit if mob.can_hit is False else '')
        if distance <= 250:
            mob.run()

    screen.fill(WHITE)

    hero_sprite.draw(screen)
    mobs_sprite.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
