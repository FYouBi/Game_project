import pygame
from settings import *
from hero_and_mobs import player, hero_sprite, mobs_sprite
from camera import camera


pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)

HIT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(HIT_EVENT, 3500)

UP_HEALTH_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(UP_HEALTH_EVENT, 4000)

ABILITY_READY = pygame.USEREVENT + 4
pygame.time.set_timer(ABILITY_READY, 3000)
ABILITY = False

ABILITY_TIME = pygame.USEREVENT + 5
pygame.time.set_timer(ABILITY_TIME, 0)

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

        if event.type == UP_HEALTH_EVENT:
            if player.health < 8:
                player.health += 1
                pygame.time.set_timer(UP_HEALTH_EVENT, KD)

        if event.type == ABILITY_READY:
            ABILITY = True
            pygame.time.set_timer(ABILITY_READY, 0)
            print('ready')

        if event.type == ABILITY_TIME:
            pygame.time.set_timer(ABILITY_TIME, 0)
            pygame.time.set_timer(ABILITY_READY, 3000)
            player.the_world()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.hit()
            if event.key == pygame.K_x and ABILITY:
                ABILITY = False
                player.the_world()
                pygame.time.set_timer(ABILITY_TIME, 3000)

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
        if distance <= 450:
            mob.run()

    screen.fill((69, 68, 89))

    pygame.draw.rect(screen, BLACK, (5, 5, 160, 30), 1)
    for i in range(player.health):
        pygame.draw.rect(screen, (235, 55, 52), (5 + 20 * i, 5, 20, 30))

    font = pygame.font.Font(None, 50)
    text = font.render(f'{player.health}', True, BLACK)
    screen.blit(text, (145, 5))

    if ABILITY:
        font = pygame.font.Font(None, 24)
        text = font.render(f'THE WORLD Ready', True, BLACK)
        screen.blit(text, (800, 5))

    hero_sprite.draw(screen)
    mobs_sprite.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
