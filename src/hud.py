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
    bar_height = 20
    bg_color = constants.COLOR_DARK_GREY
    health_text = f"hp:  {globalvars.PLAYER.creature.current_hp}/{globalvars.PLAYER.creature.maxHp}"
    text_coords = (int(bar_width / 2), int(bar_height / 2))

    if percentage > 0.6:
        health_color = constants.COLOR_HP_GREEN
    elif percentage > 0.3:
        health_color = constants.COLOR_HP_YELLOW
    else:
        health_color = constants.COLOR_HP_RED

    # initiate outline surface, health surface and back surface
    outline_rect = pygame.Rect(0, 0, bar_width, bar_height)

    healthy_width = percentage * bar_width
    healthy_surface = pygame.Surface((healthy_width, bar_height))
    healthy_surface.fill(health_color)

    back_surface = pygame.Surface((bar_width, bar_height))
    back_surface.fill(bg_color)

    # draw the health, outline, and text on to back_surface
    back_surface.blit(healthy_surface, (0, 0))
    pygame.draw.rect(back_surface, constants.COLOR_WHITE, outline_rect, 1)
    text.draw_text(back_surface, health_text, constants.FONT_BEST, text_coords, pygame.Color('black'), center=True)

    surface.blit(back_surface, coords)


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

