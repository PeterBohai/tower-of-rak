import tcod
import pygame

pygame.init()

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32  # because of the size of the sprite character's png


# FPS LIMIT
GAME_FPS = 60


# MAP VARS (39 X 23)
MAP_WIDTH = 38
MAP_HEIGHT = 22


# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (66, 167, 244)
COLOR_YELLOW = (255, 233, 147)
COLOR_ORANGE = (255, 155, 84)


# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# FOV SETTINGS

FOV_ALG = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

# MESSAGE DEFAULTS
NUM_MESSAGES = 6
MSG_WIDTH = 600

# FONTS
FONT_DEBUG_MESSAGE = pygame.font.Font('data/fonts/LiberationMono-Regular.ttf', 20)
FONT_DEBUG_MESSAGE2 = pygame.font.Font('data/fonts/AppleII.ttf', 16)
FONT_BEST = pygame.font.Font('data/fonts/fixedsys300.ttf', 16)
FONT_TARGET_X = pygame.font.Font('data/fonts/fixedsys300.ttf', CELL_HEIGHT + 10)
