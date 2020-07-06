import sys

import pygame

from src import constants, globalvars, text, startup, gui, game, draw
from src.menu import options, credits


def menu_main():
    """Initialize the game and draws the main menu

    Returns
    -------
    None
    """

    startup.game_initialize()
    center_x = constants.CAMERA_WIDTH / 2
    title_y = constants.CAMERA_HEIGHT / 4

    # ----- button specs ----- #

    # button sizes (px)
    button_width = 160
    button_height = 32
    button_offset_y = int(round(5/4 * button_height))

    new_game_button_y = title_y + 100
    cont_button_y = new_game_button_y + button_offset_y
    options_button_y = cont_button_y + button_offset_y
    credits_button_y = options_button_y + button_offset_y
    quit_button_y = credits_button_y + button_offset_y

    # ------ create buttons ----- #
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

    # ==================== MENU LOOP ==================== #
    display_changed = False
    menu_running = True

    while menu_running:
        # ---- retrieve user input and events ----- #
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        player_events = (events_list, mouse_pos)

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                perform_exit_sequence()

        # ----- button event listeners ----- #
        # start new game
        if new_game_button.update(player_events):
            pygame.mixer.music.fadeout(1500)
            draw.fade_to_solid(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT, draw_main_menu, menu_buttons_tup)
            game.game_start()
            menu_main()

        # load previous game
        elif cont_button.update(player_events):
            pygame.mixer.music.fadeout(1500)
            draw.fade_to_solid(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT,
                               draw_main_menu, menu_buttons_tup, color=pygame.Color('white'))
            game.game_start(new=False)
            menu_main()

        elif options_button.update(player_events):
            previous_display = globalvars.PREFERENCES.display_window
            options.main_options_menu()
            if previous_display != globalvars.PREFERENCES.display_window:
                display_changed = True
                break

        elif credits_button.update(player_events):
            credits.menu_credits()

        if quit_button.update(player_events):
            perform_exit_sequence()

        # ------- display functions ------- #
        draw_main_menu(menu_buttons_tup)
        pygame.display.update()

    if display_changed and globalvars.PREFERENCES.display_window == "fullscreen":
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT),
                                                          flags=pygame.FULLSCREEN)
        menu_main()

    elif display_changed:
        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        menu_main()


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
    text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak", constants.FONT_GAME_TITLE, buttons[-1],
                   constants.COLOR_RED, center=True)
    draw.draw_button_update_cursor(buttons[:-1])


def perform_exit_sequence():
    """Executes program termination procedures.

    Returns
    -------
    None
    """
    pygame.mixer.fadeout(10)
    pygame.quit()
    sys.exit()
