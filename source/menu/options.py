# Standard library imports
import numpy, copy

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, text, gui, game, draw


def menu_main_options(ingame_menu_options=False):

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 448
    menu_height = 256

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
    button_list = []

    button_width = 64
    button_height = 32
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

    display_button_x = center_x
    display_button_y = controls_button_y + button_offset
    display_button_text = "Display Settings"

    # ================== Options menu is in-game =================== #
    if ingame_menu_options:
        button_width = 96

        save_button_text = "Save game"

        back_button_x = center_x
        save_button_x = back_button_x - (button_width + button_offset)

        mm_button_x = back_button_x + (button_width + button_offset)
        mm_button_y = menu_rect.bottom - 30

        main_menu_button = gui.GuiButton(surface_menu, "Main Menu",
                                         (mm_button_x, mm_button_y),
                                         (button_width, button_height))
        button_list.append(main_menu_button)

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y),
                                (button_width, button_height))
    button_list.append(save_button)

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (button_width, button_height))
    button_list.append(back_button)

    audio_button = gui.GuiButton(surface_menu, audio_button_text,
                                 (audio_button_x, audio_button_y),
                                 (long_button_width, button_height))
    button_list.append(audio_button)

    controls_button = gui.GuiButton(surface_menu, controls_button_text,
                                    (controls_button_x, controls_button_y),
                                    (long_button_width, button_height))
    button_list.append(controls_button)

    display_button = gui.GuiButton(surface_menu, display_button_text,
                                   (display_button_x, display_button_y),
                                   (long_button_width, button_height))
    button_list.append(display_button)

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
        if display_button.update(player_events):
            menu_options_display()

        # Change cursor when hovering over a button
        for i, button in enumerate(button_list):
            if button.mouse_hover:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
            if i == len(button_list) - 1:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        # draw functions
        text.draw_text(surface_menu, "Options", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)
        back_button.draw()
        audio_button.draw()
        controls_button.draw()
        display_button.draw()

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
    menu_height = 256

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
    button_list = []
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
    button_list.append(save_button)

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (button_width, button_height))
    button_list.append(back_button)

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

        if back_button.update(player_events):
            menu_close = True

        # Change cursor when hovering over a button
        for i, buttons in enumerate(button_list):
            if buttons.mouse_hover:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
            if i == len(button_list) - 1:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)

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
    menu_height = 416

    scroll_window_width = menu_width - (2 * constants.CELL_WIDTH)
    scroll_window_height = menu_height - 70 - 64

    controls_height = 448

    # window coordinates
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    # =============== options menu surface init =============== #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    surface_scroll_window = pygame.Surface((scroll_window_width, scroll_window_height))
    menu_x, menu_y = menu_rect.topleft
    scroll_window_pos = (menu_x + 32, menu_y + 70)

    surface_controls = pygame.Surface((scroll_window_width, controls_height))
    surface_controls.fill((184, 163, 143))
    scroll_y = 0

    # title
    title_x = center_x
    title_y = menu_rect.top + 30

    # ================= button variables ================ #

    # buttons
    button_list = []

    button_width = 64
    button_height = 32
    small_button_width = 50
    small_button_height = 32
    button_x_offset = button_width + 32

    save_button_x = center_x
    save_button_y = menu_rect.bottom - 30
    save_button_text = "SAVE"

    back_button_x = center_x + button_x_offset
    back_button_y = menu_rect.bottom - 30
    back_button_text = "BACK"

    reset_button_x = center_x - button_x_offset
    reset_button_y = menu_rect.bottom - 30
    reset_button_text = "RESET"

    # ====================== button section ===================== #

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y),
                                (button_width, button_height))

    button_list.append(save_button)

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (button_width, button_height))
    button_list.append(back_button)

    reset_button = gui.GuiButton(surface_menu, reset_button_text,
                                 (reset_button_x, reset_button_y),
                                 (button_width, button_height))
    button_list.append(reset_button)

    # menu background tile positions
    topL = menu_rect.topleft
    topR = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    botL = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    botR = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))

    # text positions
    text_x = 0
    text_y_offset = text.helper_text_height(constants.FONT_BEST) + 24
    line_y = [8]      # [title_y + 40]
    for line in range(1, 20):
        line_y.append(line_y[0] + line * text_y_offset)

    keys_button_x = scroll_window_width/2
    keys_button_y = list(map(lambda x: x + int(small_button_height/2) - 8, line_y[::]))

    previous_key_bindings = copy.deepcopy(globalvars.PREFERENCES.keybindings)

    left_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["left"][0],
                                (keys_button_x, keys_button_y[0]),
                                (small_button_width, small_button_height))

    right_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["right"][0],
                                 (keys_button_x, keys_button_y[1]),
                                 (small_button_width, small_button_height))

    up_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["up"][0],
                              (keys_button_x, keys_button_y[2]),
                              (small_button_width, small_button_height))

    down_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["down"][0],
                                (keys_button_x, keys_button_y[3]),
                                (small_button_width, small_button_height))

    stay_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["stay"][0],
                                (keys_button_x, keys_button_y[4]),
                                (small_button_width, small_button_height))

    grab_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["grab"][0],
                                (keys_button_x, keys_button_y[5]),
                                (small_button_width, small_button_height))

    drop_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["drop"][0],
                                (keys_button_x, keys_button_y[6]),
                                (small_button_width, small_button_height))

    inventory_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["inventory"][0],
                                     (keys_button_x, keys_button_y[7]),
                                     (small_button_width, small_button_height))

    next_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["next"][0],
                                (keys_button_x, keys_button_y[8]),
                                (small_button_width, small_button_height))

    esc_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["back"][0],
                               (keys_button_x, keys_button_y[9]),
                               (small_button_width, small_button_height))

    # ====================== Menu LOOP ===================== #
    menu_close = False
    saved = False
    while not menu_close:

        left_button.text = globalvars.PREFERENCES.keybindings["left"][0]
        right_button.text = globalvars.PREFERENCES.keybindings["right"][0]
        up_button.text = globalvars.PREFERENCES.keybindings["up"][0]
        down_button.text = globalvars.PREFERENCES.keybindings["down"][0]
        stay_button.text = globalvars.PREFERENCES.keybindings["stay"][0]
        grab_button.text = globalvars.PREFERENCES.keybindings["grab"][0]
        drop_button.text = globalvars.PREFERENCES.keybindings["drop"][0]
        inventory_button.text = globalvars.PREFERENCES.keybindings["inventory"][0]
        next_button.text = globalvars.PREFERENCES.keybindings["next"][0]
        esc_button.text = globalvars.PREFERENCES.keybindings["back"][0]

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # update relative mouse position
        mouse_x, mouse_y = mouse_pos
        mouse_rel_x = mouse_x -scroll_window_pos[0]
        mouse_rel_y = mouse_y - (scroll_window_pos[1] + scroll_y)
        mouse_rel_pos = (mouse_rel_x, mouse_rel_y)
        if mouse_y > (scroll_window_pos[1] + scroll_window_height):
            mouse_rel_pos = (0, 0)

        player_events = (events_list, mouse_pos)
        player_events_rel = (events_list, mouse_rel_pos)

        # process player input
        for event in events_list:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    # will not save controls if exit without selecting "SAVE"
                    if not saved:
                        globalvars.PREFERENCES.keybindings = previous_key_bindings
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = min(scroll_y + 15, 0)
                if event.button == 5:
                    scroll_y = max(scroll_y - 15, -(controls_height- scroll_window_height))

        if save_button.update(player_events):
            saved = True
            game.preferences_save()

        if back_button.update(player_events):
            # will not save controls if exit without selecting "SAVE"
            if not saved:
                globalvars.PREFERENCES.keybindings = previous_key_bindings
            menu_close = True

        if reset_button.update(player_events):
            globalvars.PREFERENCES.keybindings = copy.deepcopy(globalvars.PREFERENCES.default_keybindings)

        # update control buttons
        if left_button.update(player_events_rel):
            menu_change_controls("left")
            saved = False

        if right_button.update(player_events_rel):
            menu_change_controls("right")
            saved = False

        if up_button.update(player_events_rel):
            menu_change_controls("up")
            saved = False

        if down_button.update(player_events_rel):
            menu_change_controls("down")
            saved = False

        if stay_button.update(player_events_rel):
            menu_change_controls("stay")
            saved = False

        if grab_button.update(player_events_rel):
            menu_change_controls("grab")
            saved = False

        if drop_button.update(player_events_rel):
            menu_change_controls("drop")
            saved = False

        if inventory_button.update(player_events_rel):
            menu_change_controls("inventory")
            saved = False

        if next_button.update(player_events_rel):
            menu_change_controls("next")
            saved = False

        if esc_button.update(player_events_rel):
            menu_change_controls("back")
            saved = False

        # Change cursor when hovering over a button
        for i, button in enumerate(button_list):
            if button.mouse_hover:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
            if i == len(button_list) - 1:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        # draw functions

        text.draw_text(surface_controls, "Move Left",
                       constants.FONT_BEST, (text_x, line_y[0]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Move Right",
                       constants.FONT_BEST, (text_x, line_y[1]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Move Up",
                       constants.FONT_BEST, (text_x, line_y[2]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Move Down",
                       constants.FONT_BEST, (text_x, line_y[3]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Stay",
                       constants.FONT_BEST, (text_x, line_y[4]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Grab Item",
                       constants.FONT_BEST, (text_x, line_y[5]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Drop Item",
                       constants.FONT_BEST, (text_x, line_y[6]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Inventory",
                       constants.FONT_BEST, (text_x, line_y[7]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Next Floor",
                       constants.FONT_BEST, (text_x, line_y[8]), constants.COLOR_BLACK)

        text.draw_text(surface_controls, "Back/Exit",
                       constants.FONT_BEST, (text_x, line_y[9]), constants.COLOR_BLACK)


        left_button.draw()
        right_button.draw()
        up_button.draw()
        down_button.draw()
        stay_button.draw()
        grab_button.draw()
        drop_button.draw()
        inventory_button.draw()
        next_button.draw()
        esc_button.draw()

        # >>>>> update display <<<<<
        surface_scroll_window.blit(surface_controls, (0, scroll_y))

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

        # display scroll window
        surface_menu.blit(surface_scroll_window, scroll_window_pos)

        text.draw_text(surface_menu, "CONTROLS", constants.FONT_MENU_TITLE,
                       (title_x, title_y), constants.COLOR_BLACK, center=True)
        save_button.draw()
        back_button.draw()
        reset_button.draw()
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)

        pygame.display.update()


def menu_change_controls(action):

    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 352
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

    # =============== Menu LOOP =============== #
    menu_close = False
    is_duplicate = False
    is_invalid = False

    while not menu_close:

        # get player input
        events_list = pygame.event.get()
        pressed_key_list = pygame.key.get_pressed()
        shift_pressed = (pressed_key_list[pygame.K_RSHIFT] or pressed_key_list[pygame.K_LSHIFT])

        if is_duplicate:
            text_1 = "Already in use, please choose another."
        elif is_invalid:
            text_1 = "Please choose a valid character."
        else:
            text_1 = "Press any character to change."

        text_2 = "Or press 'Esc' key to cancel."

        arrow_keys = {"up": "↑",
                      "down": "↓",
                      "left": "←",
                      "right": "→",
                      "space": "Spc"}

        shift_chars = {pygame.K_PERIOD: ">",
                       pygame.K_COMMA: "<",
                       pygame.K_SLASH: "?",
                       pygame.K_SEMICOLON: ":",
                       pygame.K_QUOTE: "\"",
                       pygame.K_LEFTBRACKET: "{",
                       pygame.K_RIGHTBRACKET: "}",
                       pygame.K_BACKSLASH: "|",
                       pygame.K_MINUS: "_",
                       pygame.K_EQUALS: "+",
                       pygame.K_BACKQUOTE: "~",
                       pygame.K_1: "!",
                       pygame.K_2: "@",
                       pygame.K_3: "#",
                       pygame.K_4: "$",
                       pygame.K_5: "%",
                       pygame.K_6: "^",
                       pygame.K_7: "&",
                       pygame.K_8: "*",
                       pygame.K_9: "(",
                       pygame.K_0: ")"}

        # process player input
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == pygame.K_ESCAPE:
                        menu_close = True

                    elif not shift_pressed:

                        if len(pygame.key.name(event.key)) > 1:
                            key_char = arrow_keys[pygame.key.name(event.key)]
                        else:
                            key_char = pygame.key.name(event.key).upper()

                        is_invalid = False
                        is_duplicate = False

                        # Check for duplicate keys
                        for tup in globalvars.PREFERENCES.keybindings.values():
                            if tup[0] == key_char:
                                key_char = globalvars.PREFERENCES.keybindings[action][0]
                                is_duplicate = True
                                break
                        if is_duplicate:
                            break

                        globalvars.PREFERENCES.keybindings[action] = (key_char, event.key)
                        menu_close = True

                    elif event.key in shift_chars.keys() and shift_pressed:
                        key_char = shift_chars[event.key]

                        is_invalid = False
                        is_duplicate = False

                        # Check for duplicate keys
                        for tup in globalvars.PREFERENCES.keybindings.values():
                            if tup[0] == key_char:
                                key_char = globalvars.PREFERENCES.keybindings[action][0]
                                is_duplicate = True
                                break
                        if is_duplicate:
                            break

                        globalvars.PREFERENCES.keybindings[action] = (key_char, event.key, pygame.K_LSHIFT)
                        menu_close = True

                except:
                    is_invalid = True
                    break


        # draw functions
        text.draw_text(surface_menu, text_1, constants.FONT_BEST,
                       (message_x, message_y),
                       constants.COLOR_BLACK, center=True)

        text.draw_text(surface_menu, text_2, constants.FONT_BEST,
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


def menu_options_display():
    # ============== options menu dimensions ============== #
    # options menu dimensions (in MAIN MENU)
    menu_width = 448
    menu_height = 256

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
    button_list = []

    button_width = 64
    button_height = 32
    button_offset = button_height + 12
    long_button_width = 160

    back_button_x = center_x
    back_button_y = menu_rect.bottom - 30
    back_button_text = "BACK"

    default_button_x = center_x
    default_button_y = menu_rect.top + 80
    default_button_text = "Default Screen"

    fill_button_x = center_x
    fill_button_y = default_button_y + button_offset
    fill_button_text = "Fill Screen"

    fullscreen_button_x = center_x
    fullscreen_button_y = fill_button_y + button_offset
    fullscreen_button_text = "Fullscreen"

    # ====================== button section ===================== #

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y),
                                (button_width, button_height))
    button_list.append(back_button)

    default_button = gui.GuiButton(surface_menu, default_button_text,
                                   (default_button_x, default_button_y),
                                   (long_button_width, button_height))
    button_list.append(default_button)

    fill_button = gui.GuiButton(surface_menu, fill_button_text,
                                (fill_button_x, fill_button_y),
                                (long_button_width, button_height))
    button_list.append(fill_button)

    fullscreen_button = gui.GuiButton(surface_menu, fullscreen_button_text,
                                      (fullscreen_button_x, fullscreen_button_y),
                                      (long_button_width, button_height))
    button_list.append(fullscreen_button)

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
                    game.preferences_save()
                    menu_close = True

        # >>> button actions <<<

        if back_button.update(player_events):
            game.preferences_save()
            menu_close = True

        if default_button.update(player_events):
            constants.CAMERA_WIDTH = constants.CAMERA_WIDTH_DEFAULT
            constants.CAMERA_HEIGHT = constants.CAMERA_HEIGHT_DEFAULT
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT

            globalvars.PREFERENCES.display_window = "default"
            globalvars.DISPLAY_CHANGE = True

        if fill_button.update(player_events):
            constants.CAMERA_WIDTH = constants.screen_width
            constants.CAMERA_HEIGHT = constants.screen_height - 45
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT

            globalvars.PREFERENCES.display_window = "fill"
            globalvars.DISPLAY_CHANGE = True

        if fullscreen_button.update(player_events):
            constants.CAMERA_WIDTH = constants.screen_width
            constants.CAMERA_HEIGHT = constants.screen_height
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT

            globalvars.PREFERENCES.display_window = "fullscreen"
            globalvars.DISPLAY_CHANGE = True

        # Change cursor when hovering over a button
        for i, button in enumerate(button_list):
            if button.mouse_hover:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
            if i == len(button_list) - 1:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        # draw functions
        text.draw_text(surface_menu, "Display Settings", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)
        back_button.draw()
        default_button.draw()
        fill_button.draw()
        fullscreen_button.draw()

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
