
# ================================================================= #
#                         -----  Text  -----                        #
# ================================================================= #


def draw_text(display_surface, text_to_display, font, t_coords, text_color, back_color=None, center=False):
    """ Displays text to the specified Surface.

    Args:
        display_surface (pygame.Surface):
        text_to_display (str):
        font (pygame.font.Font):
        t_coords (tuple):
        text_color(tuple):
        back_color (tuple):
        center (bool):

    Returns:
        None

    """

    text_surf, text_rect = helper_text_objects(text_to_display, font, text_color, back_color)

    if not center:
        text_rect.topleft = t_coords
    else:
        text_rect.center = t_coords

    display_surface.blit(text_surf, text_rect)


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
