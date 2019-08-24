import pygame

from source import constants, text, globalvars


def draw_player_health(surface, tup_coords, percentage):

    if percentage < 0:
        percentage = 0

    pos_x, pos_y = tup_coords

    BAR_WIDTH = 260
    BAR_HEIGHT = 20

    if percentage > 0.6:
        color = constants.COLOR_HP_GREEN
    elif percentage > 0.3:
        color = constants.COLOR_HP_YELLOW
    else:
        color = constants.COLOR_HP_RED

    healthy_width = percentage * BAR_WIDTH
    # healthy_rect = pygame.Rect(0, 0, healthy_width, BAR_HEIGHT)

    healthy_surface = pygame.Surface((healthy_width, BAR_HEIGHT))
    healthy_surface.fill(color)

    back_surface = pygame.Surface((BAR_WIDTH, BAR_HEIGHT))
    back_surface.fill(constants.COLOR_DARK_GREY)

    outline_rect = pygame.Rect(pos_x, pos_y, BAR_WIDTH, BAR_HEIGHT)

    back_surface.blit(healthy_surface, (0, 0))
    # pygame.draw.rect(back_surface, color, healthy_rect)
    surface.blit(back_surface, tup_coords)
    pygame.draw.rect(surface, constants.COLOR_WHITE, outline_rect, 1)
    health_text = "hp:  {}/{}".format(globalvars.PLAYER.creature.current_hp, globalvars.PLAYER.creature.maxHp)
    text_coords = (pos_x + int(BAR_WIDTH/2), pos_y + int(BAR_HEIGHT/2))
    text.draw_text(surface, health_text, constants.FONT_BEST, text_coords, pygame.Color('black'), center=True)


def draw_fps():
    """Draws the debug console onto the game screen window.

    Draws debug message text to the upper left corner of the screen.
    Displays only the current FPS for now.

    Returns:
        pos_x (int): x-coordinate of debug message

    """

    fps_text = "fps: " + str(int(globalvars.CLOCK.get_fps()))
    pos_x = constants.CAMERA_WIDTH - text.helper_text_width(constants.FONT_BEST, fps_text) - 5
    pos_y = 0

    text.draw_text(globalvars.SURFACE_MAIN, fps_text,
                   constants.FONT_BEST, (pos_x, pos_y), constants.COLOR_WHITE)

    return pos_x


def draw_messages():
    """Draws the message console to the game screen window.

    Displays a max number of messages from the game's list of messages stored in globalvars.GAME.message_history
    in sequence to the lower left corner of the screen. The order of messages starts at the bottom with the most
    recent message.

    Returns:
        None

    """
    if len(globalvars.GAME.message_history) <= constants.NUM_MESSAGES:
        globalvars.GAME.message_history = globalvars.GAME.message_history   # the last 4 messages in the list
    else:
        del globalvars.GAME.message_history[0]
        # globalvars.GAME.message_history = globalvars.GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = text.helper_text_height(constants.FONT_BEST)
    text_x = 10
    start_y = constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height) - 16

    for i, (message, color) in enumerate(globalvars.GAME.message_history):

        text.draw_text(globalvars.SURFACE_MAIN, message, constants.FONT_BEST,
                       (text_x, start_y + (i * text_height)), color, constants.COLOR_GAME_BG)


def draw_floor_title(text_color=pygame.Color('aquamarine1'), font=constants.FONT_BEST_20, change_alpha=True):
    """

    Parameters
    ----------
    text_color
    font
    change_alpha

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

