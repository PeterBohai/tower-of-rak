# Standard library imports
import numpy

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, text, gui, game, draw


def menu_main_options(ingame_menu_options=False):

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 448
    menu_height = 224

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # title
    title_x = center_x
    title_y = menu_rect.top + 30

    # ================= button variables ================ #

    button_width = 64
    button_height = 32
    back_button_width = 96
    button_offset = button_height + 12
    long_button_width = 160

    save_button_x = center_x
    save_button_y = menu_rect.bottom - 30
    save_button_text = "SAVE"

    back_button_x = center_x
    back_button_y = menu_rect.bottom - 30
    back_button_text = "BACK"

    audio_button_x = center_x
    audio_button_y = menu_rect.top + 80
    audio_button_text = "Audio Settings"

    controls_button_x = center_x
    controls_button_y = audio_button_y + button_offset
    controls_button_text = "Control Settings"

    # ================== Options menu is in-game =================== #
    if ingame_menu_options:
        button_width = 96
        back_button_width = 64

        save_button_text = "Save game"

        back_button_x = center_x
        save_button_x = back_button_x - (button_width + button_offset)

        mm_button_x = back_button_x + (button_width + button_offset)
        mm_button_y = menu_rect.bottom - 30

        main_menu_button = gui.GuiButton(surface_menu, "Main Menu",
                                         (mm_button_x, mm_button_y),
                                         (button_width, button_height))

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y),
                                (button_width, button_height))

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (back_button_width, button_height))

    audio_button = gui.GuiButton(surface_menu, audio_button_text,
                                 (audio_button_x, audio_button_y),
                                 (long_button_width, button_height))

    controls_button = gui.GuiButton(surface_menu, controls_button_text,
                                    (controls_button_x, controls_button_y),
                                    (long_button_width, button_height))

    # menu background tile positions
    topL = menu_rect.topleft
    topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))

    # ====================== menu LOOP ===================== #
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

        # >>> button actions <<<
        if back_button.update(player_events):
            menu_close = True
        if audio_button.update(player_events):
            menu_options_audio()
        if controls_button.update(player_events):
            menu_options_controls()
            if ingame_menu_options:
                draw.draw_game()
            else:
                globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.S_MAIN_MENU, (0, 0))
                text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak",
                               constants.FONT_GAME_TITLE,
                               (center_x, constants.CAMERA_HEIGHT / 4),
                               constants.COLOR_RED,
                               center=True)

        # draw functions
        text.draw_text(surface_menu, "Options", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)
        back_button.draw()
        audio_button.draw()
        controls_button.draw()

        if ingame_menu_options:

            if main_menu_button.update(player_events):
                globalvars.GAME_QUIT = True
                menu_close = True

            if save_button.update(player_events):
                game.ingame_save()

            main_menu_button.draw()
            save_button.draw()
            globalvars.CLOCK.tick(constants.GAME_FPS)

        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)

        # blit the corners
        surface_menu.blit(globalvars.ASSETS.S_TOP_L_MENU_BROWN, topL)
        surface_menu.blit(globalvars.ASSETS.S_TOP_R_MENU_BROWN, topR)
        surface_menu.blit(globalvars.ASSETS.S_BOT_L_MENU_BROWN, botL)
        surface_menu.blit(globalvars.ASSETS.S_BOT_R_MENU_BROWN, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width/32) - 2        # number of tiles width-wise ignoring the 2 corners
        num_tiles_height = int(menu_height / 32) - 2     # number of tiles height-wise ignoring the 2 corners

        for w in range(1, num_tiles_width + 1):
            surface_menu.blit(globalvars.ASSETS.S_TOP_MENU_BROWN, tuple(numpy.add(topL, (32 * w, 0))))
            surface_menu.blit(globalvars.ASSETS.S_BOT_MENU_BROWN, tuple(numpy.add(botL, (32 * w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            surface_menu.blit(globalvars.ASSETS.S_SIDE_L_MENU_BROWN, tuple(numpy.add(topL, (0, 32 * h))))
            surface_menu.blit(globalvars.ASSETS.S_SIDE_R_MENU_BROWN, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                surface_menu.blit(globalvars.ASSETS.S_MID_MENU_BROWN, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


def menu_options_audio():

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 448
    menu_height = 224

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
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
    button_width = 64
    button_height = 32
    back_button_width = 64
    button_offset = int(button_height/2)

    save_button_x = center_x - button_width
    save_button_y = menu_rect.bottom - 30
    save_button_text = "SAVE"

    back_button_x = center_x + button_width
    back_button_y = menu_rect.bottom - 30
    back_button_text = "BACK"

    # ============== volume slider initialization ============== #

    music_slider = gui.GuiSlider(surface_menu,
                                 (music_slider_x, music_slider_y),
                                 (slider_width, slider_height),
                                 globalvars.PREFERENCES.music_volume_val)

    sfx_slider = gui.GuiSlider(surface_menu,
                               (sfx_slider_x, sfx_slider_y),
                               (slider_width, slider_height),
                               globalvars.PREFERENCES.sfx_volume_val)

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y),
                                (button_width, button_height))

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (back_button_width, button_height))

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
            game.preferences_save()
            menu_close = True

        if back_button.update(player_events):
            menu_close = True

        # draw functions
        text.draw_text(surface_menu, "AUDIO", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)

        music_slider.draw()
        text.draw_text(surface_menu, "Music Volume", constants.FONT_BEST,
                       (music_slider_x, music_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)

        sfx_slider.draw()
        text.draw_text(surface_menu, "SFX Volume", constants.FONT_BEST,
                       (sfx_slider_x, sfx_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)

        save_button.draw()

        back_button.draw()

        # background tile positions
        topL = menu_rect.topleft
        topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
        botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
        botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))


        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)

        # blit the corners
        surface_menu.blit(globalvars.ASSETS.S_TOP_L_MENU_BROWN, topL)
        surface_menu.blit(globalvars.ASSETS.S_TOP_R_MENU_BROWN, topR)
        surface_menu.blit(globalvars.ASSETS.S_BOT_L_MENU_BROWN, botL)
        surface_menu.blit(globalvars.ASSETS.S_BOT_R_MENU_BROWN, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width/32) - 2        # number of tiles width-wise ignoring the 2 corners
        num_tiles_height = int(menu_height / 32) - 2     # number of tiles height-wise ignoring the 2 corners

        for w in range(1, num_tiles_width + 1):
            surface_menu.blit(globalvars.ASSETS.S_TOP_MENU_BROWN, tuple(numpy.add(topL, (32 * w, 0))))
            surface_menu.blit(globalvars.ASSETS.S_BOT_MENU_BROWN, tuple(numpy.add(botL, (32 * w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            surface_menu.blit(globalvars.ASSETS.S_SIDE_L_MENU_BROWN, tuple(numpy.add(topL, (0, 32 * h))))
            surface_menu.blit(globalvars.ASSETS.S_SIDE_R_MENU_BROWN, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                surface_menu.blit(globalvars.ASSETS.S_MID_MENU_BROWN, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


def menu_options_controls():

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 448
    menu_height = 480

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # title
    title_x = center_x
    title_y = menu_rect.top + 30

    # ================= slider/button variables ================ #

    # buttons
    button_width = 64
    button_height = 32
    back_button_width = 64
    button_offset = int(button_height/2)
    small_button_width = 50
    small_button_height = 32

    save_button_x = center_x - button_width
    save_button_y = menu_rect.bottom - 30
    save_button_text = "SAVE"

    back_button_x = center_x + button_width
    back_button_y = menu_rect.bottom - 30
    back_button_text = "BACK"

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y),
                                (button_width, button_height))

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (back_button_width, button_height))



    # menu background tile positions
    topL = menu_rect.topleft
    topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))

    # text positions
    text_x = menu_rect.left + 32
    text_y_offset = text.helper_text_height(constants.FONT_BEST) + 24
    line_y = [title_y + 40]
    for line in range(1, 20):
        line_y.append(line_y[0] + line * text_y_offset)

    keys_button_x = center_x
    keys_button_y = list(map(lambda x: x + int(small_button_height/2) - 8, line_y[::]))

    esc_button_text = "Esc"


    # ====================== Menu LOOP ===================== #
    menu_close = False
    while not menu_close:
        left_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["left"][0],
                                    (keys_button_x, keys_button_y[0]),
                                    (small_button_width, small_button_height))
        right_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["right"][0],
                                     (keys_button_x, keys_button_y[1]),
                                     (small_button_width, small_button_height))
        up_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["up"][0],
                                  (keys_button_x, keys_button_y[2]),
                                  (small_button_width, small_button_height))
        down_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["down"][0],
                                    (keys_button_x, keys_button_y[3]),
                                    (small_button_width, small_button_height))
        grab_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["grab"][0],
                                    (keys_button_x, keys_button_y[4]),
                                    (small_button_width, small_button_height))
        drop_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["drop"][0],
                                    (keys_button_x, keys_button_y[5]),
                                    (small_button_width, small_button_height))
        inventory_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["inventory"][0],
                                         (keys_button_x, keys_button_y[6]),
                                         (small_button_width, small_button_height))
        next_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["next"][0],
                                    (keys_button_x, keys_button_y[7]),
                                    (small_button_width, small_button_height))
        esc_button = gui.GuiButton(surface_menu, globalvars.PREFERENCES.keybindings["back"][0],
                                   (keys_button_x, keys_button_y[8]),
                                   (small_button_width, small_button_height))

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        player_events = (events_list, mouse_pos)

        # process player input
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        if save_button.update(player_events):
            game.preferences_save()
            menu_close = True

        if back_button.update(player_events):
            menu_close = True

        if left_button.update(player_events):
            menu_change_controls("left")

        if right_button.update(player_events):
            menu_change_controls("right")

        if up_button.update(player_events):
            menu_change_controls("up")

        if down_button.update(player_events):
            menu_change_controls("down")

        if grab_button.update(player_events):
            menu_change_controls("grab")

        if drop_button.update(player_events):
            menu_change_controls("drop")

        if inventory_button.update(player_events):
            menu_change_controls("inventory")

        if next_button.update(player_events):
            menu_change_controls("next")

        if esc_button.update(player_events):
            menu_change_controls("back")


        # draw functions
        text.draw_text(surface_menu, "CONTROLS", constants.FONT_MENU_TITLE,
                       (title_x, title_y), constants.COLOR_BLACK, center=True)

        text.draw_text(surface_menu, "Move Left",
                       constants.FONT_BEST, (text_x, line_y[0]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Move Right",
                       constants.FONT_BEST, (text_x, line_y[1]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Move Up",
                       constants.FONT_BEST, (text_x, line_y[2]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Move Down",
                       constants.FONT_BEST, (text_x, line_y[3]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Grab Item",
                       constants.FONT_BEST, (text_x, line_y[4]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Drop Item",
                       constants.FONT_BEST, (text_x, line_y[5]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Inventory",
                       constants.FONT_BEST, (text_x, line_y[6]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Next Floor",
                       constants.FONT_BEST, (text_x, line_y[7]), constants.COLOR_BLACK)

        text.draw_text(surface_menu, "Back/Exit",
                       constants.FONT_BEST, (text_x, line_y[8]), constants.COLOR_BLACK)

        save_button.draw()
        back_button.draw()
        left_button.draw()
        right_button.draw()
        up_button.draw()
        down_button.draw()
        grab_button.draw()
        drop_button.draw()
        inventory_button.draw()
        next_button.draw()
        esc_button.draw()

        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)

        # blit the corners
        surface_menu.blit(globalvars.ASSETS.S_TOP_L_MENU_BROWN, topL)
        surface_menu.blit(globalvars.ASSETS.S_TOP_R_MENU_BROWN, topR)
        surface_menu.blit(globalvars.ASSETS.S_BOT_L_MENU_BROWN, botL)
        surface_menu.blit(globalvars.ASSETS.S_BOT_R_MENU_BROWN, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width/32) - 2        # number of tiles width-wise ignoring the 2 corners
        num_tiles_height = int(menu_height / 32) - 2     # number of tiles height-wise ignoring the 2 corners

        for w in range(1, num_tiles_width + 1):
            surface_menu.blit(globalvars.ASSETS.S_TOP_MENU_BROWN, tuple(numpy.add(topL, (32 * w, 0))))
            surface_menu.blit(globalvars.ASSETS.S_BOT_MENU_BROWN, tuple(numpy.add(botL, (32 * w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            surface_menu.blit(globalvars.ASSETS.S_SIDE_L_MENU_BROWN, tuple(numpy.add(topL, (0, 32 * h))))
            surface_menu.blit(globalvars.ASSETS.S_SIDE_R_MENU_BROWN, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                surface_menu.blit(globalvars.ASSETS.S_MID_MENU_BROWN, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


def menu_change_controls(action):

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 320
    menu_height = 128

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # message
    message_x = center_x
    message_y = center_y - text.helper_text_height(constants.FONT_BEST) + 5
    text_y_offset = text.helper_text_height(constants.FONT_BEST) + 10

    # menu loop
    menu_close = False
    while not menu_close:

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        pressed_key_list = pygame.key.get_pressed()
        shift_pressed = (pressed_key_list[pygame.K_RSHIFT] or pressed_key_list[pygame.K_LSHIFT])

        player_events = (events_list, mouse_pos)

        # process player input
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

                elif not shift_pressed:
                    non_alpha_num = {"period": ".",
                                     "comma": ",",
                                     "forward slash": "/",
                                     "semicolon": ";",
                                     "quote": "'",
                                     "left bracket": "[",
                                     "right bracket": "]",
                                     "backslash": "\\",
                                     "minus sign": "-",
                                     "equals sign": "="}

                    if pygame.key.name(event.key).isalnum():
                        key_char = pygame.key.name(event.key).upper()
                    else:
                        key_char = non_alpha_num[pygame.key.name(event.key)]

                    globalvars.PREFERENCES.keybindings[action] = (key_char, event.key)
                    menu_close = True

                elif shift_pressed and event.key == pygame.K_PERIOD:
                    globalvars.PREFERENCES.keybindings[action] = (">", event.key, pygame.K_LSHIFT)
                    menu_close = True

                elif shift_pressed and event.key == pygame.K_COMMA:
                    globalvars.PREFERENCES.keybindings[action] = ("<", event.key, pygame.K_LSHIFT)
                    menu_close = True

                elif shift_pressed and event.key == pygame.K_6:
                    globalvars.PREFERENCES.keybindings[action] = ("^", event.key, pygame.K_LSHIFT)
                    menu_close = True

                elif shift_pressed and event.key == pygame.K_SLASH:
                    globalvars.PREFERENCES.keybindings[action] = ("?", event.key, pygame.K_LSHIFT)
                    menu_close = True

                else:
                    key_char = globalvars.PREFERENCES.keybindings[action][0]
                    globalvars.PREFERENCES.keybindings[action] = (key_char, event.key, pygame.K_LSHIFT)
                    menu_close = True



        # draw functions
        text.draw_text(surface_menu, "Press any character to change.", constants.FONT_BEST,
                       (message_x, message_y ),
                       constants.COLOR_BLACK, center=True)

        text.draw_text(surface_menu, "Or press 'Esc' key to cancel.", constants.FONT_BEST,
                       (message_x, message_y + text_y_offset),
                       constants.COLOR_BLACK, center=True)

        # background tile positions
        topL = menu_rect.topleft
        topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
        botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
        botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))


        # >>>>> update display <<<<<
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)

        # blit the corners
        surface_menu.blit(globalvars.ASSETS.S_TOP_L_MENU_BROWN, topL)
        surface_menu.blit(globalvars.ASSETS.S_TOP_R_MENU_BROWN, topR)
        surface_menu.blit(globalvars.ASSETS.S_BOT_L_MENU_BROWN, botL)
        surface_menu.blit(globalvars.ASSETS.S_BOT_R_MENU_BROWN, botR)

        # blit the top and bottom
        num_tiles_width = int(menu_width/32) - 2        # number of tiles width-wise ignoring the 2 corners
        num_tiles_height = int(menu_height / 32) - 2     # number of tiles height-wise ignoring the 2 corners

        for w in range(1, num_tiles_width + 1):
            surface_menu.blit(globalvars.ASSETS.S_TOP_MENU_BROWN, tuple(numpy.add(topL, (32 * w, 0))))
            surface_menu.blit(globalvars.ASSETS.S_BOT_MENU_BROWN, tuple(numpy.add(botL, (32 * w, 0))))

        # blit the left and right sides
        for h in range(1, num_tiles_height + 1):
            surface_menu.blit(globalvars.ASSETS.S_SIDE_L_MENU_BROWN, tuple(numpy.add(topL, (0, 32 * h))))
            surface_menu.blit(globalvars.ASSETS.S_SIDE_R_MENU_BROWN, tuple(numpy.add(topR, (0, 32 * h))))

        # blit the middle pieces
        for r in range(1, num_tiles_height + 1):
            for c in range(1, num_tiles_width + 1):
                surface_menu.blit(globalvars.ASSETS.S_MID_MENU_BROWN, tuple(numpy.add(topL, (32 * c, 32 * r))))

        pygame.display.update()


