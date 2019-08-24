import sys

import pygame
import numpy

from source import constants, globalvars, text, startup, gui, game, draw
from source.menu import options


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
            options.menu_main_options()
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

    # ============== options menu dimensions ============== #
    # options menu dimensions
    menu_width = 608
    menu_height = 224

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_credits_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # title
    title_x = center_x
    title_y = menu_rect.top + 20

    text_x = menu_rect.left + 20
    line1_y = title_y + 30
    line2_y = line1_y + text.helper_text_height(constants.FONT_CREDITS) + 2
    line3_y = line2_y + text.helper_text_height(constants.FONT_CREDITS) + 15
    line4_y = line3_y + text.helper_text_height(constants.FONT_CREDITS) + 2


    # ================= slider/button variables ================ #
    # buttons
    button_width = 96
    button_height = 32

    menu_button_x = center_x
    menu_button_y = menu_rect.bottom - 30
    menu_button_text = "Main Menu"

    # ====================== button section ===================== #

    menu_button = gui.GuiButton(surface_credits_menu, menu_button_text,
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
        text.draw_text(surface_credits_menu, "Credits", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)

        text.draw_text(surface_credits_menu, "GRAPHICS:",
                       constants.FONT_CREDIT_LABELS,
                       (text_x, line1_y),
                       constants.COLOR_BLACK)

        text.draw_text(surface_credits_menu, "DAWNLIKE 16x16 Universal Rogue-like tileset v1.81 by DawnBringer",
                       constants.FONT_CREDITS,
                       (text_x, line2_y),
                       constants.COLOR_BLUE3)

        text.draw_text(surface_credits_menu, "SOUND:",
                       constants.FONT_CREDIT_LABELS,
                       (text_x, line3_y),
                       constants.COLOR_BLACK)

        text.draw_text(surface_credits_menu, "Music by Eric Matyas - www.soundimage.org",
                       constants.FONT_CREDITS,
                       (text_x, line4_y),
                       constants.COLOR_BLUE3)

        menu_button.draw()

        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(surface_credits_menu, menu_rect.topleft, menu_rect)

        # blit the corners
        surface_credits_menu.blit(globalvars.ASSETS.S_TOP_L_MENU_LIGHT, topL)
        surface_credits_menu.blit(globalvars.ASSETS.S_TOP_R_MENU_LIGHT, topR)
        surface_credits_menu.blit(globalvars.ASSETS.S_BOT_L_MENU_LIGHT, botL)
        surface_credits_menu.blit(globalvars.ASSETS.S_BOT_R_MENU_LIGHT, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width / 32) - 2  # number of tiles width-wise ignoring the 2 corners
        num_tiles_height = int(menu_height / 32) - 2  # number of tiles height-wise ignoring the 2 corners

        for w in range(1, num_tiles_width + 1):
            surface_credits_menu.blit(globalvars.ASSETS.S_TOP_MENU_LIGHT, tuple(numpy.add(topL, (32*w, 0))))
            surface_credits_menu.blit(globalvars.ASSETS.S_BOT_MENU_LIGHT, tuple(numpy.add(botL, (32*w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            surface_credits_menu.blit(globalvars.ASSETS.S_SIDE_L_MENU_LIGHT, tuple(numpy.add(topL, (0, 32 * h))))
            surface_credits_menu.blit(globalvars.ASSETS.S_SIDE_R_MENU_LIGHT, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                surface_credits_menu.blit(globalvars.ASSETS.S_MID_MENU_LIGHT, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


def draw_main_menu(button_tup):

    # draw menu background and title (last element of button_tup hold title position)
    globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.S_MAIN_MENU, (0, 0))
    text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak",
                   constants.FONT_GAME_TITLE,
                   button_tup[-1],
                   constants.COLOR_RED,
                   center=True)

    # draw buttons
    button_tup[0].draw()
    button_tup[1].draw()
    button_tup[2].draw()
    button_tup[3].draw()
    button_tup[4].draw()
