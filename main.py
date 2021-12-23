import os

import pygame

import hero_mobs
from cam import Camera
from settings import *
from hero_mobs import player, hero_sprite, mobs_sprite


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

FROZEN = pygame.USEREVENT + 6
pygame.time.set_timer(FROZEN, 4000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
bar = False
running = True
font_size_Died = 30
pixel_sec = 10
width_batery_color = 0
camera = Camera()


trigger = pygame.sprite.Group()
cursor_image = pygame.image.load("images/trigger.png")
cursor = pygame.sprite.Sprite(trigger)
cursor.image = cursor_image
cursor.rect = cursor.image.get_rect()


def render_all_font_HUD():
    global font_size_Died, pixel_sec, width_batery_color, bar
    hero_sprite.draw(screen)
    mobs_sprite.draw(screen)
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 172, 10, 130, 30), 10)
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 172, 10, 128, 23))
    font_FPS = pygame.font.Font('fonts/pixel_font.otf', 26)
    if player.update_render_player:
        if ABILITY:
            if width_batery_color <= 130:
                width_batery_color += pixel_sec / FPS + 3
        if bar:
            if width_batery_color >= 0:
                if player.update_render_player:
                    width_batery_color -= pixel_sec / FPS + 0.2
            else:
                bar = False

    pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH - 170, 5, width_batery_color, 30))
    pygame.draw.rect(screen, SILVER, (WIDTH - 41, 10, 10, 20))
    pygame.draw.rect(screen, BLACK, (WIDTH - 170, 5, 130, 30), 4)
    pygame.draw.rect(screen, BLACK, (WIDTH - 41,  10, 10, 20), 4)
    pygame.draw.rect(screen, CRIMSON, (10, 10, 160, 30))

    for i in range(player.health):
        kf = 5 + 20 * (i // 13)
        yellow_kf = 24 + 20 * (i // 13)
        if player.health <= default_HEALTH_PLAYER - 12:
            pygame.draw.rect(screen, YELLOW, (yellow_kf, 5, 20, 30))
        pygame.draw.rect(screen, (235, 55, 52), (kf, 5, 20, 30))

    if player.health > int(default_HEALTH_PLAYER * 0.6):
        health_color = STATUS_BAR_HEALTH_FULL_COLOR
        health_color_background = 90, 162, 5
    elif 20 < player.health < int(default_HEALTH_PLAYER * 0.6):
        health_color = 200, 200, 0
        health_color_background = 150, 150, 0
    else:
        health_color = CRIMSON
        health_color_background = 90, 0, 5

    font_background = pygame.font.Font('fonts/pixel_font.otf', 40)
    text_background = font_background.render(f'{player.health}', True, health_color_background)
    screen.blit(text_background, (175, -1))

    font = pygame.font.Font('fonts/pixel_font.otf', 40)
    text = font.render(f'{player.health}', True, health_color)
    screen.blit(text, (173, -3))

    FPS_LOOK = str(int(clock.get_fps()))
    render = font_FPS.render(FPS_LOOK, 0, (0, 255, 0))
    screen.blit(render, (15, HEIGHT - 40))

    if not player.update_render_player:
        if int(font_size_Died) <= 100:
            font_size_Died += pixel_sec / FPS + 1
            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died))
            render_die = font_died.render('Ты умер', 0, CRIMSON)
            screen.blit(render_die, (250, HEIGHT // 2 - 100))
        else:
            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died))
            render_die = font_died.render('Ты умер', 0, CRIMSON)
            screen.blit(render_die, (250, HEIGHT // 2 - 100))


while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        M = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if KEY[pygame.K_ESCAPE]:
            running = False

        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos

        elif M[0]:
            player.hit()

        if event.type == STEP_EVENT:
            player.do_step()

        if event.type == HIT_EVENT:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True

        if event.type == UP_HEALTH_EVENT:
            if player.update_render_player:
                if player.health < default_HEALTH_PLAYER:
                    if player.health + 12 > default_HEALTH_PLAYER:
                        player.health += default_HEALTH_PLAYER - player.health
                    else:
                        player.health += 12
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
            if event.key == pygame.K_x and ABILITY:
                bar = True
                ABILITY = False
                player.the_world()
                pygame.time.set_timer(ABILITY_TIME, 3000)

        if bar:
            player.velocity *= 0.7
        else:
            if event.type == FROZEN:
                player.velocity = SPEED

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

    screen.fill(BACKGROUND)
    render_all_font_HUD()
    if pygame.mouse.get_focused():
        trigger.draw(screen)
    camera.update(player)
    for sprite in hero_sprite:
        camera.apply(sprite)
    for sprit in mobs_sprite:
        camera.apply(sprit)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
