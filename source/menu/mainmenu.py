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
    title_y = constants.CAMERA_HEIGHT / 4

    # ======================= button variables ====================== #
    # button sizes
    button_width = 150
    button_height = 30
    button_offset_y = 5/4 * button_height

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
    print(new_game_button_y - title_y)

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

        # ================ button interaction ================ #
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

        if credits_button.update(player_events):
            menu_credits()

        # ================== draw elements ================== #
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
        credits_button.draw()

        pygame.display.update()


def menu_credits():

    # ============== options menu dimensions ============== #
    # options menu dimensions
    menu_width = 600
    menu_height = 221

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

    text_x = menu_rect.left + 5
    line1_y = title_y + 30
    line2_y = line1_y + text.helper_text_height(constants.FONT_CREDITS)

    # ================= slider/button variables ================ #
    # buttons
    button_width = 80
    button_height = 30

    menu_button_x = center_x
    menu_button_y = menu_rect.bottom - 30
    menu_button_text = "Main Menu"

    # ====================== button section ===================== #

    menu_button = gui.GuiButton(surface_credits_menu, menu_button_text,
                                (menu_button_x, menu_button_y),
                                (button_width, button_height),
                                color_button_hovered=constants.COLOR_BLACK,
                                color_button_default=constants.COLOR_GREY,
                                color_text_hovered=constants.COLOR_WHITE,
                                color_text_default=constants.COLOR_WHITE)

    # menu loop
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

        # draw functions
        text.draw_text(surface_credits_menu, "Credits", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_WHITE,
                       center=True)

        text.draw_text(surface_credits_menu, "DAWNLIKE 16x16 Universal Rogue-like tileset v1.81 by DawnBringer",
                       constants.FONT_CREDITS,
                       (text_x, line1_y ),
                       constants.COLOR_WHITE)
        text.draw_text(surface_credits_menu, "Music by Eric Matyas - www.soundimage.org",
                       constants.FONT_CREDITS,
                       (text_x, line2_y),
                       constants.COLOR_WHITE)


        menu_button.draw()

        # update display
        globalvars.SURFACE_MAIN.blit(surface_credits_menu, menu_rect.topleft, menu_rect)
        surface_credits_menu.fill(constants.COLOR_BROWN)
        pygame.display.update()
