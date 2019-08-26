import pygame
import tcod

from src import constants, globalvars, text, hud


def draw_game():
    """Main function for drawing the entire game.

    Order of draw operations:
        1) Clear the screen window and map Surface
        2) Update the camera position
        3) Draw the map Surface
        5) Render the map Surface onto the screen window
        5) Draw all window ui such as fps, floor num, player health

    Returns
    -------
    None

    """
    globalvars.SURFACE_MAIN.fill(constants.COLOR_GAME_BG)
    globalvars.SURFACE_MAP.fill(constants.COLOR_GAME_BG)

    globalvars.CAMERA.update_pos()

    draw_map(globalvars.GAME.current_map)

    globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)

    draw_window_ui()


def draw_map(target_map):
    """Draws the desired `map` (floor, walls, all objects) onto the the map display surface SURFACE_MAP.

    Only the camera area of the map is rendered to prevent performance loss on large maps.

    Parameters
    ----------
    target_map : list
        Map (nested list) to be drawn onto SURFACE_MAP

    Returns
    -------
    None

    """

    # render only the visible portion of the map
    cam_grid_x, cam_grid_y = globalvars.CAMERA.map_address

    cam_grid_width = int(constants.CAMERA_WIDTH / constants.CELL_WIDTH)
    cam_grid_height = int(constants.CAMERA_HEIGHT / constants.CELL_HEIGHT)

    render_min_x = int(cam_grid_x - (cam_grid_width / 2))
    render_min_y = int(cam_grid_y - (cam_grid_height / 2))

    render_max_x = int(cam_grid_x + (cam_grid_width / 2))
    render_max_y = int(cam_grid_y + (cam_grid_height / 2))

    if render_min_x < 0:
        render_min_x = 0
    if render_min_y < 0:
        render_min_y = 0
    if render_max_x > constants.MAP_WIDTH:
        render_max_x = constants.MAP_WIDTH
    if render_max_y > constants.MAP_HEIGHT:
        render_max_y = constants.MAP_HEIGHT

    # draw floor and walls
    for x in range(render_min_x, render_max_x):
        for y in range(render_min_y, render_max_y):

            wall_num = target_map[x][y].wall_assignment
            floor_num = target_map[x][y].floor_assignment

            is_visible = tcod.map_is_in_fov(globalvars.FOV_MAP, x, y)
            index = target_map[x][y].floor_rand_index
            if is_visible:
                target_map[x][y].explored = True

                if target_map[x][y].block_path is True:
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
                if target_map[x][y].explored:

                    if target_map[x][y].block_path is True:
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.wall_explored_dict[wall_num],
                                                    (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                    else:
                        if floor_num in (0, 1, 2, 4, 8):
                            globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_explored_dict[floor_num][index],
                                                        (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                        else:
                            globalvars.SURFACE_MAP.blit(globalvars.ASSETS.floor_explored_dict[floor_num],
                                                        (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

    # draw all objects onto the map
    for obj in globalvars.GAME.current_objects:
        obj.draw()

    # draw little health bar ui and damage taken values on visible mobs
    for objActor in globalvars.GAME.current_objects:
        if objActor.is_visible and objActor.creature:
            if objActor is not globalvars.PLAYER:
                objActor.creature.draw_health()

            if objActor.creature.dmg_alpha > 0:
                objActor.creature.draw_damage_taken()


def draw_window_ui():
    """Draws all the hud locked onto the screen window and not the map (floor num, fps, PLAYER health, msgs).

    Returns
    -------
    None

    """

    # draw floor number (title) in the middle for a few seconds when floor changes and when game first starts
    if globalvars.GAME.floor_transition_alpha > 0:
        hud.draw_floor_title(change_alpha=False)

    # Draw fps message
    debug_pos_x = hud.draw_fps()

    # Draw floor number
    floor_font = constants.FONT_BEST_18
    if globalvars.GAME.cur_floor != constants.MAP_MAX_NUM_FLOORS:
        floor_text = f"{globalvars.GAME.cur_floor}F"
    else:
        floor_text = f"{globalvars.GAME.cur_floor}F [final]"

    floor_x = debug_pos_x - text.get_text_width(floor_font, floor_text) - 10
    text.draw_text(globalvars.SURFACE_MAIN, floor_text,
                   floor_font, (floor_x, 0), pygame.Color('aquamarine1'))

    # draw PLAYER health bar
    hud.draw_player_health(globalvars.SURFACE_MAIN, (10, 10), globalvars.PLAYER.creature.get_health_percentage())

    # draw PLAYER messages
    hud.draw_messages()


def draw_one_tile(display_surface, tile_coords, color, alpha=150, mark=False):
    """Covers one tile grid on the map with a specific color tint. For use in tile selection (spell scrolls).

    Parameters
    ----------
    display_surface : pygame Surface
        The surface the color tint will be displayed on.
    tile_coords : tuple
        The (x, y) map grid coordinates of the tile to be colored.
    color : tuple
        The color to cover the tile with.
    alpha : int, optional
        An int from 0 to 255 both inclusive, specifying the amount of opacity for the tint.
    mark : bool, optional
        True if a target mark also needs to be drawn onto the tile.

    Returns
    -------
    None

    """
    x, y = tile_coords

    # convert map grid coords to pixel coords
    map_x = x * constants.CELL_WIDTH
    map_y = y * constants.CELL_HEIGHT

    # Create a Surface that's the size of one tile grid
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(color)

    new_surface.set_alpha(alpha)
    if mark:
        display_surface.blit(new_surface, (map_x, map_y))
        display_surface.blit(globalvars.ASSETS.S_TARGET_MARK, (map_x, map_y))
    else:
        display_surface.blit(new_surface, (map_x, map_y))


def fade_to_solid(width, height, redraw_func, redraw_args, color=pygame.Color('black')):
    """Fades current display to a solid `color`.

    Parameters
    ----------
    width : int
        Width of the surface area to be faded.
    height : int
        Height of the surface area to be faded.
    redraw_func : function
        The draw function that is executed while the display doesnt fade straight to the color after one iteration.
    redraw_args : tuple
        All necessary arguments to be passed into the `redraw_func` function
    color : tuple, optional
        The solid color to fade towards. Default is black.

    Returns
    -------
    None

    """
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill(color)

    for alpha in range(0, 257, 2):
        fade_surface.set_alpha(alpha)
        redraw_func(redraw_args)

        globalvars.SURFACE_MAIN.blit(fade_surface, (0, 0))
        pygame.display.update()
