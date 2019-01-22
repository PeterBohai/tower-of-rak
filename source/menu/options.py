# Standrad library imports
import sys

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, text, gui, game


def menu_main_options(game_menu_options=False):

    # ============== options menu dimensions ============== #
    # options menu dimensions
    menu_width = 366
    menu_height = 221

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_option_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # title
    title_x = center_x
    title_y = menu_rect.top + 30

    # ================= slider/button variables ================ #
    slider_width = 170
    slider_height = 8
    slider_text_offset_y = 18

    music_slider_x = center_x
    music_slider_y = center_y - 20
    sfx_slider_x = music_slider_x
    sfx_slider_y = music_slider_y + 45

    # buttons
    button_width = 50
    button_height = 25

    save_button_x = center_x
    save_button_y = menu_rect.bottom - 30
    save_button_text = "SAVE"

    # ============== volume slider initialization ============== #

    music_slider = gui.GuiSlider(surface_option_menu,
                             (music_slider_x, music_slider_y),
                             (slider_width, slider_height),
                             globalvars.PREFERENCES.music_volume_val)

    sfx_slider = gui.GuiSlider(surface_option_menu,
                           (sfx_slider_x, sfx_slider_y),
                           (slider_width, slider_height),
                           globalvars.PREFERENCES.sfx_volume_val)

    # ================== Options menu is in-game =================== #
    if game_menu_options:
        button_width = 80
        button_height = 25

        save_button_x = center_x - button_width
        save_button_text = "Save game"

        mm_button_x = center_x + button_width
        mm_button_y = menu_rect.bottom - 30

        main_menu_button = gui.GuiButton(surface_option_menu, "Main Menu",
                                         (mm_button_x, mm_button_y),
                                         (button_width, button_height),
                                         color_button_hovered=constants.COLOR_BLACK,
                                         color_button_default=constants.COLOR_GREY,
                                         color_text_hovered=constants.COLOR_WHITE,
                                         color_text_default=constants.COLOR_WHITE)

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_option_menu, save_button_text,
                                (save_button_x, save_button_y),
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

        # volume values before updating
        current_music_vol = globalvars.PREFERENCES.music_volume_val
        current_sfx_vol = globalvars.PREFERENCES.sfx_volume_val

        # Update slider when mouse is dragging over the sfx slider
        music_slider.update(player_events)
        sfx_slider.update(player_events)

        # Update any changes
        if music_slider.slider_value is not current_music_vol:
            globalvars.PREFERENCES.music_volume_val = music_slider.slider_value
            globalvars.ASSETS.volume_adjust()

        elif sfx_slider.slider_value is not current_sfx_vol:
            globalvars.PREFERENCES.sfx_volume_val = sfx_slider.slider_value
            globalvars.ASSETS.volume_adjust()

        if save_button.update(player_events):
            if game_menu_options:
                game.ingame_save()
                print("game saved")
                # causing problems as need to quit options menu first, which enters main game loop for a few frames
                # and the draw_game() can't draw saved game cuz when it saves, it turns stuff to none..?
            else:
                game.preferences_save()
                menu_close = True

        # draw functions
        text.draw_text(surface_option_menu, "Options", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_WHITE,
                       center=True)

        music_slider.draw()
        text.draw_text(surface_option_menu, "Music Volume", constants.FONT_BEST,
                       (music_slider_x, music_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)

        sfx_slider.draw()
        text.draw_text(surface_option_menu, "SFX Volume", constants.FONT_BEST,
                       (sfx_slider_x, sfx_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)

        save_button.draw()

        if game_menu_options:

            if main_menu_button.update(player_events):
                globalvars.GAME_QUIT = True
                menu_close = True

            main_menu_button.draw()
            globalvars.CLOCK.tick(constants.GAME_FPS)

        # update display
        globalvars.SURFACE_MAIN.blit(surface_option_menu, menu_rect.topleft, menu_rect)
        surface_option_menu.fill(constants.COLOR_BROWN)
        pygame.display.update()
