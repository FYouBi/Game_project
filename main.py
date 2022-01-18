import random
import interactive_obj
from cam import Camera
from settings import *
from hero_and_mobs import player, hero_sprite, mobs_sprite, balls_sprite
from cursor import cursor, trigger
from interactive_obj import coin_sprite


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)

HIT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(HIT_EVENT, 3500)

ABILITY_READY = pygame.USEREVENT + 4
pygame.time.set_timer(ABILITY_READY, 3000)
ABILITY = False

ABILITY_TIME = pygame.USEREVENT + 5
pygame.time.set_timer(ABILITY_TIME, 0)

endurance = pygame.USEREVENT + 7
pygame.time.set_timer(endurance, 1000)

COIN_FLIP = pygame.USEREVENT + 8
pygame.time.set_timer(COIN_FLIP, 120)

screen = screen
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
die_hero_sound = pygame.mixer.Sound('sounds/dead.wav')
hit_hero_sound = pygame.mixer.Sound('sounds/hit.wav')
the_world = pygame.mixer.Sound('sounds/the_world.wav')
time_resume = pygame.mixer.Sound('sounds/time_resumes.wav')
play_sounder = 0
status_image = pygame.image.load(f'images/hud_hp_stamina_medic-export.png').convert_alpha(screen)
battery = pygame.image.load(f'images/battery-export.png').convert_alpha(screen)
death_font = pygame.image.load(f'images/death_font.png').convert_alpha(screen)
death_font = pygame.transform.scale(death_font, (WIDTH//2, HEIGHT//2))
heal = False
count_coins = 0
pause = False
confirmation_exit = False
select_button_options = 0
bg = pygame.image.load(f'images/fon.png').convert_alpha(screen)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
buttons_option = ['resume', 'exit']
render_update = True
resume_color = [DARK_GREEN, GREEN]
exit_color = [CRIMSON, RED]
screen_rect = (0, 0, WIDTH, HEIGHT)


def render():
    global font_size_Died, PIXEL_SEC, width_batery_color, bar

    # Отрисовка спрайтов
    screen.blit(bg, (0, 0))
    interactive_obj.ground_first.draw(screen)
    interactive_obj.ground_second.draw(screen)
    coin_sprite.draw(screen)
    hero_sprite.draw(screen)
    mobs_sprite.draw(screen)
    balls_sprite.draw(screen)

    # Отрисовка кол-ва монет
    font_count_coin = pygame.font.Font('fonts/pixel_font.otf', 30)
    text_background = font_count_coin.render(f'{count_coins}', True, GRAY)
    screen.blit(text_background, (WIDTH - 180, HEIGHT - 63))
    font_count_coin = pygame.font.Font('fonts/pixel_font.otf', 30)
    text_background = font_count_coin.render(f'{count_coins}', True, WHITE)
    screen.blit(text_background, (WIDTH - 185, HEIGHT - 63))

    # Отрисовка востановления здоровья
    pygame.draw.rect(screen, DARK_GREEN, (6, 55, 55, 10))
    pygame.draw.rect(screen, GREEN, (6, 50, player.heal, 10))

    # Отрисовка стамины
    pygame.draw.rect(screen, DARK_BLUE, (6, 35, 60, 10))
    pygame.draw.rect(screen, LIGHT_BLUE, (6, 35, player.stamina, 10))

    font_FPS = pygame.font.Font('fonts/pixel_font.otf', 26)

    if not player.pause:
        if player.update_render_player:
            if not bar:
                if width_batery_color <= 75:
                    width_batery_color += PIXEL_SEC / FPS + 0.18
            if bar:
                if width_batery_color >= 0:
                    if player.update_render_player:
                        width_batery_color -= PIXEL_SEC / FPS + 0.05
                else:
                    bar = False

    # Отрисовка батареи
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 90, 15, 70, 35), 10)
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH - 90, 15, 70, 35))
    pygame.draw.rect(screen, LIGHT_BLUE,
                     (WIDTH - 90, 15, width_batery_color - 15 if width_batery_color > 15 else - 0, 35), 10)
    pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH - 90, 15, width_batery_color, 35))

    # Отрисовка тени хп
    pygame.draw.rect(screen, CRIMSON, (10, 10, 90, 20))

    # Отрисовка здоровья
    pygame.draw.rect(screen, (235, 55, 52), (5, 10, player.health, 20))
    pygame.draw.rect(screen, YELLOW, (player.health if player.health > 5 else + 5, 10, 5, 20))

    # Отрисовка ФПС
    FPS_LOOK = str(int(clock.get_fps()))
    render = font_FPS.render(FPS_LOOK, False, (0, 255, 0))
    screen.blit(render, (15, HEIGHT - 40))

    if not player.update_render_player:
        if int(font_size_Died) <= WIDTH // 6:
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
    screen.blit(status_image, (5, 5))
    screen.blit(battery, (WIDTH - 100, 10))


def set_map():
    interactive_obj.ground_first.empty()
    with open('map.txt', 'r') as _map:
        for y, i in enumerate(_map):
            for x, j in enumerate(''.join(i.split())):
                if j == 'G':
                    interactive_obj.Ground((80 * x, 79 * y), screen, interactive_obj.ground_first)


set_map()
while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        M = pygame.mouse.get_pressed()
        motion = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Перемещение по меню паузы
            if event.key == pygame.K_s and player.pause:
                resume_color, exit_color = exit_color, resume_color
                select_button_options += 1
                if select_button_options > 1:
                    select_button_options = 0
            elif event.key == pygame.K_w and player.pause:
                resume_color, exit_color = exit_color, resume_color
                select_button_options -= 1
                if select_button_options < 0:
                    select_button_options = 1
            if event.key == pygame.K_ESCAPE:
                player.paus()

            # Выбор опции
            if event.key == pygame.K_e and player.pause:
                if buttons_option[select_button_options] == 'exit':
                    running = False
                if buttons_option[select_button_options] == 'resume':
                    player.pause = False
            # Окрашивание выбраной опции

        # Перемещение курсора
        if event.type == pygame.MOUSEMOTION and not cursor.have_target:
            cursor.rect.topleft = event.pos

        # Реакция на нажатие мыши
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

        # Анимация бега
        if event.type == STEP_EVENT and not player.pause:
            player.do_step()

        # Откат атаки у мобов
        if event.type == HIT_EVENT and not player.pause:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True

        # Анимация вращения монетки
        if event.type == COIN_FLIP and not player.pause:
            for sprite in coin_sprite:
                sprite.update()

        # Готовность способности
        if event.type == ABILITY_READY and not player.pause:
            ABILITY = True
            pygame.time.set_timer(ABILITY_READY, 0)

        # Завершение способности
        if event.type == ABILITY_TIME and not player.pause:
            pygame.time.set_timer(ABILITY_TIME, 0)
            pygame.time.set_timer(ABILITY_READY, 3000)
            time_resume.set_volume(0.2)
            time_resume.play(loops=0, maxtime=0, fade_ms=120)
            player.the_world()
            player.velocity = SPEED

        if event.type == pygame.KEYDOWN and not player.pause:
            # Использование способности
            if event.key == pygame.K_x and ABILITY:
                bar = True
                ABILITY = False
                player.the_world()
                the_world.set_volume(0.2)
                the_world.play(loops=0, maxtime=0, fade_ms=120)
                pygame.time.set_timer(ABILITY_TIME, 5300)
                player.velocity *= 0.3
            # Ускорение
            if event.key == pygame.K_LSHIFT and not block and not player.pause:
                sprint = True
            # Хил
            if event.key == pygame.K_q:
                heal = True
            # Блок
            if event.key == pygame.K_f and not sprint:
                block = True
                player.velocity -= 0.5
            # jump
            if event.key == pygame.K_SPACE and player.check_collide_with_ground():
                player.can_jump_flag = True
                player.stamina -= 33

        if event.type == pygame.KEYUP and not player.pause:
            # Отмена ускорения
            if event.key == pygame.K_LSHIFT:
                sprint = False
            # Отмена хила
            if event.key == pygame.K_q:
                heal = False
            # Отмена блока
            if event.key == pygame.K_f and block:
                block = False
                player.block = False
                player.velocity += 0.5

    if sprint and player.stamina > 0:
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
    if player.can_jump_flag:
        player.jump()

    # Перемещение
    if KEY[pygame.K_d]:
        player.move_right()
    if KEY[pygame.K_a]:
        player.move_left()

    # Добавление монеток
    count_coins = player.check_collide_with_coin()

    if motion[0] > player.rect.x and motion[1] >= 0:
        player.left = False
    if motion[0] < player.rect.x and motion[1] >= 0:
        player.left = True

    for mob in mobs_sprite.sprites():
        distance = abs(int(player.rect.centerx) - int(mob.rect.centerx))
        mob.run(distance)
        if not mob.check_collide_with_ground():
            mob.rect = mob.rect.move(0, 4)

    for ball in balls_sprite.sprites():
        ball.move()

    if not player.check_collide_with_ground():
        player.rect = player.rect.move(0, 4)

    if not player.update_render_player:
        if play_sounder == 0:
            play_sounder = 1
            die_hero_sound.set_volume(0.4)
            die_hero_sound.play(loops=0, maxtime=0, fade_ms=120)

    screen.fill(BLACK)
    render()
    if pygame.mouse.get_focused():
        trigger.draw(screen)
    # Фокустровка камеры на персонаже
    camera.update(player)
    # Перемещение объектов относительно персонажа
    for sprite in hero_sprite:
        camera.apply(sprite)
    for sprite in mobs_sprite:
        camera.apply(sprite)
    for sprite in coin_sprite:
        camera.apply(sprite)
    for sprite in balls_sprite:
        camera.apply(sprite)
    for sprite in interactive_obj.ground_first:
        camera.apply(sprite)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
