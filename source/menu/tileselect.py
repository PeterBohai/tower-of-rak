
# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, draw, map


def menu_tile_select(coords_origin=None,
                     max_range=None,
                     radius=None,
                     wall_penetration=True,
                     creature_penetration=True):
    """Enables the player to select a tile on the map.

    This function will produce a rectangular indication when the mouse is hovered over a tile. When the player
    left-clicks the selected tile, the map address will be returned for use in other functions like spells.

    Returns:
         Map address of the selected tile when the player left-clicks the mouse button.

    """

    menu_close = False

    while not menu_close:

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # convert mouse window address to map pixel address
        map_x_pixel, map_y_pixel = globalvars.CAMERA.window_to_map((mouse_x, mouse_y))

        # convert to map tile address
        map_tile_x = int(map_x_pixel/constants.CELL_WIDTH)
        map_tile_y = int(map_y_pixel/constants.CELL_HEIGHT)

        if coords_origin:
            list_of_tiles = map.map_find_line(coords_origin, (map_tile_x, map_tile_y))

            # deal with "valid" tiles
            for i, (tile_x, tile_y) in enumerate(list_of_tiles):

                # stop at max_range
                if max_range and i == max_range:
                    # only take the map address tuples before the range
                    list_of_tiles = list_of_tiles[:i+1]

                # stop at wall
                if not wall_penetration:
                    # boolean checking if the tile is a wall or not (True if it is, False if not)
                    tile_is_wall = globalvars.GAME.current_map[tile_x][tile_y].block_path is True
                    if tile_is_wall:
                        list_of_tiles = list_of_tiles[:i]

                # stop at first creature encountered
                # same as slicing used above but slightly faster truncation method with deletion
                if not creature_penetration:
                    target_creature = map.map_check_for_creatures(tile_x, tile_y)
                    if target_creature and target_creature is not globalvars.PLAYER:
                        del list_of_tiles[i+1:]

        else:
            list_of_tiles = [(map_tile_x, map_tile_y)]

        # Get events
        event_list = pygame.event.get()
        for event in event_list:
            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

            # mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:    # left-click is 1, right is 3, scroll up is 4 and down is 5

                # return the last map tile address within the valid list of tiles
                if event.button == 1:

                    if (map_tile_x, map_tile_y) == list_of_tiles[-1]:
                        return map_tile_x, map_tile_y

                    # or maybe tell player that they must click on a tile that is within the range, etc.
                    else:
                        return list_of_tiles[-1]

        # Draw game
        # clear the surface (filling it with some color, wipe the color out)
        globalvars.SURFACE_MAIN.fill(constants.COLOR_BLACK)
        globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)

        globalvars.CAMERA.update_pos()

        # draw the map
        draw.draw_map(globalvars.GAME.current_map)

        # draw the character
        for obj in globalvars.GAME.current_objects:
            obj.draw()

        # draw area of affect with the correct radius
        if radius:
            area_of_effect = map.map_find_radius(list_of_tiles[-1], radius)
            target_tile = list_of_tiles[-1]

            # prevent tiles to be highlighted twice (as it changes the opaqueness of the highlight)
            for (tile_x, tile_y) in area_of_effect:
                target_creature = map.map_check_for_creatures(tile_x, tile_y)

                for x, y in list_of_tiles:
                    if (tile_x, tile_y) == (x, y):
                        list_of_tiles.remove((x, y))

                # highlight tile in red if tile contains a monster
                if target_creature:
                    # mark target with an "X"
                    if (tile_x, tile_y) == target_tile:
                        draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED, alpha=200, mark="X")

                    else:
                        draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED, alpha=150)

                # highlight anything else (walls, floor, items) in pale yellow
                else:
                    # mark target with an "X"
                    if (tile_x, tile_y) == target_tile:
                        draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=200, mark="X")
                    else:
                        draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=100)

        # Draw rectangle at mouse position over game visuals
        for (tile_x, tile_y) in list_of_tiles:

            # mark target with an "X"
            if (tile_x, tile_y) == list_of_tiles[-1] and not radius:
                draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=200, mark="X")

            target_creature = map.map_check_for_creatures(tile_x, tile_y)

            # highlight tile in red if tile contains a monster
            if target_creature and target_creature is not globalvars.PLAYER:
                draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED)

            # no highlight of tile if tile is PLAYER (setting transparency to max)
            elif target_creature is globalvars.PLAYER:
                draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=0)

            # highlight anything else (walls, floor, items) in white
            else:
                draw.draw_tile_rect(globalvars.SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=150)

        # next half of draw_game()
        globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)

        draw.draw_debug()
        draw.draw_messages()

        pygame.display.flip()  # pygame.display.update() does the same thing if given without any arguments

        # tick the CLOCK
        globalvars.CLOCK.tick(constants.GAME_FPS)
