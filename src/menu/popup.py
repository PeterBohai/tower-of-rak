import textwrap

import pygame
import numpy

from src import constants, globalvars, text, draw, game, gui


def popup_menu(msg):
    """A simple popup menu that displays a message.

    Returns
    -------
    None
    """

    menu_text = msg
    font = constants.FONT_BEST_20

    text_height = text.get_text_height(font)
    text_width = text.get_text_width(font, menu_text)

    menu_x = (constants.CAMERA_WIDTH/2) - (text_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (text_height/2)

    start_time = pygame.time.get_ticks()

    menu_close = False
    while not menu_close:
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= 1300:
            break

        event_list = pygame.event.get()

        text.draw_text(globalvars.SURFACE_MAIN, menu_text, font,
                       (menu_x, menu_y), constants.COLOR_WHITE, constants.COLOR_GAME_BG)

        for event in event_list:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()


def game_story_popup():
    """A popup menu containing text about the game's story as well as basic controls information.

    To be displayed at the start of a new game.

    Returns
    -------
    None
    """
    menu_width, menu_height = 600, 400
    menu_x = (constants.CAMERA_WIDTH/2) - (menu_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (menu_height/2)
    pop_surface = pygame.Surface((menu_width, menu_height))

    title_font = constants.FONT_BEST_20
    title_text = "Greetings!"
    title_coords = (menu_width // 2, 30)

    story_font = constants.FONT_BEST
    story_text = "Welcome to this world of two violently opposing races. " \
                 "You, Twenty-Fifth Raak, was raised by the Gaters, a race which have struggled " \
                 "helplessly against the dominating Teurtals for over half a millennium. " \
                 "Upon hearing about the mysterious Tower of Rak, " \
                 "you ventured out in hopes of obtaining the rumored ancient relic said to be " \
                 "hidden on the very top of the tower. With its legemdary hidden power, " \
                 "you seek to free the Gators from the shackles of the Teurtals once and for all."

    story_coords = (40, 50)
    text_height = text.get_text_height(story_font)

    begin_text = "Your adventure begins now, " \
                 "as you finally managed to find and enter the Tower of Rak. Good luck!"

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

        # exit menu if mouse clicks outside its boundaries
        if mouse_clicked and (mouse_rel_y < 0 or mouse_rel_x < 0
                              or mouse_rel_x > menu_width or mouse_rel_y > menu_height):
            menu_close = True

        pop_surface.blit(globalvars.ASSETS.S_GRAY_POPUP, (0, 0))

        # draw title and story text
        text.draw_text(pop_surface, title_text, title_font, title_coords, constants.COLOR_BLACK,
                       center=True)

        new_msg_lines = textwrap.wrap(story_text, 65)

        last_y = story_coords[1]
        for text_line in new_msg_lines:

            text.draw_text(pop_surface, text_line, story_font, (story_coords[0], last_y),
                           pygame.Color("#00223a"))
            last_y = last_y + text_height + 4

        begin_text_lines = textwrap.wrap(begin_text, 65)
        begin_y = last_y + text_height
        for txt in begin_text_lines:
            text.draw_text(pop_surface, txt, story_font, (story_coords[0], begin_y),
                           pygame.Color("#00223a"))
            begin_y = begin_y + text_height + 4

        globalvars.SURFACE_MAIN.blit(pop_surface, (menu_x, menu_y))
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()


def confirmation_popup():
    """Displays a confirmation popup menu.

    Returns
    -------
    None
    """
    menu_width = 448
    menu_height = 160

    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # ================= button variables ================ #
    # buttons
    button_width = 64
    button_height = 32

    menu_button_x = center_x
    menu_button_y = menu_rect.bottom - 30
    menu_button_text = "Exit"

    # message vars
    font = constants.FONT_BEST
    text_height = text.get_text_height(font)
    text_offset = text_height + 6
    text_x = menu_rect.centerx
    text_y = menu_rect.top + (menu_button_y - menu_rect.top) // 2 - text_offset // 2

    # ====================== button section ===================== #
    menu_button = gui.GuiButton(surface_menu, menu_button_text,
                                (menu_button_x, menu_button_y),
                                (button_width, button_height))

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

    # ====================== MENU LOOP ===================== #
    menu_close = False
    while not menu_close:
        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        mouse_rel_x = mouse_pos[0] - menu_rect.left
        mouse_rel_y = mouse_pos[1] - menu_rect.top

        player_events = (events_list, mouse_pos)
        mouse_clicked = False
        # process player input
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    mouse_clicked = True

        if mouse_clicked and (mouse_rel_y < 0 or mouse_rel_x < 0
                              or mouse_rel_x > menu_width or mouse_rel_y > menu_height):
            menu_close = True

        if menu_button.update(player_events):
            game.game_exit()
            menu_close = True

        if menu_button.mouse_hover:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        # draw functions
        text.draw_text(surface_menu, "Exit game?",
                       font,
                       (text_x, text_y),
                       constants.COLOR_BLACK, center=True)
        text.draw_text(surface_menu, "Remember to go to the options menu to save the game.",
                       font,
                       (text_x, text_y + text_offset),
                       constants.COLOR_BLACK, center=True)
        menu_button.draw()

        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(surface_menu, (menu_width, menu_height), *corner_positions)
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

