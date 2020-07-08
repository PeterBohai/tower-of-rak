
import pygame
import numpy

from src import constants, globalvars, text, gui, draw
from src.menu import mainmenu


def menu_credits():
    """Displays the credits menu.

    Returns
    -------
    None
    """
    menu_width = 608
    menu_height = 224

    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu init =============== #
    credits_surface = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # text positions
    title_x = center_x
    title_y = menu_rect.top + 20

    text_height = text.get_text_height(constants.FONT_CREDITS)
    text_x = menu_rect.left + 20
    text_y_first = title_y + 30
    text_y_offset = text_height + 2

    num_lines = (menu_height - (text_y_first - menu_rect.top)) // (text_height + 2)
    line_y = [text_y_first + line * text_y_offset for line in range(num_lines)]

    text_lines = ("GRAPHICS:", "DAWNLIKE 16x16 Universal Rogue-like tileset v1.81 by DawnBringer",
                  "SOUND:", "Music by Eric Matyas - www.soundimage.org")

    # ================= button variables ================ #
    # buttons
    button_width = 96
    button_height = 32

    menu_button_x = center_x
    menu_button_y = menu_rect.bottom - 30
    menu_button_text = "Main Menu"

    # ====================== button section ===================== #
    menu_button = gui.GuiButton(credits_surface, menu_button_text,
                                (menu_button_x, menu_button_y),
                                (button_width, button_height))

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)
    menu_tiles = (
        globalvars.ASSETS.S_TOP_L_MENU_LIGHT, globalvars.ASSETS.S_TOP_R_MENU_LIGHT,
        globalvars.ASSETS.S_BOT_L_MENU_LIGHT, globalvars.ASSETS.S_BOT_R_MENU_LIGHT,
        globalvars.ASSETS.S_TOP_MENU_LIGHT, globalvars.ASSETS.S_BOT_MENU_LIGHT,
        globalvars.ASSETS.S_SIDE_L_MENU_LIGHT, globalvars.ASSETS.S_SIDE_R_MENU_LIGHT,
        globalvars.ASSETS.S_MID_MENU_LIGHT
    )

    # ====================== MENU LOOP ===================== #
    menu_close = False
    while not menu_close:

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        player_events = (events_list, mouse_pos)

        # process player input
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        if menu_button.update(player_events):
            menu_close = True

        if menu_button.mouse_hover:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        # draw functions

        text.draw_text(credits_surface, "Credits", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)

        # display lines of text
        line_num = -2

        for line in text_lines:
            line_num += 1 if not line.isupper() else 2
            text_font = constants.FONT_CREDIT_LABELS if line.isupper() else constants.FONT_CREDITS
            text.draw_text(credits_surface, line, text_font, (text_x, line_y[line_num]),
                           constants.COLOR_BLACK if line.isupper() else constants.COLOR_BLUE3)
        menu_button.draw()

        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(credits_surface, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(credits_surface, (menu_width, menu_height), *corner_positions,
                                  assets=menu_tiles)
        pygame.display.update()
