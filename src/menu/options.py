import copy

import numpy
import pygame

from src import constants, globalvars, text, gui, game, draw
from src.menu import popup, mainmenu

# Standard button attributes
button_wh = (64, 32)
button_wh_small = (50, 32)
button_wh_long = (160, 32)
back_button_text = "BACK"
save_button_text = "SAVE"

# Standard options menu specs
menu_width = 448


def main_options_menu(in_game=False):
    """The primary options menu that includes sub-menus like audio, control, display, etc.

    Parameters
    ----------
    in_game : bool, optional
        True if the menu was brought up in-game, False if in main menu.

    Returns
    -------
    None
    """

    # ----- menu specs ----- #
    menu_height = 256
    center_x, center_y = constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2

    # ----- initialize menu surface ----- #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    title_x = center_x
    title_y = menu_rect.top + 30

    # ----- button specs -----#
    button_width = 96 if in_game else 64
    button_height = 32
    button_offset = button_height + 12

    back_button_x = center_x
    back_button_y = menu_rect.bottom - 30

    save_button_x = back_button_x - (button_width + button_offset) if in_game else center_x
    save_button_y = menu_rect.bottom - 30

    audio_button_x = center_x
    audio_button_y = menu_rect.top + 80

    controls_button_x = center_x
    controls_button_y = audio_button_y + button_offset

    display_button_x = center_x
    display_button_y = controls_button_y + button_offset

    # ----- create buttons ----- #
    save_button = gui.GuiButton(surface_menu, "Save game" if in_game else save_button_text,
                                (save_button_x, save_button_y), (button_width, button_height))

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y), (button_width, button_height))

    audio_button = gui.GuiButton(surface_menu, "Audio Settings",
                                 (audio_button_x, audio_button_y), button_wh_long)

    controls_button = gui.GuiButton(surface_menu, "Control Settings",
                                    (controls_button_x, controls_button_y), button_wh_long)

    display_button = gui.GuiButton(surface_menu, "Display Settings",
                                   (display_button_x, display_button_y), button_wh_long)

    button_list = [back_button, audio_button, controls_button, display_button]

    if in_game:
        mm_button_x = back_button_x + (button_width + button_offset)
        mm_button_y = menu_rect.bottom - 30

        main_menu_button = gui.GuiButton(surface_menu, "Main Menu",
                                         (mm_button_x, mm_button_y),
                                         (button_width, button_height))
        button_list.append(main_menu_button)
        button_list.append(save_button)

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

    # ==================== MENU LOOP ==================== #
    menu_close = False
    while not menu_close:
        # ---- retrieve user input and events ----- #
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        player_events = (events_list, mouse_pos)

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        # ----- button event listeners ----- #
        if back_button.update(player_events):
            menu_close = True
        if audio_button.update(player_events):
            audio_options_menu()
        if controls_button.update(player_events):
            controls_options_menu()
            if in_game:
                draw.draw_game()
            else:
                globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.S_MAIN_MENU, (0, 0))
                text.draw_text(globalvars.SURFACE_MAIN, "Tower of Rak",
                               constants.FONT_GAME_TITLE,
                               (center_x, constants.CAMERA_HEIGHT / 4),
                               constants.COLOR_RED,
                               center=True)
        if display_button.update(player_events):
            display_options_menu()

        if in_game:
            if main_menu_button.update(player_events):
                globalvars.GAME_QUIT = True
                menu_close = True

            if save_button.update(player_events):
                game.game_save(in_game=True)
                popup.popup_menu("Saved game!")

            globalvars.CLOCK.tick(constants.GAME_FPS)

        # ----- display functions ----- #
        text.draw_text(surface_menu, "Options", constants.FONT_MENU_TITLE,
                       (title_x, title_y),
                       constants.COLOR_BLACK,
                       center=True)

        draw.draw_button_update_cursor(button_list)
        # update display
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(surface_menu, (menu_width, menu_height), *corner_positions)
        pygame.display.update()


def audio_options_menu():
    """Displays the options sub-menu for audio control.

    Returns
    -------
    None
    """

    # ----- menu specs ----- #
    menu_height = 256
    center_x, center_y = constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2

    # ----- initialize menu surface ----- #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    title_x = center_x
    title_y = menu_rect.top + 30

    # ----- slider and button specs ----- #
    slider_width = 170
    slider_height = 8
    slider_text_offset_y = 18

    music_slider_x = center_x
    music_slider_y = center_y - 20
    sfx_slider_x = music_slider_x
    sfx_slider_y = music_slider_y + 45

    save_button_x = center_x - button_wh[0]
    save_button_y = menu_rect.bottom - 30

    back_button_x = center_x + button_wh[0]
    back_button_y = menu_rect.bottom - 30

    # ----- create sliders and buttons ----- #
    music_slider = gui.GuiSlider(surface_menu, (music_slider_x, music_slider_y),
                                 (slider_width, slider_height),
                                 globalvars.PREFERENCES.music_volume_val)

    sfx_slider = gui.GuiSlider(surface_menu, (sfx_slider_x, sfx_slider_y),
                               (slider_width, slider_height),
                               globalvars.PREFERENCES.sfx_volume_val)

    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y), button_wh)

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y), button_wh)

    button_slider_list = (save_button, back_button, music_slider, sfx_slider)

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

    # ==================== MENU LOOP ==================== #
    menu_close = False
    while not menu_close:
        # ---- retrieve user input and events ----- #
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        player_events = (events_list, mouse_pos)

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        # volume values before updating
        current_music_vol = globalvars.PREFERENCES.music_volume_val
        current_sfx_vol = globalvars.PREFERENCES.sfx_volume_val

        # ----- button and slider event listeners ----- #
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

        # ----- display functions ----- #
        text.draw_text(surface_menu, "AUDIO", constants.FONT_MENU_TITLE, (title_x, title_y),
                       constants.COLOR_BLACK, center=True)
        text.draw_text(surface_menu, "Music Volume", constants.FONT_BEST,
                       (music_slider_x, music_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)
        text.draw_text(surface_menu, "SFX Volume", constants.FONT_BEST,
                       (sfx_slider_x, sfx_slider_y - slider_text_offset_y),
                       constants.COLOR_BLACK, center=True)

        draw.draw_button_update_cursor(button_slider_list)

        # update display
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(surface_menu, (menu_width, menu_height), *corner_positions)
        pygame.display.update()


def controls_options_menu():
    """Displays the options sub-menu for keybindings.

    Returns
    -------
    None
    """

    # ----- menu specs -----#
    menu_height = 416
    center_x, center_y = constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2
    scroll_window_width = menu_width - (2 * constants.CELL_WIDTH)
    scroll_window_height = menu_height - 70 - 64
    controls_height = 448

    # ----- initialize menu surface ----- #
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    surface_scroll_window = pygame.Surface((scroll_window_width, scroll_window_height))
    menu_x, menu_y = menu_rect.topleft
    scroll_window_pos = (menu_x + 32, menu_y + 70)

    surface_controls = pygame.Surface((scroll_window_width, controls_height))
    surface_controls.fill((184, 163, 143))
    scroll_y = 0

    # ----- text specs ----- #
    title_x = center_x
    title_y = menu_rect.top + 30

    text_x = 0
    text_y_first = 8
    text_y_offset = text.get_text_height(constants.FONT_BEST) + 24
    num_lines = 20
    line_y = [text_y_first + line * text_y_offset for line in range(num_lines)]
    descriptions = ("Move Left", "Move Right", "Move Up", "Move Down", "Stay",
                    "Grab Item", "Drop Item", "Inventory", "Next Floor", "Back/Exit")

    # ----- button specs ----- #
    button_x_offset = button_wh[0] + 32

    save_button_x = center_x
    save_button_y = menu_rect.bottom - 30

    back_button_x = center_x + button_x_offset
    back_button_y = menu_rect.bottom - 30

    reset_button_x = center_x - button_x_offset
    reset_button_y = menu_rect.bottom - 30
    reset_button_text = "RESET"

    keys_button_x = scroll_window_width // 2
    keys_button_y = [y_pos + button_wh_small[1] // 2 - 8 for y_pos in line_y]

    # ----- create buttons ----- #
    save_button = gui.GuiButton(surface_menu, save_button_text,
                                (save_button_x, save_button_y), button_wh)

    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y), button_wh)

    reset_button = gui.GuiButton(surface_menu, reset_button_text,
                                 (reset_button_x, reset_button_y), button_wh)
    # In-game controls buttons
    previous_key_bindings = copy.deepcopy(globalvars.PREFERENCES.keybindings)

    left_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["left"][0],
                                (keys_button_x, keys_button_y[0]), button_wh_small)

    right_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["right"][0],
                                 (keys_button_x, keys_button_y[1]), button_wh_small)

    up_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["up"][0],
                              (keys_button_x, keys_button_y[2]), button_wh_small)

    down_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["down"][0],
                                (keys_button_x, keys_button_y[3]), button_wh_small)

    stay_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["stay"][0],
                                (keys_button_x, keys_button_y[4]), button_wh_small)

    grab_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["grab"][0],
                                (keys_button_x, keys_button_y[5]), button_wh_small)

    drop_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["drop"][0],
                                (keys_button_x, keys_button_y[6]), button_wh_small)

    inventory_button = gui.GuiButton(surface_controls,
                                     globalvars.PREFERENCES.keybindings["inventory"][0],
                                     (keys_button_x, keys_button_y[7]), button_wh_small)

    next_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["next"][0],
                                (keys_button_x, keys_button_y[8]), button_wh_small)

    esc_button = gui.GuiButton(surface_controls, globalvars.PREFERENCES.keybindings["back"][0],
                               (keys_button_x, keys_button_y[9]), button_wh_small)

    button_list = [save_button, back_button, reset_button]
    game_buttons = [(left_button, "left"), (right_button, "right"), (up_button, "up"),
                    (down_button, "down"), (stay_button, "stay"), (grab_button, "grab"),
                    (drop_button, "drop"), (inventory_button, "inventory"), (next_button, "next"),
                    (esc_button, "back")]

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

    # ==================== MENU LOOP ==================== #
    menu_close = False
    saved = False
    while not menu_close:
        # ---- retrieve user input and events ----- #
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Update relative mouse position
        mouse_x, mouse_y = mouse_pos
        mouse_rel_x = mouse_x - scroll_window_pos[0]
        mouse_rel_y = mouse_y - (scroll_window_pos[1] + scroll_y)
        mouse_rel_pos = (mouse_rel_x, mouse_rel_y)
        if mouse_y > (scroll_window_pos[1] + scroll_window_height):
            mouse_rel_pos = (0, 0)

        player_events = (events_list, mouse_pos)
        player_events_rel = (events_list, mouse_rel_pos)

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
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
                    scroll_y = max(scroll_y - 15, -(controls_height - scroll_window_height))

        # ----- button click event listeners ----- #
        if save_button.update(player_events):
            saved = True
            game.preferences_save()
        if back_button.update(player_events):
            # will not save controls if exit without selecting "SAVE"
            if not saved:
                globalvars.PREFERENCES.keybindings = previous_key_bindings
            menu_close = True
        if reset_button.update(player_events):
            globalvars.PREFERENCES.keybindings = copy.deepcopy(
                globalvars.PREFERENCES.default_keybindings)

        # Trigger pop-up prompt window if user clicks on a game control button
        for button, action in game_buttons:
            # Constantly update button labels so that any changes are displayed in real-time
            button.text = globalvars.PREFERENCES.keybindings[action][0]
            if button.update(player_events_rel):
                menu_change_controls(action)
                saved = False

        # ----- display functions ----- #
        for i, desc in enumerate(descriptions):
            text.draw_text(surface_controls, desc, constants.FONT_BEST, (text_x, line_y[i]),
                           constants.COLOR_BLACK)

        surface_scroll_window.blit(surface_controls, (0, scroll_y))
        draw.draw_menu_background(surface_menu, (menu_width, menu_height), *corner_positions)
        draw.draw_button_update_cursor(button_list + [btn for btn, action in game_buttons])
        # display scroll window
        surface_menu.blit(surface_scroll_window, scroll_window_pos)
        text.draw_text(surface_menu, "CONTROLS", constants.FONT_MENU_TITLE,
                       (title_x, title_y), constants.COLOR_BLACK, center=True)
        # update main display
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        pygame.display.update()


def menu_change_controls(action):
    """Displays a pop-up prompt when player clicks on a key button to change in the controls menu.

    Returns
    -------
    None
    """

    # ----- menu specs -----#
    menu_width_sm, menu_height = 352, 128
    center_x, center_y = constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2

    # ----- initialize menu surface -----#
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width_sm, menu_height))
    menu_rect.center = (center_x, center_y)

    message_x = center_x
    message_y = center_y - text.get_text_height(constants.FONT_BEST) + 5
    text_y_offset = text.get_text_height(constants.FONT_BEST) + 10

    # background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

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

    # ==================== MENU LOOP ==================== #
    menu_close = False
    is_duplicate = False
    is_invalid = False

    while not menu_close:
        text_1 = "Press any character to change."
        text_2 = "Or press 'Esc' key to cancel."
        if is_duplicate:
            text_1 = "Already in use, please choose another."
        elif is_invalid:
            text_1 = "Please choose a valid character."

        # ---- retrieve user input and events ----- #
        events_list = pygame.event.get()
        pressed_key_list = pygame.key.get_pressed()
        shift_pressed = (pressed_key_list[pygame.K_RSHIFT] or pressed_key_list[pygame.K_LSHIFT])

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
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

        # ----- display functions ----- #
        text.draw_text(surface_menu, text_1, constants.FONT_BEST, (message_x, message_y),
                       constants.COLOR_BLACK, center=True)
        text.draw_text(surface_menu, text_2, constants.FONT_BEST, (message_x, message_y + text_y_offset),
                       constants.COLOR_BLACK, center=True)
        # update display
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(surface_menu, (menu_width_sm, menu_height), *corner_positions)
        pygame.display.update()


def display_options_menu():
    """Displays the options sub-menu for window display settings.

    Returns
    -------
    None
    """

    # ------ menu specs ----- #
    menu_height = 256
    center_x, center_y = constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2

    # ----- initialize menu surface -----#
    surface_menu = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    # ----- text specs ----- #
    title_x = center_x
    title_y = menu_rect.top + 30

    # ----- button specs ----- #
    button_offset = button_wh[1] + 12

    back_button_x = center_x
    back_button_y = menu_rect.bottom - 30

    default_button_x = center_x
    default_button_y = menu_rect.top + 80

    fill_button_x = center_x
    fill_button_y = default_button_y + button_offset

    fullscreen_button_x = center_x
    fullscreen_button_y = fill_button_y + button_offset

    # ----- create buttons ----- #
    back_button = gui.GuiButton(surface_menu, back_button_text,
                                (back_button_x, back_button_y), button_wh)

    default_button = gui.GuiButton(surface_menu, "Default Screen",
                                   (default_button_x, default_button_y), button_wh_long)

    fill_button = gui.GuiButton(surface_menu, "Fill Screen",
                                (fill_button_x, fill_button_y), button_wh_long)

    fullscreen_button = gui.GuiButton(surface_menu, "Fullscreen",
                                      (fullscreen_button_x, fullscreen_button_y), button_wh_long)

    button_list = (back_button, default_button, fill_button, fullscreen_button)

    # menu background tile positions
    top_r = tuple(numpy.subtract(menu_rect.topright, (32, 0)))
    bot_l = tuple(numpy.subtract(menu_rect.bottomleft, (0, 32)))
    bot_r = tuple(numpy.subtract(menu_rect.bottomright, (32, 32)))
    corner_positions = (menu_rect.topleft, top_r, bot_l, bot_r)

    # ==================== MENU LOOP ==================== #
    menu_close = False
    while not menu_close:
        # ---- retrieve user input and events ----- #
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        player_events = (events_list, mouse_pos)

        # ----- event listeners (user keyboard input) ----- #
        for event in events_list:
            if event.type == pygame.QUIT:
                mainmenu.perform_exit_sequence()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.preferences_save()
                    menu_close = True

        # ----- button click event listeners ----- #
        if back_button.update(player_events):
            game.preferences_save()
            menu_close = True

        if default_button.update(player_events):
            constants.CAMERA_WIDTH = constants.CAMERA_WIDTH_DEFAULT
            constants.CAMERA_HEIGHT = constants.CAMERA_HEIGHT_DEFAULT
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT
            globalvars.PREFERENCES.display_window = "default"

        if fill_button.update(player_events):
            constants.CAMERA_WIDTH = constants.screen_width
            constants.CAMERA_HEIGHT = constants.screen_height - 45
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT
            globalvars.PREFERENCES.display_window = "fill"

        if fullscreen_button.update(player_events):
            constants.CAMERA_WIDTH = constants.screen_width
            constants.CAMERA_HEIGHT = constants.screen_height
            globalvars.CAMERA.width = constants.CAMERA_WIDTH
            globalvars.CAMERA.height = constants.CAMERA_HEIGHT
            globalvars.PREFERENCES.display_window = "fullscreen"

        # ------- display functions ------- #
        draw.draw_button_update_cursor(button_list)
        text.draw_text(surface_menu, "Display Settings", constants.FONT_MENU_TITLE,
                       (title_x, title_y), constants.COLOR_BLACK, center=True)
        # update display
        globalvars.SURFACE_MAIN.blit(surface_menu, menu_rect.topleft, menu_rect)
        draw.draw_menu_background(surface_menu, (menu_width, menu_height), *corner_positions)
        pygame.display.update()
