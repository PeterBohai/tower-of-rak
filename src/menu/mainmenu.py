import sys

import pygame
import numpy

from src import constants, globalvars, text, startup, gui, game, draw
from src.menu import options


def menu_main():
    """Initialize the game and draws the main menu

    Returns
    -------
    None

    """

    startup.game_initialize()

    # tile address
    center_x = constants.CAMERA_WIDTH / 2
    title_y = constants.CAMERA_HEIGHT / 4

    # ======================= button variables ====================== #

    # button sizes (px)
    button_width = 160
    button_height = 32
    button_offset_y = int(round(5/4 * button_height))

    # button address
    new_game_button_y = title_y + 100
    cont_button_y = new_game_button_y + button_offset_y
    options_button_y = cont_button_y + button_offset_y
    credits_button_y = options_button_y + button_offset_y
    quit_button_y = credits_button_y + button_offset_y

    # ====================== button initialization ===================== #
    new_game_button = gui.GuiButton(globalvars.SURFACE_MAIN, "New Game",
                                    (center_x, new_game_button_y),
                                    (button_width, button_height))

    cont_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Continue",
                                (center_x, cont_button_y),
                                (button_width, button_height))

    options_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Options",
                                   (center_x, options_button_y),
                                   (button_width, button_height))

    credits_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Credits",
                                   (center_x, credits_button_y),
                                   (button_width, button_height))

    quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "QUIT",
                                (center_x, quit_button_y),
                                (button_width, button_height))

    # all main menu buttons in vertical order (top to bottom) along with relevant coords as last element
    menu_buttons_tup = (new_game_button, cont_button, options_button, credits_button, quit_button, (center_x, title_y))

    # play background music (on loop)
    pygame.mixer.music.load(globalvars.ASSETS.main_menu_music)
    pygame.mixer.music.play(-1)

    # set flags
    display_changed = False
    menu_running = True

    # ====================== main menu loop ===================== #
    while menu_running:

        # process inputs
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        player_events = (events_list, mouse_pos)
        for event in events_list:
            if event.type == pygame.QUIT:
                pygame.mixer.fadeout(10)
                pygame.quit()
                sys.exit()

        # ================ button interaction ================ #
        # start new game if clicked
        if new_game_button.update(player_events):
            pygame.mixer.music.fadeout(1500)
            draw.fade_to_solid(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT, draw_main_menu, menu_buttons_tup)
            game.game_start()
            menu_main()

        # load previous game if clicked
        if cont_button.update(player_events):
            pygame.mixer.music.fadeout(1500)
            draw.fade_to_solid(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT,
                               draw_main_menu, menu_buttons_tup, color=pygame.Color('white'))
            game.game_start(new=False)
            menu_main()

        # display options menu
        if options_button.update(player_events):
            previous_display = globalvars.PREFERENCES.display_window
            options.main_options_menu()
            if previous_display != globalvars.PREFERENCES.display_window:
                display_changed = True
                break
            else:
                display_changed = False

        if credits_button.update(player_events):
            menu_credits()

        # quit the game
        if quit_button.update(player_events):
            pygame.mixer.fadeout(10)
            pygame.quit()
            sys.exit()

        # Change cursor when hovering over a button
        for i, button in enumerate(menu_buttons_tup[:-1]):
            if button.mouse_hover:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
            if i == len(menu_buttons_tup) - 2:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        # ================== draw elements ================== #
        # draw menu background and title
        draw_main_menu(menu_buttons_tup)

        pygame.display.update()

    if display_changed and globalvars.PREFERENCES.display_window == "fullscreen":
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT),
                                                          flags=pygame.FULLSCREEN)
        menu_main()

    elif display_changed:
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        menu_main()


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

    title_x = center_x
    title_y = menu_rect.top + 20

    text_x = menu_rect.left + 20
    text_height = text.get_text_height(constants.FONT_CREDITS)

    line_y = [title_y + 30]

    num_lines = int((menu_height - (line_y[0] - menu_rect.top)) / (text_height + 2))
    for i in range(1, num_lines + 1):
        line_y.append(line_y[i-1] + text_height + 2)

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

    # background tile positions
    topL = menu_rect.topleft
    topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))

    # ====================== MENU LOOP ===================== #
    menu_close = False
    while not menu_close:

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        player_events = (events_list, mouse_pos)

        # process player input
        for event in events_list:
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

        text.draw_text(credits_surface, "GRAPHICS:",
                       constants.FONT_CREDIT_LABELS,
                       (text_x, line_y[0]),
                       constants.COLOR_BLACK)

        text.draw_text(credits_surface, "DAWNLIKE 16x16 Universal Rogue-like tileset v1.81 by DawnBringer",
                       constants.FONT_CREDITS,
                       (text_x, line_y[1]),
                       constants.COLOR_BLUE3)

        text.draw_text(credits_surface, "SOUND:",
                       constants.FONT_CREDIT_LABELS,
                       (text_x, line_y[3]),
                       constants.COLOR_BLACK)

        text.draw_text(credits_surface, "Music by Eric Matyas - www.soundimage.org",
                       constants.FONT_CREDITS,
                       (text_x, line_y[4]),
                       constants.COLOR_BLUE3)

        menu_button.draw()

        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(credits_surface, menu_rect.topleft, menu_rect)

        # blit the corners
        credits_surface.blit(globalvars.ASSETS.S_TOP_L_MENU_LIGHT, topL)
        credits_surface.blit(globalvars.ASSETS.S_TOP_R_MENU_LIGHT, topR)
        credits_surface.blit(globalvars.ASSETS.S_BOT_L_MENU_LIGHT, botL)
        credits_surface.blit(globalvars.ASSETS.S_BOT_R_MENU_LIGHT, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width / 32) - 2
        num_tiles_height = int(menu_height / 32) - 2

        for w in range(1, num_tiles_width + 1):
            credits_surface.blit(globalvars.ASSETS.S_TOP_MENU_LIGHT, tuple(numpy.add(topL, (32*w, 0))))
            credits_surface.blit(globalvars.ASSETS.S_BOT_MENU_LIGHT, tuple(numpy.add(botL, (32*w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            credits_surface.blit(globalvars.ASSETS.S_SIDE_L_MENU_LIGHT, tuple(numpy.add(topL, (0, 32 * h))))
            credits_surface.blit(globalvars.ASSETS.S_SIDE_R_MENU_LIGHT, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                credits_surface.blit(globalvars.ASSETS.S_MID_MENU_LIGHT, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


def draw_main_menu(buttons):
    """Draws the main menu (background and buttons).

    Parameters
    ----------
    buttons : tuple
        A tuple containing all GuiButton objects to be drawn and the coordinates for the title.

    Returns
    -------
    None

    """
    globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.S_MAIN_MENU, (0, 0))

    text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak",
                   constants.FONT_GAME_TITLE,
                   buttons[-1],
                   constants.COLOR_RED,
                   center=True)
    for btn in buttons:
        if type(btn) is gui.GuiButton:
            btn.draw()

