# Standrad library imports
import sys

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, text, startup, gui, game
from source.menu import options


def menu_main():
    startup.game_initialize()
    menu_running = True

    # tile address
    center_x = constants.CAMERA_WIDTH / 2
    title_y = constants.CAMERA_HEIGHT / 2 - (constants.CAMERA_HEIGHT/4)

    # button sizes
    button_width = 150
    button_height = 30
    button_offset_y = 5/4 * button_height

    # button address
    new_game_button_y = title_y + constants.CAMERA_HEIGHT/5
    cont_button_y = new_game_button_y + button_offset_y
    options_button_y = cont_button_y + button_offset_y
    quit_button_y = options_button_y + button_offset_y

    # buttons
    new_game_button = gui.GuiButton(globalvars.SURFACE_MAIN, "NEW GAME",
                            (center_x, new_game_button_y),
                            (button_width, button_height))

    cont_button = gui.GuiButton(globalvars.SURFACE_MAIN, "CONTINUE",
                           (center_x, cont_button_y),
                           (button_width, button_height))

    options_button = gui.GuiButton(globalvars.SURFACE_MAIN, "OPTIONS",
                              (center_x, options_button_y),
                              (button_width, button_height))

    quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "QUIT",
                           (center_x, quit_button_y),
                           (button_width, button_height))

    # play background music
    pygame.mixer.music.load(globalvars.ASSETS.main_menu_music)
    pygame.mixer.music.play(-1)

    while menu_running:

        # process inputs
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        player_events = (events_list, mouse_pos)

        for event in events_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # start new game if clicked
        if new_game_button.update(player_events):
            pygame.mixer.music.fadeout(3000)
            game.game_new()
            game.game_main_loop()
            menu_main()

        # load previous game if clicked
        if cont_button.update(player_events):
            pygame.mixer.music.fadeout(3000)
            game.game_start()
            menu_main()

        # quit the game
        if quit_button.update(player_events):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        # display options menu
        if options_button.update(player_events):
            options.menu_main_options()

        # draw menu background and title
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.S_MAIN_MENU, (0, 0))
        text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak",
                       constants.FONT_GAME_TITLE,
                       (center_x, title_y),
                       constants.COLOR_RED,
                       center=True)

        # draw buttons
        new_game_button.draw()
        cont_button.draw()
        options_button.draw()
        quit_button.draw()

        pygame.display.update()