import pygame

from src import constants, globalvars, draw, map


def menu_tile_select(coords_origin=None,
                     max_range=None,
                     radius=None,
                     wall_pen=True,
                     creature_pen=True,
                     base_color=constants.COLOR_WHITE,
                     target_color=constants.COLOR_RED,
                     single_tile=False):
    """Enables the player to select a tile on the map.

    This function produces a rectangular indication when the mouse is hovered over a tile as well as other tiles
    that could be affected, depending on the spell being used, etc.

    Parameters
    ----------
    coords_origin : tuple, optional
        The map-grid coordinate of the caster/spell user.
    max_range : int, optional
        Maximum number of tiles out from the caster.
    radius : int, optional
        Number of tiles out from the player when using an area of affect spell in the shape of a ball/square.
    wall_pen : bool, optional
        True if spell can ignore wall tiles.
    creature_pen : bool, optional
        True if spell can range past the first creature encounter.
    base_color : tuple, optional
        Color of tile tint with no affected objects.
    target_color : tuple, optional
        Color of tile tint when there is an affected object (creature).
    single_tile : bool, optional
        True if spell requires only a single tile target and not a line or aoe.

    Returns
    -------
    tuple
        The map-grid coordinate of the tile that the PLAYER clicked on.

    """
    menu_close = False
    while not menu_close:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # convert mouse window address to map grid address
        map_tile_x, map_tile_y = globalvars.CAMERA.window_to_map((mouse_x, mouse_y))

        if coords_origin is not None:
            list_of_tiles = map.tiles_in_line(coords_origin, (map_tile_x, map_tile_y))

            # deal with "valid" tiles
            for i, (tile_x, tile_y) in enumerate(list_of_tiles):

                # stop at max_range
                if max_range is not None and i == max_range:
                    # only take the map address tuples before the range
                    list_of_tiles = list_of_tiles[:i+1]

                # stop at wall
                if not wall_pen:
                    # boolean checking if the tile is a wall or not (True if it is, False if not)
                    tile_is_wall = globalvars.GAME.current_map[tile_x][tile_y].block_path is True
                    if tile_is_wall:
                        list_of_tiles = list_of_tiles[:i]

                # stop at first creature encountered
                if not creature_pen:
                    target_creature = map.creature_at_coords(tile_x, tile_y)
                    if target_creature and target_creature is not globalvars.PLAYER:
                        del list_of_tiles[i+1:]

        else:
            list_of_tiles = [(map_tile_x, map_tile_y)]

        event_list = pygame.event.get()
        for event in event_list:
            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

            # mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (map_tile_x, map_tile_y) == list_of_tiles[-1]:
                        return map_tile_x, map_tile_y
                    else:
                        return list_of_tiles[-1]

        # Draw game
        globalvars.SURFACE_MAIN.fill(constants.COLOR_GAME_BG)
        globalvars.SURFACE_MAP.fill(constants.COLOR_GAME_BG)

        globalvars.CAMERA.update_pos()

        # draw the map
        draw.draw_map(globalvars.GAME.current_map)

        # draw the character
        for obj in globalvars.GAME.current_objects:
            obj.draw()

        # Draw line of selection
        for (tile_x, tile_y) in list_of_tiles:
            if (tile_x, tile_y) == list_of_tiles[-1]:
                draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), base_color)

            target_creature = map.creature_at_coords(tile_x, tile_y)

            if target_creature is not None:
                if target_creature is not globalvars.PLAYER:
                    draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), target_color, alpha=100, mark=True)

                elif target_creature is globalvars.PLAYER and single_tile:
                    draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, mark=True)
            else:
                draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), base_color)

        if radius:
            area_of_effect = map.tiles_in_radius(list_of_tiles[-1], radius)
            target_tile = list_of_tiles[-1]

            # prevent tiles to be highlighted twice (as it changes the opaqueness of the highlight)
            for (tile_x, tile_y) in area_of_effect:
                target_creature = map.creature_at_coords(tile_x, tile_y)

                for x, y in list_of_tiles:
                    if (tile_x, tile_y) == (x, y):
                        list_of_tiles.remove((x, y))

                # highlight tile in red if tile contains a monster
                if target_creature is not None:
                    if (tile_x, tile_y) == target_tile:
                        draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), target_color, mark=True)

                    else:
                        draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), target_color, mark=True)
                else:
                    # mark target with an "X"
                    if (tile_x, tile_y) == target_tile:
                        draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=200, mark=True)
                    else:
                        draw.draw_one_tile(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=125)

        globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)
        draw.draw_window_ui()
        pygame.display.flip()
        globalvars.CLOCK.tick(constants.GAME_FPS)
