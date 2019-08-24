import pygame
import numpy

from source import constants, globalvars, text


class GuiButton:

    def __init__(self, surface, text, tup_coords_center, tup_size,
                 color_button_hovered=constants.COLOR_BLUE2,
                 color_button_default=constants.COLOR_BLUE1_LIGHTER,
                 color_text_hovered=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_BLACK):

        self.surface = surface
        self.text = text
        self.coords_center = tup_coords_center
        self.size = tup_size

        self.color_button_hovered = color_button_hovered
        self.color_button_default = color_button_default
        self.color_text_hovered = color_text_hovered
        self.color_text_default = color_text_default

        self.color_button_current = color_button_default
        self.color_text_current = color_text_default

        self.button_rect = pygame.Rect((0, 0), self.size)
        self.button_rect.center = self.coords_center
        self.mouse_hover = False
        self.num_played_rollover = 0

    def update(self, player_input):

        button_clicked = False
        mouse_clicked = False

        events_list, mouse_input = player_input
        mouse_x, mouse_y = mouse_input

        for event in events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        mouse_hovered = (self.button_rect.left <= mouse_x <= self.button_rect.right and
                         self.button_rect.top <= mouse_y <= self.button_rect.bottom)

        if mouse_hovered:
            self.color_button_current = self.color_button_hovered
            self.color_text_current = self.color_text_hovered
            self.mouse_hover = True
            if self.num_played_rollover == 0:
                globalvars.ASSETS.sfx_rollover.play()
                self.num_played_rollover = 1

        else:
            self.color_button_current = self.color_button_default
            self.color_text_current = self.color_text_default
            self.mouse_hover = False
            self.num_played_rollover = 0
            # fadeout to try and prevent "crackling" at end of audio (if abruptly ended)
            globalvars.ASSETS.sfx_rollover.fadeout(60)


        if mouse_hovered and mouse_clicked:
            globalvars.ASSETS.sfx_click1.play()
            button_clicked = True

        return button_clicked

    def draw(self):
        surface_button = pygame.Surface(self.size)
        surface_button.fill(self.color_button_current)

        topL = (0, 0)
        topR = numpy.subtract(self.size, (32, self.size[1]))
        num_tiles_width = int(self.size[0] / 32) - 2

        if not self.mouse_hover and self.size != (16, 16):
            surface_button.blit(globalvars.ASSETS.S_SIDE_L_BUTTON_BLUE, topL)
            surface_button.blit(globalvars.ASSETS.S_SIDE_R_BUTTON_BLUE, topR)
            for w in range(1, num_tiles_width + 1):
                surface_button.blit(globalvars.ASSETS.S_MID_BUTTON_BLUE, tuple(numpy.add(topL, (32*w, 0))))

        elif self.mouse_hover and self.size != (16,16):
            surface_button.blit(globalvars.ASSETS.S_SIDE_L_BUTTON_BLUE_HOVER, topL)
            surface_button.blit(globalvars.ASSETS.S_SIDE_R_BUTTON_BLUE_HOVER, topR)
            for w in range(1, num_tiles_width + 1):
                surface_button.blit(globalvars.ASSETS.S_MID_BUTTON_BLUE_HOVER, tuple(numpy.add(topL, (32 * w, 0))))

        self.surface.blit(surface_button, self.button_rect.topleft)

        # pygame.draw.rect(self.surface, self.color_button_current, self.button_rect)

        text.draw_text(self.surface, self.text, constants.FONT_BEST, self.coords_center,
                       self.color_text_current, self.color_button_current, center=True)



class GuiSlider:
    def __init__(self,
                 surface,
                 tup_coords_center,
                 tup_size,
                 slider_value,
                 color_slider_bg=constants.COLOR_GREY,
                 color_slider_fg=constants.COLOR_WHITE):

        self.surface = surface
        self.coords_center = tup_coords_center
        self.size = tup_size
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

    def update(self, player_input):

        events_list, mouse_input = player_input
        mouse_x, mouse_y = mouse_input

        button_y = self.grab_button.centery - int(self.grab_button_height/2)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        mouse_over_slider = (self.slider_rect.left <= mouse_x <= self.slider_rect.right and
                             button_y <= mouse_y <= button_y + self.grab_button_height)

        if mouse_pressed and mouse_over_slider:
            # update slider value
            self.slider_value = (mouse_x - self.slider_rect.left) / self.slider_rect.width

            # update foreground slider width
            self.fg_rect.width = self.slider_rect.width * self.slider_value

            # update grab center
            self.grab_button.center = (self.fg_rect.right, self.slider_rect.centery)

    def draw(self):

        # draw background slider rectangle
        pygame.draw.rect(self.surface, self.color_slider_bg, self.slider_rect)

        # draw foreground slider rectangle
        pygame.draw.rect(self.surface, self.color_slider_fg, self.fg_rect)

        # draw grab button rectangle
        # pygame.draw.rect(self.surface, constants.COLOR_WHITE, self.grab_button)

        self.surface.blit(globalvars.ASSETS.S_SLIDER_BUTTON, (self.grab_button.centerx - int(self.grab_button_width/2),
                                                   self.grab_button.centery - int(self.grab_button_height/2)))
