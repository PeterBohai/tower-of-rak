import pygame

# ================================================================= #
#                         -----  Text  -----                        #
# ================================================================= #


def draw_text(display_surface, text, font, t_coords, text_color, back_color=None, center=False):
    """ Displays text to the specified Surface.

    Args:
        display_surface (pygame.Surface):
        text (str):
        font (pygame.font.Font):
        t_coords (tuple):
        text_color(tuple, Color):
        back_color (tuple):
        center (bool):

    Returns:
        None

    """

    text_surf, text_rect = helper_text_objects(text, font, text_color, back_color)

    if center:
        text_rect.center = t_coords
    else:
        text_rect.topleft = t_coords

    display_surface.blit(text_surf, text_rect)


def draw_fading_text(display_surface, text, font, t_coords, text_color, alpha_var, speed=2, center=False):
    """ Displays text that fades away (to transparency)

    Args:
        display_surface (pygame.Surface):
        text (str):
        font (pygame.font.Font):
        t_coords (tuple):
        text_color (tuple, Color):
        alpha_var (int):
        speed (int):
        center (bool):

    Returns:
        alpha_var (int): The new alpha value (so that it can modify the actual alpha variable that needs to be changed

    """

    orig_surface = font.render(text, True, text_color)
    txt_surface = orig_surface.copy()
    alpha_surface = pygame.Surface(txt_surface.get_size(), pygame.SRCALPHA)

    # change alpha value (higher speed num = faster fade)
    alpha_var = max(alpha_var - speed, 0)

    # Fill alpha_surf with this color to set its alpha value.
    alpha_surface.fill((255, 255, 255, alpha_var))
    txt_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # set text alignment position
    text_rect = txt_surface.get_rect()
    if center:
        text_rect.center = t_coords
    else:
        text_rect.topleft = t_coords

    display_surface.blit(txt_surface, text_rect)
    return alpha_var


def helper_text_objects(incoming_text, font, incoming_color, incoming_bg):

    if incoming_bg:
        text_surface = font.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = font.render(incoming_text, False, incoming_color)  # constants.FONT_BEST

    return text_surface, text_surface.get_rect()


def helper_text_height(font):
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height       # return font's height in pixels


def helper_text_width(font, text):
    font_object = font.render(text, False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.width
