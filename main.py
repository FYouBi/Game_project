import hero_and_mobs
import interactive_obj
import datetime
from cam import Camera
from cursor import cursor, trigger
import func_rotate
from hero_and_mobs import player, hero_sprite, mobs_sprite, balls_sprite
from settings import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 200)

HIT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(HIT_EVENT, 2500)

ABILITY_READY = pygame.USEREVENT + 4
pygame.time.set_timer(ABILITY_READY, 15000)
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
select_lvl = True
win_cycle = False
death = False
sprint = False
block = False
width_batery_color = 0
stamina = ENDURANCE
auto_aim = 0
die_hero_sound = pygame.mixer.Sound('sounds/dead.wav')
hit_hero_sound = pygame.mixer.Sound('sounds/hit.wav')
the_world = pygame.mixer.Sound('sounds/the_world.wav')
time_resume = pygame.mixer.Sound('sounds/time_resumes.wav')
play_sounder = 0
pygame.mixer.music.load(f'sounds/sounds_back_music.mp3')
pygame.mixer.music.play(-1, 0, 100)
pygame.mixer.music.set_volume(0.3)
status_image = pygame.image.load(f'images/hud_hp_stamina_medic-export.png').convert_alpha(screen)
battery = pygame.image.load(f'images/battery-export.png').convert_alpha(screen)
weapon = pygame.image.load(f'images/weapon.png').convert_alpha(screen)
weapon = pygame.transform.scale(weapon, (136, 6))
heal = False
count_coins = 0
pause = False
right = True
confirmation_exit = False
select_button_options = 0
bg = pygame.image.load(f'images/fon.png').convert_alpha(screen)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
buttons_option = ['resume', 'exit']
with open('data/data.txt', 'r') as data:
    data = data.readlines()[0].split()
    print(data)
    levels = [[1, int(data[0]), 1], [2, int(data[1]), 10], [3, int(data[2]), 18]]
render_update = True
resume_color = [DARK_GREEN, GREEN]
exit_color = [CRIMSON, RED]
screen_rect = (0, 0, WIDTH, HEIGHT)
current_lvl = 0
speed_attack = SPEED_ATTACK
motion = [0, 0]
mob_count = 7
final_angle = 360
angle = 0
damage_count = 0
accepted_damage = 0
hero_lvl = HERO_LVL
begin_time = datetime.timedelta(minutes=0, seconds=0)
finish_time = datetime.timedelta(minutes=0, seconds=0)
current_time = datetime.timedelta(minutes=0, seconds=0)


def save():
    with open('data/data.txt', 'w') as data:
        str_ = ['1' if i[1] else '0' for i in levels]
        data.write(' '.join(str_) + '\n')
        data.write(str(hero_lvl))


def render():
    global PIXEL_SEC, width_batery_color, bar, count_coins, angle
    # Отрисовка спрайтов
    screen.blit(bg, (0, 0))
    interactive_obj.ground_first.draw(screen)
    interactive_obj.aid_kit.draw(screen)
    interactive_obj.coin_sprite.draw(screen)
    interactive_obj.particle_sprite.draw(screen)
    func_rotate.blitRotate(screen, weapon, (player.rect.topleft[0] + 20, player.rect.topleft[1] + 30), (0, 0), angle)
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
    pygame.draw.rect(screen, LIGHT_BLUE, (6, 35, player.stamina // 2, 10))

    font_FPS = pygame.font.Font('fonts/pixel_font.otf', 26)

    if player.update_render_player:
        if width_batery_color <= 75 and not ABILITY and not bar:
            width_batery_color += PIXEL_SEC / FPS
        elif width_batery_color >= 0 and bar:
            width_batery_color -= PIXEL_SEC / FPS * 2.6

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

    font = pygame.font.Font('fonts/pixel_font.otf', 26)
    render_die = font.render(f'{mob_count}/7', False, WHITE)
    screen.blit(render_die, (WIDTH // 2 - 5, 20))

    score = font.render(f'{str(current_time - begin_time)[2:]}', False, SILVER)
    screen.blit(score, (WIDTH // 2 - 23, 100))

    if death:
        font_died = pygame.font.Font('fonts/pixel_font.otf', 126)
        render_die = font_died.render('Ты умер', False, CRIMSON)
        screen.blit(render_die, (WIDTH//3, HEIGHT // 3.5))
        font_died = pygame.font.Font('fonts/pixel_font.otf', 33)
        render_die = font_died.render('НАЖМИТЕ "SPACE" ЧТОБЫ ВОЗРОДИТЬСЯ', False, SILVER)
        screen.blit(render_die, (WIDTH//3, HEIGHT // 2))
        font_died = pygame.font.Font('fonts/pixel_font.otf', 33)
        render_die = font_died.render('НАЖМИТЕ "E" ЧТОБЫ ВЕРНУТЬСЯ НА ВЫБОР УРОВНЯ', False, SILVER)
        screen.blit(render_die, (WIDTH//3, HEIGHT // 1.7))
        font_died = pygame.font.Font('fonts/pixel_font.otf', 33)
        render_die = font_died.render('НАЖМИТЕ "ESC" ЧТОБЫ ВЫЙТИ ИЗ ИГРЫ', False, SILVER)
        screen.blit(render_die, (WIDTH//3, HEIGHT // 1.5))

    if win_cycle:
        font = pygame.font.Font('fonts/pixel_font.otf', 33)
        score = font.render('СЧЕТ:', False, YELLOW)
        screen.blit(score, (WIDTH // 2 - 35, HEIGHT // 3))
        score = font.render(f'НАНЕСЕННЫЙ УРОН:    {damage_count}', False, YELLOW)
        screen.blit(score, (WIDTH // 2 - 175, HEIGHT // 2.5))
        score = font.render(f'ПОЛУЧЕННЫЙ УРОН    {accepted_damage}', False, YELLOW)
        screen.blit(score, (WIDTH // 2 - 175, HEIGHT // 2.2))
        score = font.render(f'ОЧКИ    {count_coins}', False, YELLOW)
        screen.blit(score, (WIDTH // 2 - 45, HEIGHT // 2))
        score = font.render(f'ВРЕМЯ {str(finish_time - begin_time)[2:]}', False, YELLOW)
        screen.blit(score, (WIDTH // 2 - 85, HEIGHT // 1.7))
        if levels[current_lvl][0] == 0:
            score = font.render('ПОЗДРАВЛЯЕМ, ВЫ ПРОШЛИ ИГРУ:', False, YELLOW)
            screen.blit(score, (WIDTH // 1.5, HEIGHT // 4))
            score = font.render('ЧТОБЫ ВЕРНУТьСЯ НА ВЫБОР УРОВНЯ НАЖМИТЕ "SPACE"', False, YELLOW)
            screen.blit(score, (WIDTH // 3 - 45, HEIGHT // 1.6 + 20))
        else:
            score = font.render('ЧТОБЫ ПРОДОЛЖИТЬ НАЖМИТЕ "SPACE"', False, YELLOW)
            screen.blit(score, (WIDTH//3 - 15, HEIGHT // 1.6 + 20))

    if player.pause:
        pygame.mixer.music.set_volume(0.1)
        font_pause = pygame.font.Font('fonts/pixel_font.otf', 100)
        text = font_pause.render(f'ПРОДОЛЖИТЬ', True, resume_color[0])
        screen.blit(text, (WIDTH // 2 - 310, HEIGHT // 2 - 95))
        text = font_pause.render(f'ПРОДОЛЖИТЬ', True, resume_color[1])
        screen.blit(text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))
        font_pause = pygame.font.Font('fonts/pixel_font.otf', 86)
        text = font_pause.render(f'ВЫЙТИ ИЗ ИГРЫ', True, exit_color[0])
        screen.blit(text, (WIDTH // 2 - 320, HEIGHT // 2 + 5))
        text = font_pause.render(f'ВЫЙТИ ИЗ ИГРЫ', True, exit_color[1])
        screen.blit(text, (WIDTH // 2 - 310, HEIGHT // 2))
        font_pause = pygame.font.Font('fonts/pixel_font.otf', 26)
        text = font_pause.render(f'НАЖМИТЕ "SPACE" ЧТОБЫ ВЕРНУТЬСЯ НА ВЫБОР УРОВНЯ', True, SILVER)
        screen.blit(text, (WIDTH//3, HEIGHT - 100))
    else:
        pygame.mixer.music.set_volume(0.6)
    screen.blit(status_image, (5, 5))
    screen.blit(battery, (WIDTH - 100, 10))
    font_version = pygame.font.Font('fonts/pixel_font.otf', 26)
    text = font_version.render(f'0.0.9', True, SILVER)
    screen.blit(text, (WIDTH // 2, HEIGHT - 30))
    lvl = font_version.render(f'{str(hero_lvl)}', True, (255, 255, 255))
    pygame.draw.line(screen, (255, 255, 255), [20, 64], [20, 87], 2)
    pygame.draw.line(screen, (255, 255, 255), [15, 64], [15, 87], 2)
    screen.blit(lvl, (10, 80))


def select_levels(current):
    font_pause = pygame.font.Font('fonts/pixel_font.otf', 100)
    text = font_pause.render(f'\nLEVELS\n', True, (11, 122, 96))
    screen.blit(text, (WIDTH // 2.7, HEIGHT // 7))

    font_pause = pygame.font.Font('fonts/pixel_font.otf', 124)
    text = font_pause.render(f'\n', True, (72, 153, 95) if current[1] else (140, 13, 42))
    screen.blit(text, (WIDTH // 2.7 + 23 * current[2], HEIGHT // 2.5))

    font_pause = pygame.font.Font('fonts/pixel_font.otf', 100)
    text = font_pause.render(f'1    2   3', True, (75, 2, 92))
    screen.blit(text, (WIDTH // 2.7 + 45, HEIGHT // 2.5 + 10))

    font_pause = pygame.font.Font('fonts/pixel_font.otf', 76)
    text = font_pause.render(f'ВЫБРАТЬ', True, (72, 153, 95) if current[1] else (140, 13, 42))
    screen.blit(text, (WIDTH // 2.4, HEIGHT // 1.5))


def set_map(lvl):
    interactive_obj.ground_first.empty()
    interactive_obj.aid_kit.empty()
    interactive_obj.coin_sprite.empty()
    interactive_obj.particle_sprite.empty()
    balls_sprite.empty()
    mobs_sprite.empty()
    with open(f'data/map{lvl}.txt', 'r') as _map:
        for y, i in enumerate(_map):
            for x, j in enumerate(i.split()):
                if j == 'G':
                    interactive_obj.Ground((81 * x, 79 * y), screen, interactive_obj.ground_first)
                elif j == 'A':
                    interactive_obj.AidKit((81 * x, 79 * y), interactive_obj.aid_kit)
                elif j == 'S':
                    hero_and_mobs.Slime((81 * x, 79 * y), f'{lvl}', mobs_sprite)


def reset_player(flag):
    global mob_count, damage_count, accepted_damage, count_coins, hero_lvl, angle, \
        final_angle, begin_time, finish_time, current_time
    player.stamina = 200
    player.heal = 100
    player.health = 100
    angle = 0
    final_angle = 360
    player.rotate = False
    player.pause = False
    player.rect.x, player.rect.y = 100, 100
    mob_count = 7
    damage_count = 0
    accepted_damage = 0
    count_coins = player.coin_count = 0
    begin_time = datetime.timedelta(minutes=0, seconds=0)
    finish_time = datetime.timedelta(minutes=0, seconds=0)
    current_time = datetime.timedelta(minutes=0, seconds=0)
    if flag:
        time = datetime.datetime.now()
        begin_time = datetime.timedelta(minutes=time.minute, seconds=time.second)
        hero_lvl += count_coins // 100
        player.damage = 14 + 4 * hero_lvl


def death_screen():
    global death, KEY, running, select_lvl
    while death:
        for event in pygame.event.get():
            KEY = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                save()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    death = False
                    player.update_render_player = True
                    select_lvl = True
                    reset_player(False)
                    set_map(levels[current_lvl][0])
                if event.key == pygame.K_e:
                    running = True
                    death = False
                    player.update_render_player = True
                    select_lvl = True
                    reset_player(False)
                    select_lvl_func()
                if event.key == pygame.K_ESCAPE:
                    exit()
        screen.fill(BLACK)
        render()
        pygame.display.update()


def select_lvl_func():
    global select_lvl, current_lvl, KEY, running, begin_time, count_coins
    count_coins = player.coin_count = 0
    while select_lvl:
        for event in pygame.event.get():
            KEY = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                save()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    current_lvl += 1 if current_lvl < 2 else -2
                if event.key == pygame.K_a:
                    current_lvl += -1 if current_lvl > 0 else 2
                if event.key == pygame.K_e and levels[current_lvl][1]:
                    set_map(levels[current_lvl][0])
                    select_lvl = False
                    running = True
                    time = datetime.datetime.now()
                    begin_time = datetime.timedelta(minutes=time.minute, seconds=time.second)
        screen.fill(BLACK)
        select_levels(levels[current_lvl])
        pygame.display.update()


def win():
    global win_cycle, current_lvl, KEY, running, select_lvl
    while win_cycle:
        for event in pygame.event.get():
            KEY = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                save()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if levels[current_lvl][0] != 3:
                        reset_player(True)
                        running = True
                        current_lvl += 1
                        levels[current_lvl][1] = True
                        set_map(levels[current_lvl][0])
                        win_cycle = False
                    else:
                        win_cycle = False
                        select_lvl = True
                        select_lvl_func()
        screen.fill(BLACK)
        render()
        pygame.display.update()


select_lvl_func()

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
            elif event.key == pygame.K_SPACE and player.pause:
                running = False
                select_lvl = True
                reset_player(False)
                select_lvl_func()
            if event.key == pygame.K_ESCAPE:
                player.paus()

            # Выбор опции
            if event.key == pygame.K_e and player.pause:
                if buttons_option[select_button_options] == 'exit':
                    save()
                    running = False
                if buttons_option[select_button_options] == 'resume':
                    player.pause = False

        # Перемещение курсора
        if event.type == pygame.MOUSEMOTION and not cursor.have_target:
            cursor.rect.topleft = event.pos

        # Реакция на нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.pause and not player.rotate:
                if player.stamina >= 36:
                    if player.update_render_player:
                        hit_hero_sound.set_volume(0.2)
                        hit_hero_sound.play(loops=0, maxtime=0, fade_ms=12)
                c = player.hit(cursor)
                mob_count -= c
                damage_count += default_DAMAGE_PLAYER * c

        # Анимация бега
        if event.type == STEP_EVENT and not player.pause:
            player.update()

        # Откат атаки у мобов
        if event.type == HIT_EVENT and not player.pause:
            for mob in mobs_sprite.sprites():
                mob.can_hit = True

        # Анимация вращения монетки
        if event.type == COIN_FLIP and not player.pause:
            if not player.time_stop:
                for sprite in interactive_obj.coin_sprite:
                    if sprite.coin:
                        sprite.update()
                for sprite in mobs_sprite:
                    sprite.update()

        # Готовность способности
        if event.type == ABILITY_READY and not player.pause:
            ABILITY = True
            pygame.time.set_timer(ABILITY_READY, 0)

        # Завершение способности
        if event.type == ABILITY_TIME and not player.pause:
            bar = False
            pygame.time.set_timer(ABILITY_TIME, 0)
            pygame.time.set_timer(ABILITY_READY, 15000)
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
                pygame.time.set_timer(ABILITY_TIME, 5000)
                player.velocity *= 0.3
            # Ускорение
            if event.key == pygame.K_LSHIFT and not block and not player.pause:
                sprint = True
            # Хил
            if event.key == pygame.K_q:
                heal = True
            # jump
            if event.key == pygame.K_SPACE and player.check_collide_with_ground():
                player.can_jump_flag = True

        if event.type == pygame.KEYUP and not player.pause:
            # Отмена ускорения
            if event.key == pygame.K_LSHIFT:
                sprint = False
            # Отмена хила
            if event.key == pygame.K_q:
                heal = False

    if sprint and player.stamina > 0:
        player.sprint()
    else:
        player.velocity_dawn()
    if heal:
        player.heal_up()
    if not sprint:
        if player.stamina < 200:
            player.up_stamina()
    if player.can_jump_flag:
        player.jump()

    # Атака
    if player.rotate and not player.pause:
        if final_angle >= 0:
            angle -= 10 / FPS + speed_attack
            final_angle -= 10 / FPS + speed_attack
            player.stamina -= 1.5
        else:
            player.rotate = False
            angle = 0
            final_angle = 360

    if not player.rotate:
        if motion[0] > player.rect.x and motion[1] >= 0:
            angle = -((motion[1] - WIDTH // 3.5) // 12) \
                if abs(-((motion[1] - WIDTH // 3.5) // 12)) <= 90 else angle
        if motion[0] < player.rect.x and motion[1] >= 0:
            angle = ((motion[1] - WIDTH // 3.5) // 12 - 180) \
                if abs(((motion[1] - WIDTH // 3.5) // 12 - 180)) <= 360 else angle

    # Перемещение
    if KEY[pygame.K_d]:
        if player.check_collide_with_ground():
            interactive_obj.create_particles((player.rect.topleft[0], player.rect.topleft[1] + 50))
        player.move_right()
    if KEY[pygame.K_a]:
        if player.check_collide_with_ground():
            interactive_obj.create_particles((player.rect.topright[0], player.rect.topright[1] + 50))
        player.move_left()

    if mob_count == 0:
        win_cycle = True
        running = False
        finish_time = current_time
        win()

    time = datetime.datetime.now()
    current_time = datetime.timedelta(minutes=time.minute, seconds=time.second)

    # Добавление монеток
    count_coins = player.check_collide_with_coin()

    if motion[0] > player.rect.x and motion[1] >= 0:
        if not player.rotate:
            if right:
                angle = 0
                right = False
            player.left = False
    if motion[0] < player.rect.x and motion[1] >= 0:
        if not player.rotate:
            if not right:
                angle = 180
                right = True
            player.left = True

    for sprite in interactive_obj.particle_sprite.sprites():
        sprite.update()

    for mob in mobs_sprite.sprites():
        distance = abs(int(player.rect.centerx) - int(mob.rect.centerx))
        mob.run(distance)
        if not mob.check_collide_with_ground() and not player.time_stop:
            mob.rect = mob.rect.move(0, 13)
            if mob.check_pos_y():
                mobs_sprite.remove(mob)
                mob_count -= 1

    for ball in balls_sprite.sprites():
        accepted_damage += ball.move()
        if ball.rect.x < 0 or ball.rect.x > 10000:
            balls_sprite.remove(ball)

    player.check_collide_with_aid_kit()

    if not player.check_collide_with_ground() and not player.pause:
        player.rect = player.rect.move(0, 13)
        for sprite in interactive_obj.ground_first:
            if sprite.rect.y < -450:
                player.update_render_player = False
            break

    if not player.update_render_player:
        if play_sounder == 0:
            play_sounder = 1
            die_hero_sound.set_volume(0.4)
            die_hero_sound.play(loops=0, maxtime=0, fade_ms=120)
        running = False
        death = True
        death_screen()
    screen.fill(BLACK)
    render()
    if pygame.mouse.get_focused():
        trigger.draw(screen)
    # Фокустровка камеры на персонаже
    camera.update(player)
    # Перемещение объектов относительно персонажа
    for sprite in hero_sprite:
        camera.apply(sprite)
    for sprite in interactive_obj.aid_kit:
        camera.apply(sprite)
    for sprite in mobs_sprite:
        camera.apply(sprite)
    for sprite in interactive_obj.coin_sprite:
        camera.apply(sprite)
    for sprite in balls_sprite:
        camera.apply(sprite)
    for sprite in interactive_obj.ground_first:
        camera.apply(sprite)
    clock.tick(35)
    pygame.display.update()

pygame.quit()
