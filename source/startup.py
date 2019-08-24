import pygame
import tcod

from source import constants, globalvars, game, data, camera, assets


def game_initialize():
    """Initializes the main game window and other game assets.

    Initializes pygame, the main surface (game window), ObjGame, clock (time tracker), ObjAssets, and PLAYER.
    Globalizes important variable constants.

    """

    # initialize pygame mixer in a way that prevents the sound delays
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.mixer.quit()
    pygame.mixer.pre_init(44100, -16, 2, 1024)

    # doesn't set dock icon when running
    icon = pygame.image.load("data/graphics/rak_icon.png")
    pygame.display.set_icon(icon)

    # initialize pygame
    pygame.init()
    pygame.key.set_repeat(165, 85)  # (delay, interval) in milliseconds for movement when holding down keys

    try:
        game.preferences_load()

    except FileNotFoundError:
        globalvars.PREFERENCES = data.StructPreferences()

    # Parse name generation files
    tcod.namegen_parse("data/namegen/jice_fantasy.cfg")

    pygame.display.set_caption("Tower of Rak")

    # displays the pygame window
    if globalvars.PREFERENCES.display_window == "default":
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    elif globalvars.PREFERENCES.display_window == "fill":
        constants.CAMERA_WIDTH = constants.screen_width
        constants.CAMERA_HEIGHT = constants.screen_height - 45
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    elif globalvars.PREFERENCES.display_window == "fullscreen":
        constants.CAMERA_WIDTH = constants.screen_width
        constants.CAMERA_HEIGHT = constants.screen_height
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT),
                                                          flags=pygame.FULLSCREEN)

    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # surface of entire map
    globalvars.SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    globalvars.CAMERA = camera.ObjCamera()

    globalvars.ASSETS = assets.ObjAssets()

    globalvars.CLOCK = pygame.time.Clock()

    globalvars.FOV_CALCULATE = True

    globalvars.FLOOR_CHANGED = False
