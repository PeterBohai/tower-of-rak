import pygame

from src import constants, globalvars, text, draw, game, gui


def menu_inventory():
    """Displays the inventory menu when PLAYER accesses the inventory.

    Menu allows PLAYER to look at stored items and use or equip them.

    Returns
    -------
    None

    """
    menu_width = 809
    menu_height = 384

    first_frame_x, first_frame_y = 264, 71

    frame_x_spacing = 56
    frame_y_spacing = 52

    # (x, y) coordinates for the topleft corner of the menu
    menu_x = (constants.CAMERA_WIDTH/2) - (menu_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (menu_height/2)

    inventory_surface = pygame.Surface((menu_width, menu_height))

    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    item_selected = None
    menu_close = False
    while not menu_close:

        draw.draw_game()

        # mouse control inside menu
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rel_x = mouse_x - menu_x
        mouse_rel_y = mouse_y - menu_y

        mouse_clicked = False
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                game.game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    mouse_clicked = True

        inventory_surface.blit(globalvars.ASSETS.S_INVENTORY, (0, 0))

        # display items icons onto inventory surface
        for num, item in enumerate(globalvars.PLAYER.container.inventory):
            row = num // 5
            col = num % 5
            item_x = first_frame_x + col * frame_x_spacing
            item_y = first_frame_y + row * frame_y_spacing

            mouse_hover = (item_x < mouse_rel_x < item_x + 32 and item_y < mouse_rel_y < item_y + 32)

            if mouse_hover:
                item_selected = num
            else:
                item_selected = None

            gui.hovered_clickable_element(mouse_hover, mouse_clicked)
            inventory_surface.blit(globalvars.ASSETS.animation_dict[item.animation_key][0], (item_x, item_y))

        globalvars.SURFACE_MAIN.blit(inventory_surface, (menu_x, menu_y))
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

        if mouse_clicked and item_selected is not None:
            # stay inside inventory menu if putting on equipment
            if not globalvars.PLAYER.container.inventory[item_selected].equipment:
                menu_close = True

            # use or equip the item
            globalvars.PLAYER.container.inventory[item_selected].item.use()



