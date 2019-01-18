import tcod
import pygame

pygame.init()

# GAME SIZES
CELL_WIDTH = 32
CELL_HEIGHT = 32  # because of the size of the sprite character's png

CAMERA_WIDTH = 900
CAMERA_HEIGHT = 650


# FPS LIMIT
GAME_FPS = 60


# MAP VARS (39 X 23)
MAP_WIDTH = 50
MAP_HEIGHT = 50
MAP_MAX_NUM_ROOMS = 10


# ROOM LIMITS
ROOM_MAX_HEIGHT = 9
ROOM_MAX_WIDTH = 9

ROOM_MIN_HEIGHT = 5
ROOM_MIN_WIDTH = 5


# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (66, 167, 244)
COLOR_YELLOW = (255, 233, 147)
COLOR_ORANGE = (255, 155, 84)
COLOR_BROWN = (213, 178, 171)


# Game colors


# FOV SETTINGS

FOV_ALG = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5

# MESSAGE DEFAULTS
NUM_MESSAGES = 6
MSG_WIDTH = 600

# FONTS
FONT_DEBUG_MESSAGE = pygame.font.Font('data/fonts/LiberationMono-Regular.ttf', 20)
FONT_DEBUG_MESSAGE2 = pygame.font.Font('data/fonts/AppleII.ttf', 16)
FONT_GAME_TILE = pygame.font.Font('data/fonts/Future_TimeSplitters.otf', 60)
FONT_BEST = pygame.font.Font('data/fonts/fixedsys300.ttf', 16)
FONT_MENU_TITLE = pygame.font.Font('data/fonts/fixedsys300.ttf', 20)
FONT_TARGET_X = pygame.font.Font('data/fonts/fixedsys300.ttf', CELL_HEIGHT + 10)
