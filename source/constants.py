# Third party imports
import tcod
import pygame

pygame.init()

# GAME SIZES
CELL_WIDTH = 32
CELL_HEIGHT = 32  # because of the size of the sprite character's png

CAMERA_WIDTH_DEFAULT = 900  # 900
CAMERA_HEIGHT_DEFAULT = 700 # 650

game_info = pygame.display.Info()
screen_width = game_info.current_w
screen_height = game_info.current_h

CAMERA_WIDTH = CAMERA_WIDTH_DEFAULT
CAMERA_HEIGHT = CAMERA_HEIGHT_DEFAULT

# FPS LIMIT
GAME_FPS = 60


# MAP VARS (39 X 23)
MAP_WIDTH = 50
MAP_HEIGHT = 50
MAP_MAX_NUM_ROOMS = 3
MAP_MAX_NUM_FLOORS = 3


# ROOM LIMITS
ROOM_MAX_HEIGHT = 9
ROOM_MAX_WIDTH = 9

ROOM_MIN_HEIGHT = 5
ROOM_MIN_WIDTH = 5


# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (70, 70, 70)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_GRASS_GREEN = (48, 194, 53)

COLOR_BLUE = (66, 167, 244)
COLOR_BLUE1 = (114, 156, 224)
COLOR_BLUE1_LIGHTER = (151, 185, 240)
COLOR_BLUE2 = (45, 95, 175)
COLOR_BLUE3 = (33, 70, 130)
COLOR_GREYBLUE1 = (59, 83, 122)
COLOR_GREYBLUE2 = (34, 51, 77)

COLOR_FORREST_GREEN1 = (58, 94, 63)
COLOR_FORREST_GREEN2 = (36, 59, 39)
COLOR_HP_GREEN = (88, 168, 135)
COLOR_HP_YELLOW = (214, 209, 66)
COLOR_HP_RED = (242, 65, 65)

COLOR_YELLOW = (255, 233, 147)
COLOR_YELLOW_2 = (255, 247, 18)
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
FONT_DEBUG_MESSAGE2 = pygame.font.Font('data/fonts/AppleII.ttf', 16)

FONT_GAME_TITLE = pygame.font.Font('data/fonts/Future_TimeSplitters.otf', 60)

FONT_PLAYER_DEATH = pygame.font.Font('data/fonts/fixedsys300.ttf', 50)

FONT_BEST = pygame.font.Font('data/fonts/fixedsys300.ttf', 16)

FONT_MENU_TITLE = pygame.font.Font('data/fonts/fixedsys300.ttf', 20)
FONT_MENU_TITLE.set_underline(True)

FONT_TARGET_X = pygame.font.Font('data/fonts/fixedsys300.ttf', CELL_HEIGHT + 10)

FONT_CREDITS = pygame.font.SysFont('arial', 14)

FONT_CREDIT_LABELS = pygame.font.SysFont('data/fonts/fixedsys300.ttf', 20)

