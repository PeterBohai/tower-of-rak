# Standard library imports
import math

# Third party imports
import pygame
import tcod

# Local project imports
from source import constants
from source import globalvars
from source import text

# ================================================================= #
#                        -----  Draw  -----                         #
# ================================================================= #


def draw_game():
    """Main function for drawing the entire game.

    Order of draw operations:
        1) Clear the screen window and map Surface
        2) Update the camera position
        3) Draw the map Surface
        4) Draw all appropriate actor objects onto the map Surface
        5) Render the map Surface onto the screen window
        5) Draw the debug fps message in the top-left corner of the screen window
        6) Draw the player messages on the screen window

    Returns:
        None

    """

    # clear the surface (filling it with some color, wipe the color out)
    globalvars.SURFACE_MAIN.fill(constants.COLOR_BLACK)
    globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)

    globalvars.CAMERA.update_pos()

    # draw the map Surface
    draw_map(globalvars.GAME.current_map)

    # draw the character
    for obj in globalvars.GAME.current_objects:
        obj.draw()

    # Display map onto main game screen window
    globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)

    # Draw fps message
    draw_debug()

    # Draw all player interactive messages
    draw_messages()


def draw_map(map_to_draw):
    """ Draws specified map onto the main globalvars.SURFACE_MAP map Surface.

    Only renders the camera area of the map to prevent performance loss when exploring large maps.

    Args:
        map_to_draw (2D array): Map to be drawn onto globalvars.SURFACE_MAP.

    Returns:
        None

    """

    # render only the visible portion of the map
    cam_tile_x, cam_tile_y = globalvars.CAMERA.map_address

    window_tile_width = int(constants.CAMERA_WIDTH / constants.CELL_WIDTH)
    window_tile_height = int(constants.CAMERA_HEIGHT / constants.CELL_HEIGHT)

    render_min_x = int(cam_tile_x - (window_tile_width / 2))
    render_min_y = int(cam_tile_y - (window_tile_height / 2))

    render_max_x = int(cam_tile_x + (window_tile_width / 2))
    render_max_y = int(cam_tile_y + (window_tile_height / 2))

    if render_min_x < 0:
        render_min_x = 0
    if render_min_y < 0:
        render_min_y = 0
    if render_max_x > constants.MAP_WIDTH:
        render_max_x = constants.MAP_WIDTH
    if render_max_y > constants.MAP_HEIGHT:
        render_max_y = constants.MAP_HEIGHT

    for x in range(render_min_x, render_max_x):
        for y in range(render_min_y, render_max_y):

            is_visible = tcod.map_is_in_fov(globalvars.FOV_MAP, x, y)      # to check whether or not a tile is visible

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path is True:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                else:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            else:
                if map_to_draw[x][y].explored:
                    if map_to_draw[x][y].block_path is True:
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_WALL_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                    else:
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOR_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            # else if not visible:
                # the background fill color of the surface being drawn on is displayed (black at the moment)


def draw_debug():
    """Draws the debug console onto the game screen window.

    Draws debug message text to the upper left corner of the screen.
    Displays only the current FPS for now.

    Returns:
        None

    """

    text.draw_text(globalvars.SURFACE_MAIN, "fps: " + str(int(globalvars.CLOCK.get_fps())), constants.FONT_BEST, (0, 0),
              constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_messages():
    """Draws the message console to the game screen window.

    Displays a max number of messages from the game's list of messages stored in globalvars.GAME.message_history in sequence to
    the lower left corner of the screen. The order of messages starts at the bottom with the most recent message.

    Returns:
        None

    """
    if len(globalvars.GAME.message_history) <= constants.NUM_MESSAGES:
        globalvars.GAME.message_history = globalvars.GAME.message_history   # the last 4 messages in the list
    else:
        del globalvars.GAME.message_history[0]
        # globalvars.GAME.message_history = globalvars.GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = text.helper_text_height(constants.FONT_BEST)
    start_y = constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)

    for i, (message, color) in enumerate(globalvars.GAME.message_history):

        text.draw_text(globalvars.SURFACE_MAIN, message, constants.FONT_BEST, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)


def draw_tile_rect(display_surface, tile_coords, color, alpha=150, mark=None):

    x, y = tile_coords

    # convert map tile coordinates into actual pixel map addresses for proper blitting
    map_x = x * constants.CELL_WIDTH
    map_y = y * constants.CELL_HEIGHT

    # Create a rectangular image/Surface object that's the size of one tile (cell)
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    # fill the Surface with a solid color
    new_surface.fill(color)

    # Draw pixels of this Surface slightly transparent according to value (0 being transparent and 255 being opaque)
    new_surface.set_alpha(alpha)

    if mark:
        text.draw_text(new_surface, mark, constants.FONT_TARGET_X,
                  (constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2),
                  constants.COLOR_BLACK, center=True)

    display_surface.blit(new_surface, (map_x, map_y))