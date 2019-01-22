
# Third party imports
import pygame
import tcod

# Local project imports
from source import constants, globalvars, game, data, camera, assets


def game_initialize():

    """Initializes the main game window and other game assets.

    Initializes pygame, the main surface (game window), ObjGame, clock (time tracker), ObjAssets, and PLAYER.
    Globalizes important variable constants.

    """

    # initialize pygame
    pygame.init()
    pygame.key.set_repeat(180, 90)  # (delay, interval) in milliseconds for movement when holding down keys

    globalvars.init()

    try:
        game.preferences_load()

    except:
        globalvars.PREFERENCES = data.StructPreferences()

    # Parse name generation files
    tcod.namegen_parse("data/namegen/jice_fantasy.cfg")

    # displays the pygame window
    globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    # surface of entire map
    globalvars.SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    globalvars.CAMERA = camera.ObjCamera()

    globalvars.ASSETS = assets.ObjAssets()

    globalvars.CLOCK = pygame.time.Clock()

    globalvars.FOV_CALCULATE = True

    globalvars.FLOOR_CHANGED = False
