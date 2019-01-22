
# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, text



def menu_pause():
    """Menu that pauses the game and displays a simple pause message.

    """

    menu_close = False

    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    pause_menu_text = "PAUSED"
    pause_menu_font = constants.FONT_BEST

    pause_text_height = text.helper_text_height(pause_menu_font)
    pause_text_width = text.helper_text_width(pause_menu_font, pause_menu_text)

    pause_menu_x = (window_width/2) - (pause_text_width/2)
    pause_menu_y = (window_height/2) - (pause_text_height/2)

    while not menu_close:
        event_list = pygame.event.get()

        text.draw_text(globalvars.SURFACE_MAIN, pause_menu_text, pause_menu_font, (pause_menu_x, pause_menu_y),
                  constants.COLOR_WHITE, constants.COLOR_BLACK)

        for event in event_list:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    menu_close = True       # pressing pause button again means break out and unpause game

        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()
