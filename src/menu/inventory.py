import pygame

from src import constants, globalvars, text, draw


def menu_inventory():
    """Displays the inventory menu when PLAYER accesses the inventory.

    Menu allows PLAYER to look at stored items and use or equip them.

    Returns
    -------
    None

    """
    menu_width = (2/5) * constants.CAMERA_WIDTH
    menu_height = (2/5) * constants.CAMERA_HEIGHT

    # (x, y) coordinates for the topleft corner of the menu
    menu_x = (constants.CAMERA_WIDTH/2) - (menu_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (menu_height/2)

    text_font = constants.FONT_BEST
    text_height = text.get_text_height(constants.FONT_BEST)
    text_color = constants.COLOR_WHITE

    inventory_surface = pygame.Surface((menu_width, menu_height))

    menu_close = False
    while not menu_close:

        draw.draw_game()
        inventory_surface.fill(constants.COLOR_GREY)

        # mouse control inside menu
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rel_x = mouse_x - menu_x
        mouse_rel_y = mouse_y - menu_y
        mouse_in_menu = (0 < mouse_rel_x < menu_width and 0 < mouse_rel_y < menu_height)

        # starting from 0, each line of text is an int
        mouse_line_selection = int(mouse_rel_y/text_height)
        item_names_list = [obj.display_name for obj in globalvars.PLAYER.container.inventory]

        for line_num, name in enumerate(item_names_list):
            if mouse_in_menu and line_num == mouse_line_selection:
                text.draw_text(inventory_surface, name, text_font, (0, 0 + (line_num * text_height)),
                               constants.COLOR_BLACK, back_color=constants.COLOR_WHITE)
            else:
                text.draw_text(inventory_surface, name, text_font, (0, 0 + (line_num * text_height)), text_color)

        globalvars.SURFACE_MAIN.blit(inventory_surface, (menu_x, menu_y))
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    if mouse_in_menu and mouse_line_selection + 1 <= len(item_names_list):
                        # stay inside inventory menu if putting on equipment
                        if not globalvars.PLAYER.container.inventory[mouse_line_selection].equipment:
                            menu_close = True

                        # use or equip the item
                        globalvars.PLAYER.container.inventory[mouse_line_selection].item.use()
