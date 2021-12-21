import pygame
from settings import *
from hero_mobs import player, hero_sprite
from hero_mobs import mobs_sprite

pygame.init()
font = pygame.font.Font(None, 36)
STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)
name = 'quarter.txt'
HIT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(HIT_EVENT, 3000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True

while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        elif KEY[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
        if event.type == STEP_EVENT:
            if player.health > 0:
                player.do_step()
        if event.type == HIT_EVENT:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if player.health > 0:
                    player.hit()
    if player.health > 0:
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
            if distance <= 250:
                mob.run()

    if BACKGROUND == 0:
        screen.fill(GRAY)
    else:
        screen.fill(RED)
    if player.health > 0:
        hero_sprite.draw(screen)
    mobs_sprite.draw(screen)
    FPS_LOOK = str(int(clock.get_fps()))
    render = font.render(FPS_LOOK, 0, (255, 0, 0))
    screen.blit(render, (0, 0))
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
