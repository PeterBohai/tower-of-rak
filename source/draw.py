# Standard library imports

# Third party imports
import pygame
import tcod
import random

# Local project imports
from source import constants
from source import globalvars
from source import text
from source import hud
from source import map

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
    text_coords = (constants.CAMERA_WIDTH/2, constants.CAMERA_HEIGHT/2 - constants.CELL_HEIGHT - 5)
    # clear the surface (filling it with some color, wipe the color out)
    globalvars.SURFACE_MAIN.fill(constants.COLOR_GAME_BG)
    globalvars.SURFACE_MAP.fill(constants.COLOR_GAME_BG)

    globalvars.CAMERA.update_pos()

    # draw the map Surface
    draw_map(globalvars.GAME.current_map)

    # draw all objects (player, creatures, items)
    for obj in globalvars.GAME.current_objects:
        obj.draw()

    # draw little health bar ui on top of visible creatures (that have been hit)
    for objActor in globalvars.GAME.current_objects:
        if objActor.is_visible and objActor.creature:

            if objActor.name_object != "PLAYER":
                objActor.creature.draw_health()

            if objActor.creature.dmg_alpha > 0:
                objActor.creature.draw_damage_taken()

    # draw floor number (title) in the middle for a few seconds when floor changes and when game first starts
    if globalvars.GAME.floor_transition_alpha > 0:
        draw_floor_num_title(change_alpha=False)

    # Display map onto main game screen window
    globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)

    # Draw fps message and floor number
    debug_pos_x = draw_debug()

    # Draw floor number
    floor_font = constants.FONT_BEST_18
    if globalvars.GAME.cur_floor == constants.MAP_MAX_NUM_FLOORS:
        floor_text = f"{globalvars.GAME.cur_floor}F [final]"
    else:
        floor_text = f"{globalvars.GAME.cur_floor}F"
    floor_x = debug_pos_x - text.helper_text_width(floor_font, floor_text) - 10
    text.draw_text(globalvars.SURFACE_MAIN, floor_text,
                   floor_font, (floor_x, 0), pygame.Color('aquamarine1'))

    # HUD draw functions
    hud.draw_player_health(globalvars.SURFACE_MAIN, (10, 10), globalvars.PLAYER.creature.get_health_percentage())

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

            wall_num = map_to_draw[x][y].wall_assignment
            floor_num = map_to_draw[x][y].floor_assignment

            is_visible = tcod.map_is_in_fov(globalvars.FOV_MAP, x, y)      # to check whether or not a tile is visible
            index = map_to_draw[x][y].floor_rand_index
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path is True:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.wall_dict[wall_num],
                                                (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                else:
                    if floor_num in (0, 1, 2, 4, 8):
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_dict[floor_num][index],
                                                    (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    else:
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_dict[floor_num],
                                                    (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            else:
                if map_to_draw[x][y].explored:

                    if map_to_draw[x][y].block_path is True:
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.wall_explored_dict[wall_num],
                                                    (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                    else:
                        if floor_num in (0, 1, 2, 4, 8):
                            globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_explored_dict[floor_num][index],
                                                        (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                        else:
                            globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_explored_dict[floor_num],
                                                        (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))



            # else if not visible:
                # the background fill color of the surface being drawn on is displayed (black at the moment)


def draw_debug():
    """Draws the debug console onto the game screen window.

    Draws debug message text to the upper left corner of the screen.
    Displays only the current FPS for now.

    Returns:
        pos_x (int): x-coordinate of debug message

    """

    fps_text = "fps: " + str(int(globalvars.CLOCK.get_fps()))
    pos_x = constants.CAMERA_WIDTH - text.helper_text_width(constants.FONT_BEST, fps_text) - 5
    pos_y = 0

    text.draw_text(globalvars.SURFACE_MAIN, fps_text,
                   constants.FONT_BEST, (pos_x, pos_y), constants.COLOR_WHITE)

    return pos_x


def draw_messages():
    """Draws the message console to the game screen window.

    Displays a max number of messages from the game's list of messages stored in globalvars.GAME.message_history
    in sequence to the lower left corner of the screen. The order of messages starts at the bottom with the most
    recent message.

    Returns:
        None

    """
    if len(globalvars.GAME.message_history) <= constants.NUM_MESSAGES:
        globalvars.GAME.message_history = globalvars.GAME.message_history   # the last 4 messages in the list
    else:
        del globalvars.GAME.message_history[0]
        # globalvars.GAME.message_history = globalvars.GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = text.helper_text_height(constants.FONT_BEST)
    text_x = 10
    start_y = constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height) - 16

    for i, (message, color) in enumerate(globalvars.GAME.message_history):

        text.draw_text(globalvars.SURFACE_MAIN, message, constants.FONT_BEST,
                       (text_x, start_y + (i * text_height)), color, constants.COLOR_GAME_BG)


def draw_tile_rect(display_surface, tile_coords, color, alpha=150, mark=False):

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
        display_surface.blit(new_surface, (map_x, map_y))
        display_surface.blit(globalvars.ASSETS.S_TARGET_MARK, (map_x, map_y))
    else:
        display_surface.blit(new_surface, (map_x, map_y))


def draw_floor_num_title(text_color=pygame.Color('aquamarine1'), font=constants.FONT_BEST_20, change_alpha=True):

    text_coords = (constants.CAMERA_WIDTH/2, constants.CAMERA_HEIGHT/2 - constants.CELL_HEIGHT - 5)
    floor_num = globalvars.GAME.cur_floor

    alpha_val = globalvars.GAME.floor_transition_alpha
    floor_text = f"Floor - {floor_num}"

    # dont need to change alpha value here since the main game loop does it
    if change_alpha:
        globalvars.GAME.floor_transition_alpha = text.draw_fading_text(globalvars.SURFACE_MAIN, floor_text, font,
                                                                        text_coords, text_color, alpha_val, center=True)
    else:
        text.draw_fading_text(globalvars.SURFACE_MAIN, floor_text, font,
                              text_coords, text_color, alpha_val, speed=1, center=True)


def fade_to_solid(width, height, redraw_func, redraw_args, color=pygame.Color('black')):

    fade_surface = pygame.Surface((width, height))
    fade_surface.fill(color)
    for alpha in range(0, 303, 3):
        fade_surface.set_alpha(alpha)

        # redraw background while fading
        redraw_func(redraw_args)

        globalvars.SURFACE_MAIN.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(0)
