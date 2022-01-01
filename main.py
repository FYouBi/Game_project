import pygame

import interactive_obj
from cam import Camera
from settings import *
from hero_and_mobs import player, hero_sprite, mobs_sprite
from cursor import cursor, trigger
from interactive_obj import coin_sprite
from win32api import GetSystemMetrics

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

pygame.mixer.pre_init(44100, -16, 1, 512)
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

endurance = pygame.USEREVENT + 7
pygame.time.set_timer(endurance, 1000)

COIN_FLIP = pygame.USEREVENT + 8
pygame.time.set_timer(COIN_FLIP, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

camera = Camera()

bar = False
running = True
sprint = False
block = False
font_size_Died = 30
width_batery_color = 0
stamina = ENDURANCE
auto_aim = 0
dict_of_distance = {}
sorted_keys = None
die_hero_sound = pygame.mixer.Sound('sounds/dead.wav')
hit_hero_sound = pygame.mixer.Sound('sounds/hit.wav')
the_world = pygame.mixer.Sound('sounds/the_world.wav')
time_resume = pygame.mixer.Sound('sounds/time_resumes.wav')
play_sounder = 0
heal = False
count_coins = 0
pause = False
confirmation_exit = False
select_button_options = 0
bg = pygame.image.load(f'images/fon.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
buttons_option = ['resume', 'exit']
resume_color = [DARK_GREEN, GREEN]
exit_color = [CRIMSON, RED]


def render_all_font_HUD():
    global font_size_Died, PIXEL_SEC, width_batery_color, bar

    screen.blit(bg, (0, 0))
    interactive_obj.dirt.draw(screen)
    interactive_obj.ground.draw(screen)
    coin_sprite.draw(screen)
    hero_sprite.draw(screen)
    mobs_sprite.draw(screen)

    font_count_coin = pygame.font.Font('fonts/pixel_font.otf', 30)
    text_background = font_count_coin.render(f'{count_coins}', True, GRAY)
    screen.blit(text_background, (WIDTH - 180, HEIGHT - 63))

    font_count_coin = pygame.font.Font('fonts/pixel_font.otf', 30)
    text_background = font_count_coin.render(f'{count_coins}', True, WHITE)
    screen.blit(text_background, (WIDTH - 185, HEIGHT - 63))

    # Отрисовка востановления здоровья
    pygame.draw.rect(screen, DARK_GREEN, (11, 68, 100, 10))
    pygame.draw.rect(screen, GREEN, (6, 65, player.heal, 10))

    # Отрисовка стамины
    pygame.draw.rect(screen, DARK_BLUE, (11, 50, 160, 10))
    pygame.draw.rect(screen, LIGHT_BLUE, (6, 45, player.stamina, 10))

    # Частичная отрисовка батареии
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 172, 10, 130, 30), 10)
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 172, 10, 128, 23))

    font_FPS = pygame.font.Font('fonts/pixel_font.otf', 26)

    if not player.pause:
        if player.update_render_player:
            if not bar:
                if width_batery_color <= 130:
                    width_batery_color += PIXEL_SEC / FPS + 0.224
            if bar:
                if width_batery_color >= 0:
                    if player.update_render_player:
                        width_batery_color -= PIXEL_SEC / FPS + 0.1
                else:
                    bar = False

    # Отрисовка батареи
    pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH - 170, 5, width_batery_color, 30))
    pygame.draw.rect(screen, SILVER, (WIDTH - 41, 10, 10, 20))
    pygame.draw.rect(screen, BLACK, (WIDTH - 170, 5, 130, 30), 4)
    pygame.draw.rect(screen, BLACK, (WIDTH - 41,  10, 10, 20), 4)

    # Отрисовка тени хп
    pygame.draw.rect(screen, CRIMSON, (10, 10, 160, 30))

    # Отрисовка здоровья
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
    render = font_FPS.render(FPS_LOOK, False, (0, 255, 0))
    screen.blit(render, (15, HEIGHT - 40))

    if not player.update_render_player:
        if int(font_size_Died) <= WIDTH//6:
            font_size_Died += PIXEL_SEC / FPS + 0.8
            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died + 10))
            render_die = font_died.render('Ты умер', False, BLACK)
            screen.blit(render_die, (230, HEIGHT // 3))

            font_size_Died += PIXEL_SEC / FPS + 0.6
            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died))
            render_die = font_died.render('Ты умер', False, CRIMSON)
            screen.blit(render_die, (250, HEIGHT // 3))
        else:
            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died + 10))
            render_die = font_died.render('Ты умер', False, BLACK)
            screen.blit(render_die, (230, HEIGHT // 3))

            font_died = pygame.font.Font('fonts/pixel_font.otf', int(font_size_Died))
            render_die = font_died.render('Ты умер', False, CRIMSON)
            screen.blit(render_die, (250, HEIGHT // 3))
    if player.pause:
        # screen.blit(pygame.image.load(f'images/ground.png'), (0, 0))

        font_pause = pygame.font.Font('fonts/pixel_font.otf', 100)
        text = font_pause.render(f'ПРОДОЛЖИТЬ', True, resume_color[0])
        screen.blit(text, (WIDTH // 2 - 210, HEIGHT // 2 - 95))

        font_pause = pygame.font.Font('fonts/pixel_font.otf', 100)
        text = font_pause.render(f'ПРОДОЛЖИТЬ', True, resume_color[1])
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

        font_pause = pygame.font.Font('fonts/pixel_font.otf', 86)
        text = font_pause.render(f'ВЫЙТИ ИЗ ИГРЫ', True, exit_color[0])
        screen.blit(text, (WIDTH // 2 - 210, HEIGHT // 2 + 5))

        font_pause = pygame.font.Font('fonts/pixel_font.otf', 86)
        text = font_pause.render(f'ВЫЙТИ ИЗ ИГРЫ', True, exit_color[1])
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))


while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        M = pygame.mouse.get_pressed()
        motion = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and player.pause:
                select_button_options += 1
                if select_button_options > 1:
                    select_button_options = 0
            elif event.key == pygame.K_w and player.pause:
                select_button_options -= 1
                if select_button_options < 0:
                    select_button_options = 1
            if select_button_options == 0:
                resume_color = [DARK_GREEN, GREEN]
                exit_color = [CRIMSON, RED]
            else:
                exit_color = [DARK_GREEN, GREEN]
                resume_color = [CRIMSON, RED]
            if event.key == pygame.K_e and player.pause:
                if buttons_option[select_button_options] == 'exit':
                    running = False
                if buttons_option[select_button_options] == 'resume':
                    player.pause = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                player.paus()

        if event.type == pygame.MOUSEMOTION and not cursor.have_target:
            cursor.rect.topleft = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                cursor.change_aim()
                auto_aim = cursor.aim
            if event.button == 1 and not player.pause:
                if player.stamina >= 36:
                    if player.update_render_player:
                        hit_hero_sound.set_volume(0.2)
                        hit_hero_sound.play(loops=0, maxtime=0, fade_ms=12)
                player.hit(cursor)

        if event.type == STEP_EVENT and not player.pause:
            player.do_step()

        if event.type == HIT_EVENT and not player.pause:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True

        if event.type == COIN_FLIP and not player.pause:
            for sprite in coin_sprite:
                sprite.update()

        if event.type == ABILITY_READY and not player.pause:
            ABILITY = True
            pygame.time.set_timer(ABILITY_READY, 0)

        if event.type == ABILITY_TIME and not player.pause:
            pygame.time.set_timer(ABILITY_TIME, 0)
            pygame.time.set_timer(ABILITY_READY, 3000)
            time_resume.set_volume(0.2)
            time_resume.play(loops=0, maxtime=0, fade_ms=120)
            player.the_world()
            player.velocity = SPEED

        if event.type == pygame.KEYDOWN and not player.pause:
            if event.key == pygame.K_x and ABILITY:
                bar = True
                ABILITY = False
                player.the_world()
                the_world.set_volume(0.2)
                the_world.play(loops=0, maxtime=0, fade_ms=120)
                pygame.time.set_timer(ABILITY_TIME, 5300)
                player.velocity *= 0.3

            if event.key == pygame.K_LSHIFT and not block and not player.pause:
                sprint = True
            if event.key == pygame.K_q:
                heal = True
            if event.key == pygame.K_f and not sprint:
                block = True
                player.velocity -= 0.5

        if event.type == pygame.KEYUP and not player.pause:
            if event.key == pygame.K_LSHIFT:
                sprint = False
            if event.key == pygame.K_q:
                heal = False
            if event.key == pygame.K_f and block:
                block = False
                player.block = False
                player.velocity += 0.5

    if sprint:
        player.sprint()
    else:
        player.velocity_dawn()
    if heal:
        player.heal_up()
    if block and player.stamina > 0:
        player.block = True
        player.stamina -= 0.1
    if not block and not sprint:
        if player.stamina < 160:
            player.up_stamina()
    if KEY[pygame.K_d]:
        player.move_right()
    if KEY[pygame.K_a]:
        player.move_left()
    # if KEY[pygame.K_w]:
    #     player.move_up()
    # if KEY[pygame.K_s]:
    #     player.move_down()
    if KEY[pygame.K_SPACE]:
        player.jump()
    if motion[0] > WIDTH//2 and motion[1] >= 0:
        player.right_mouse()
    if motion[0] < WIDTH//2 - 5 and motion[1] >= 0:
        player.left_mouse()

    count_coins = player.check_collide_with_coin()

    for mob in mobs_sprite.sprites():
        distance = ((int(player.rect.centerx) - int(mob.rect.centerx)) ** 2 +
                    (int(player.rect.centery) - int(mob.rect.centery)) ** 2) ** 0.5
        if distance <= WIDTH//3 + 10:
            mob.run()

    if not player.update_render_player:
        if play_sounder == 0:
            play_sounder = 1
            die_hero_sound.set_volume(0.4)
            die_hero_sound.play(loops=0, maxtime=0, fade_ms=120)

    screen.fill(BACKGROUND)
    render_all_font_HUD()
    if pygame.mouse.get_focused():
        trigger.draw(screen)
    camera.update(player)
    for sprite in hero_sprite:
        camera.apply(sprite)
    for sprite in mobs_sprite:
        camera.apply(sprite)
    for sprite in coin_sprite:
        camera.apply(sprite)
    for sprite in interactive_obj.ground:
        camera.apply(sprite)
    for sprite in interactive_obj.dirt:
        camera.apply(sprite)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
