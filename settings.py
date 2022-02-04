import pygame
from win32api import GetSystemMetrics

# WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), 32, 32)
FPS = 59
SPEED = 7.5
PIXEL_SEC = 10

KEY = None
KD = 4000

STATUS_BAR_HEALTH_FULL_COLOR = 100, 172, 15
CRIMSON = 140, 0, 15
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
DARK_GREEN = 0, 155, 0
BLUE = 0, 0, 255
LIGHT_BLUE = 60, 170, 255
DARK_BLUE = 0, 33, 55
GRAY = 128, 128, 128
SILVER = 192, 192, 192
YELLOW = 255, 170, 0
BACKGROUND = 69, 68, 89

STATS_MOB_SLIME = {'1': (14, 14*3), '2': (28, 14*5), '3': (14, 14*7)}
STEP_MOBS_BEFORE_DIED = ['UP', 'RIGHT', 'LEFT', 'DOWN']
with open('data.txt', 'r') as stats:
    stats = stats.readlines()
    HERO_LVL = int(stats[1])
    default_DAMAGE_PLAYER = 14 + 4 * HERO_LVL
default_HEALTH_PLAYER = 100
default_HEALTH_MOB = 56
ENDURANCE = 200
JUMP_Y = 17
