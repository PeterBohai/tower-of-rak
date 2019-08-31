import pygame

from src import constants, text, globalvars


def draw_player_health(surface, coords, percentage):
    """Displays the player's health onto the screen.

    Parameters
    ----------
    surface : pygame Surface obj
        The surface that the health bar will be drawn on.
    coords : tuple
        The pixel topleft-aligned coordinates of where the health bar will be drawn.
    percentage : float
        The percentage of total health remaining.

    Returns
    -------
    None

    """
    if percentage < 0:
        percentage = 0

    bar_width = 260
    bar_height = 26
    bg_color = (219, 219, 219, 180)
    health_text = f"hp {globalvars.PLAYER.creature.current_hp}/{globalvars.PLAYER.creature.max_hp}"
    text_coords = (int(bar_width / 2), int(bar_height / 2))

    if percentage > 0.6:
        health_color = (235, 27, 35)
    elif percentage > 0.3:
        health_color = (235, 27, 35)
    else:
        health_color = (235, 27, 35)

    # initiate outline surface, health surface and back surface
    outline_rect = pygame.Rect(0, 0, bar_width, bar_height)

    healthy_width = percentage * bar_width
    healthy_surface = pygame.Surface((healthy_width, bar_height))
    healthy_surface.fill(health_color)

    back_surface = pygame.Surface((bar_width, bar_height))
    back_surface.fill(bg_color)

    # draw the health, outline, and text on to back_surface
    back_surface.blit(healthy_surface, (0, 0))
    pygame.draw.rect(back_surface, constants.COLOR_BLACK, outline_rect, 2)
    text.draw_text(back_surface, health_text, constants.FONT_BEST, text_coords, (201, 214, 223), center=True)

    surface.blit(back_surface, coords)


def pfp(surface, coord):
    """Draws the player profile square onto the window ui.

    Parameters
    ----------
    surface : pygame Surface obj
        The surface to draw the pfp on (normally main surface).
    coord : tuple
        Appropriate coordinates (usually in px) to position the pfp relative to its topleft corner.

    Returns
    -------
    None

    """

    pfp_img = globalvars.ASSETS.S_PLAYER_PFP
    surface.blit(pfp_img, coord)


def level_sign(surface, coord):
    """Draws the player level onto the window ui.

    Parameters
    ----------
    surface : pygame Surface obj
        The surface to draw the level indicator on (normally main surface).
    coord : tuple
        Appropriate coordinates (usually in px) to position the indicator relative to its topleft corner.

    Returns
    -------
    None

    """
    level_img = globalvars.ASSETS.S_PLAYER_LVL
    level_txt = f"LV {globalvars.PLAYER.level}"

    if globalvars.PLAYER.level != constants.PLAYER_MAX_LV:
        txt_color = (109, 227, 176)
    else:
        txt_color = constants.COLOR_WHITE

    sign_surface = pygame.Surface(level_img.get_size())

    # draw the sign
    sign_surface.blit(level_img, (0, 0))
    text.draw_text(sign_surface, level_txt, constants.FONT_BEST, (34, 15), txt_color, center=True)

    surface.blit(sign_surface, coord)


def update_pfp(surface, player_input):
    """Updates the pfp area whenever the cursor clicks or hovers over it.

    Parameters
    ----------
    surface : pygame Surface obj
        The pfp surface used.
    player_input : tuple
        Contains the events list and mouse position

    Returns
    -------
    bool
        True if the pfp was clicked, False if not.

    """
    surface_rect = surface.get_rect()
    button_clicked = False
    mouse_clicked = False
    events_list, mouse_pos = player_input

    mouse_x, mouse_y = mouse_pos
    for event in events_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True

    mouse_hover = (surface_rect.left <= mouse_x <= surface_rect.right and
                   surface_rect.top <= mouse_y <= surface_rect.bottom)

    if mouse_hover:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

        if not globalvars.GAME.hover_sound_played:
            globalvars.ASSETS.sfx_rollover.play()
            globalvars.GAME.hover_sound_played = True

        if mouse_clicked:
            globalvars.ASSETS.sfx_click1.play()
            button_clicked = True

    else:
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        globalvars.ASSETS.sfx_rollover.fadeout(60)
        globalvars.GAME.hover_sound_played = False

    return button_clicked


def draw_fps():
    """Draws the current fps onto the game screen window.

    Returns
    -------
    int
        The x-coordinate of the topleft corner of the fps message

    """
    fps_text = f"fps: {int(globalvars.CLOCK.get_fps())}"
    pos_x = constants.CAMERA_WIDTH - text.get_text_width(constants.FONT_BEST, fps_text) - 5
    pos_y = 0

    text.draw_text(globalvars.SURFACE_MAIN, fps_text,
                   constants.FONT_BEST, (pos_x, pos_y), constants.COLOR_WHITE)

    return pos_x


def draw_messages():
    """Draws the message console to the game screen window.

    Displays a number of messages from GAME.message_history in sequence. The order of messages starts from
    the most recent at the bottom and older at the top.

    Returns
    -------
    None

    """
    if len(globalvars.GAME.message_history) <= constants.NUM_MESSAGES:
        globalvars.GAME.message_history = globalvars.GAME.message_history
    else:
        del globalvars.GAME.message_history[0]

    text_height = text.get_text_height(constants.FONT_BEST)
    text_x = 10
    start_y = constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height) - 16

    for i, (message, color) in enumerate(globalvars.GAME.message_history):
        text.draw_text(globalvars.SURFACE_MAIN, message, constants.FONT_BEST,
                       (text_x, start_y + (i * text_height)), color, constants.COLOR_GAME_BG)


def draw_floor_title(text_color=pygame.Color('aquamarine1'), font=constants.FONT_BEST_20, change_alpha=True):
    """Displays the fading floor title text when entering game from the main menu or entering a floor.

    Parameters
    ----------
    text_color : tuple, optional
        The color of the text.
    font : pygame Font obj, optional
        The font of the text.
    change_alpha : bool, optional
        True if the alpha value needs to be decremented.

    Returns
    -------
    None

    """
    text_coords = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2 - constants.CELL_HEIGHT - 5)
    floor_num = globalvars.GAME.cur_floor

    alpha_val = globalvars.GAME.floor_transition_alpha
    floor_text = f"Floor - {floor_num}"

    # dont need to change alpha value here since the main game loop does it
    if change_alpha:
        globalvars.GAME.floor_transition_alpha = text.draw_fading_text(globalvars.SURFACE_MAIN, floor_text, font,
                                                                       text_coords, text_color, alpha_val, center=True)
    else:
        text.draw_fading_text(globalvars.SURFACE_MAIN, floor_text, font,
                              text_coords, text_color, alpha_val, speed=1, center=True)

