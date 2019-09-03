import pygame
import numpy

from src import constants, globalvars, text


class GuiButton:
    """A button object class that creates simple rectangular buttons.

    Attributes
    ----------
    surface : pygame Surface obj
        The surface that the button will be drawn on.
    text : str
        The text that is displayed onto the button.
    coords_center : tuple
        The center coordinate position (in pixels) of the button.
    size : tuple
        The (width, height) of the button.
    color_button_hovered : tuple, optional
        The background color of the button when the cursor is hovered over it.
    color_button_default : tuple, optional
        The background color of the button when it is not in focus.
    color_text_hovered : tuple, optional
        The text color of the button when the cursor is hovered over it.
    color_text_default : tuple, optional
        The text color of the button when the button is not in focus.
    color_button_current : tuple
        The current background color of the button.
    color_text_current : tuple
        The current text color of the button.
    button_rect : pygame Rect obj
        The Rect object that represents the button.
    mouse_hover : bool
        True if the cursor is hovered over the button.
    hover_sfx_played : bool
        True if the hover sfx played once already.

    """
    def __init__(self, surface, text, coords_center, size,
                 color_button_hovered=constants.COLOR_BLUE2,
                 color_button_default=constants.COLOR_BLUE1_LIGHTER,
                 color_text_hovered=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_BLACK):

        self.surface = surface
        self.text = text
        self.coords_center = coords_center
        self.size = size
        self.color_button_hovered = color_button_hovered
        self.color_button_default = color_button_default
        self.color_text_hovered = color_text_hovered
        self.color_text_default = color_text_default

        self.color_button_current = color_button_default
        self.color_text_current = color_text_default

        self.button_rect = pygame.Rect((0, 0), self.size)
        self.button_rect.center = self.coords_center
        self.mouse_hover = False
        self.hover_sfx_played = False

    def update(self, player_input):
        """Updates the button color and all other actions when the button is hovered over or clicked on.

        Parameters
        ----------
        player_input : tuple
            Contains the events list and mouse position

        Returns
        -------
        bool
            True if the button was clicked, False if not.
        """
        button_clicked = False
        mouse_clicked = False

        events_list, mouse_pos = player_input
        mouse_x, mouse_y = mouse_pos
        for event in events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        self.mouse_hover = (self.button_rect.left <= mouse_x <= self.button_rect.right and
                            self.button_rect.top <= mouse_y <= self.button_rect.bottom)

        if self.mouse_hover:
            self.color_button_current = self.color_button_hovered
            self.color_text_current = self.color_text_hovered

            if not self.hover_sfx_played:
                globalvars.ASSETS.sfx_rollover.play()
                self.hover_sfx_played = True

            if mouse_clicked:
                globalvars.ASSETS.sfx_click1.play()
                button_clicked = True

        else:
            # fadeout prevents "crackling" at end of audio (caused by abruptly ending)
            globalvars.ASSETS.sfx_rollover.fadeout(60)
            self.color_button_current = self.color_button_default
            self.color_text_current = self.color_text_default
            self.hover_sfx_played = False

        return button_clicked

    def draw(self):
        """Draws the button onto the specified `surface`.

        Returns
        -------
        None

        """
        button_surf = pygame.Surface(self.size)

        # placement for button assets (all blit from their top left corner)
        left_coord = (0, 0)
        right_coord = (self.size[0] - 32, 0)
        num_middle_tiles = int(self.size[0] / 32) - 2

        left_tile = globalvars.ASSETS.S_SIDE_L_BUTTON_BLUE
        right_tile = globalvars.ASSETS.S_SIDE_R_BUTTON_BLUE
        mid_tile = globalvars.ASSETS.S_MID_BUTTON_BLUE

        button_surf.fill(self.color_button_current)

        if self.mouse_hover:
            left_tile = globalvars.ASSETS.S_SIDE_L_BUTTON_BLUE_HOVER
            right_tile = globalvars.ASSETS.S_SIDE_R_BUTTON_BLUE_HOVER
            mid_tile = globalvars.ASSETS.S_MID_BUTTON_BLUE_HOVER

        # blit left and right corner tiles
        button_surf.blit(left_tile, left_coord)
        button_surf.blit(right_tile, right_coord)
        # blit middle tiles
        for w in range(1, num_middle_tiles + 1):
            button_surf.blit(mid_tile, tuple(numpy.add(left_coord, (32 * w, 0))))

        self.surface.blit(button_surf, self.button_rect.topleft)
        text.draw_text(self.surface, self.text, constants.FONT_BEST, self.coords_center,
                       self.color_text_current, self.color_button_current, center=True)


class GuiSlider:
    """A slider object class that creates simple horizontal slider.

        Attributes
        ----------
        surface : pygame Surface obj
            The surface that the button will be drawn on.
        coords_center : tuple
            The center coordinate position (in pixels) of the button.
        size : tuple
            The (width, height) of the button.
        color_slider_bg : tuple, optional
            The background color of the slider strip (to the right of slider button).
        color_slider_fg : tuple, optional
            The foreground color of the slider strip (to the left of slider button).
        slider_rect : pygame Rect obj
            The Rect object that represents the background slider strip.
        fg_rect : pygame Rect obj
            The Rect object that represents the moving foreground slider strip.
        grab_button : pygame Rect obj
            The Rect object that represents the slider button.

        """
    def __init__(self,
                 surface,
                 coords_center,
                 size,
                 slider_value,
                 color_slider_bg=constants.COLOR_GREY,
                 color_slider_fg=constants.COLOR_WHITE):

        self.surface = surface
        self.coords_center = coords_center
        self.size = size
        self.slider_value = slider_value

        self.color_slider_bg = color_slider_bg
        self.color_slider_fg = color_slider_fg

        self.slider_rect = pygame.Rect((0, 0), self.size)
        self.slider_rect.center = self.coords_center
        self.fg_rect = pygame.Rect((0, 0), (self.slider_rect.width * self.slider_value, self.slider_rect.height))
        self.fg_rect.topleft = self.slider_rect.topleft

        self.grab_button = pygame.Rect((0, 0), (20, self.slider_rect.height + 6))
        self.grab_button.center = (self.fg_rect.right, self.slider_rect.centery)
        self.grab_button_width, self.grab_button_height = globalvars.ASSETS.slider_button_size

    @property
    def grab_button_x(self):
        return self.grab_button.centerx - int(self.grab_button_width / 2)

    @property
    def grab_button_y(self):
        return self.grab_button.centery - int(self.grab_button_height / 2)

    def update(self, player_input):
        """Moves the slider when cursor is dragging over it, and updates its stored value.

        Parameters
        ----------
        player_input : tuple
            Contains the events list and mouse position

        Returns
        -------
        None

        """
        events_list, mouse_pos = player_input
        mouse_x, mouse_y = mouse_pos
        mouse_pressed = pygame.mouse.get_pressed()[0]

        mouse_over_slider = (self.slider_rect.left <= mouse_x <= self.slider_rect.right and
                             self.grab_button_y <= mouse_y <= self.grab_button_y + self.grab_button_height)

        if mouse_pressed and mouse_over_slider:
            self.slider_value = (mouse_x - self.slider_rect.left) / self.slider_rect.width
            self.fg_rect.width = self.slider_rect.width * self.slider_value
            self.grab_button.center = (self.fg_rect.right, self.slider_rect.centery)

    def draw(self):
        """Draws the slider and its button onto the specified `surface`.

        Returns
        -------
        None

        """
        pygame.draw.rect(self.surface, self.color_slider_bg, self.slider_rect)
        pygame.draw.rect(self.surface, self.color_slider_fg, self.fg_rect)
        self.surface.blit(globalvars.ASSETS.S_SLIDER_BUTTON, (self.grab_button_x, self.grab_button_y))


def hovered_clickable_element(mouse_hovered, mouse_clicked):
    """Give visual and audio feedback when mouse is hovering over or clicked a clickable element.

    Parameters
    ----------
    mouse_hovered : bool
        True if the mouse position is within the boundaries of the element.
    mouse_clicked : bool
        True if the mouse clicked (left mouse button down and up).

    Returns
    -------
    bool
        True if the mouse clicked within the element

    """
    element_clicked = False
    if mouse_hovered:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

        if not globalvars.GAME.hover_sound_played:
            globalvars.ASSETS.sfx_rollover.play()
            globalvars.GAME.hover_sound_played = True

        if mouse_clicked:
            globalvars.ASSETS.sfx_click1.play()
            print("played click sound")
            element_clicked = True

    else:
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        globalvars.ASSETS.sfx_rollover.fadeout(60)
        globalvars.GAME.hover_sound_played = False

    return element_clicked
