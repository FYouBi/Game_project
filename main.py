import pygame
from settings import *
from hero import Hero

pygame.init()

STEP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(STEP_EVENT, 230)

# font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
hero_sprite = pygame.sprite.Group()
player = Hero(hero_sprite)
RECTANGLE = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 20, 130))
running = True
while running:
    for event in pygame.event.get():
        KEY = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == STEP_EVENT:
            player.do_step()
        # player.stay()

    if KEY[pygame.K_d]:
        player.move_right()
    if KEY[pygame.K_a]:
        player.move_left()
    if KEY[pygame.K_w]:
        player.move_up()
    if KEY[pygame.K_s]:
        player.move_down()
    if KEY[pygame.K_f]:
        player.hit()

    FPS_LOOK = str(int(clock.get_fps()))
    print(FPS_LOOK)
    # render = font.render(FPS_LOOK, 0, (255, 0, 0))
    # screen.blit(render, (0, 0))
    screen.fill((50, 100, 0))
    hero_sprite.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
