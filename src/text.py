import pygame


def draw_text(display_surface, text, font, coords, text_color, back_color=None, center=False):
    """Displays the `text` to the desired `display_surface`

    Parameters
    ----------
    display_surface : pygame Surface obj
        The surface to display the text on.
    text : str
        The text that will be displayed.
    font : pygame Font obj
        The font to display the text in.
    coords : tuple
        The (x, y) pixel coordinates to position the text to.
    text_color : tuple
        Color of the text itself.
    back_color : tuple, optional
        Color of the text background.
    center : bool, optional
        True if `coords` center aligns the text instead of from the topleft (False by default).

    Returns
    -------
    None
    """
    if back_color is not None:
        text_surf = font.render(text, False, text_color, back_color)
    else:
        text_surf = font.render(text, False, text_color)

    text_rect = text_surf.get_rect()

    if center:
        text_rect.center = coords
    else:
        text_rect.topleft = coords

    display_surface.blit(text_surf, text_rect)


def draw_fading_text(display_surface, text, font, coords, text_color, alpha_val, speed=2,
                     center=False):
    """Displays text that fades to transparency

    Parameters
    ----------
    display_surface : pygame Surface obj
        The surface to display the text on.
    text : str
        The text that will be displayed.
    font : pygame Font obj
        The font to display the text in.
    coords : tuple
        The (x, y) pixel coordinates to position the text to.
    text_color : tuple
        Color of the text itself.
    alpha_val : int
        The alpha value to display the text in.
    speed : int, optional
        The speed of decreasing the alpha value and thus, the speed of the fade.
        The higher the speed, the faster the fade.
    center : bool, optional
        True if `coords` center aligns the text instead of from the topleft (False by default).

    Returns
    -------
    int
        The new alpha value (needed to modify the actual alpha variable that needs to be changed)
    """
    orig_surface = font.render(text, True, text_color)
    txt_surface = orig_surface.copy()
    alpha_surface = pygame.Surface(txt_surface.get_size(), pygame.SRCALPHA)

    # change alpha value
    alpha_val = max(alpha_val - speed, 0)

    # Fill alpha_surf with this color to set its alpha value.
    alpha_surface.fill((255, 255, 255, alpha_val))
    txt_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # set text alignment position
    text_rect = txt_surface.get_rect()
    if center:
        text_rect.center = coords
    else:
        text_rect.topleft = coords

    display_surface.blit(txt_surface, text_rect)
    return alpha_val


def get_text_height(font):
    """Provides the height of a text font.

    Parameters
    ----------
    font : pygame Font obj
        The font of the text.

    Returns
    -------
    int
        The height of the text font in pixels.
    """
    font_object = font.render('A', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height


def get_text_width(font, text):
    """Provides the total width of a line of text.

    Parameters
    ----------
    font : pygame Font obj
        The font of the text.
    text : str
        The line of text.

    Returns
    -------
    int
        The width of the text in pixels.
    """
    font_object = font.render(text, False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.width
