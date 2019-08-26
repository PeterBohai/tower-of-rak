import pygame

from src import constants, globalvars, text, draw


def menu_inventory():

    menu_close = False

    # game window dimensions
    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    # menu characteristics
    menu_width = (2/5) * window_width
    menu_height = (2/5) * window_height
    menu_x = (window_width/2) - (menu_width/2)          # number of pixels to the right from the left game window side
    menu_y = (window_height/2) - (menu_height/2)        # number of pixels down from the top game window side
    menu_text_font = constants.FONT_BEST
    menu_text_height = text.get_text_height(constants.FONT_BEST)
    menu_text_color = constants.COLOR_WHITE

    local_inventory_menu_surface = pygame.Surface((menu_width, menu_height))
    while not menu_close:

        draw.draw_game()

        # Clear the menu
        local_inventory_menu_surface.fill(constants.COLOR_GREY)

        # mouse control inside menu
        mouse_x, mouse_y = pygame.mouse.get_pos()  # gets mouse position coordinates relative to game window
        mouse_rel_x = mouse_x - menu_x      # mouse position relative to the menu
        mouse_rel_y = mouse_y - menu_y
        mouse_in_menu = (0 < mouse_rel_x < menu_width and
                         0 < mouse_rel_y < menu_height)

        mouse_line_selection = int(mouse_rel_y/menu_text_height)   # starting from 0, each line of text is an int number

        # Register changes (draw text on the local_inventory_menu_surface)
        print_list = [obj.display_name for obj in globalvars.PLAYER.container.inventory]    # list comprehension

        for line, name in enumerate(print_list):
            if mouse_in_menu and line == mouse_line_selection:
                text.draw_text(local_inventory_menu_surface, name, menu_text_font, (0, 0 + (line * menu_text_height)),
                               constants.COLOR_BLACK, constants.COLOR_WHITE)
            else:
                text.draw_text(local_inventory_menu_surface, name, menu_text_font, (0, 0 + (line * menu_text_height)),
                               menu_text_color)

        # draw menu
        globalvars.SURFACE_MAIN.blit(local_inventory_menu_surface,
                          (menu_x, menu_y))

        # get list of events input
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:    # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    if mouse_in_menu and mouse_line_selection + 1 <= len(print_list):

                        # exit out of inventory menu if using an item
                        # stay inside inventory menu if putting on equipment
                        if not globalvars.PLAYER.container.inventory[mouse_line_selection].equipment:
                            menu_close = True

                        # use or equip the item
                        globalvars.PLAYER.container.inventory[mouse_line_selection].item.use()

        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()   # pygame.display.update() does the same thing if given without any arguments
