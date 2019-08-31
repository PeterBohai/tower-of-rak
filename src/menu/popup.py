import pygame

from src import constants, globalvars, text


def popup_menu(msg):
    """A simple popup menu that displays a message.

    Returns
    -------
    None

    """
    menu_close = False

    menu_text = msg
    font = constants.FONT_BEST_20

    text_height = text.get_text_height(font)
    text_width = text.get_text_width(font, menu_text)

    menu_x = (constants.CAMERA_WIDTH/2) - (text_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (text_height/2)

    start_time = pygame.time.get_ticks()

    while not menu_close:
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= 1300:
            break

        event_list = pygame.event.get()

        text.draw_text(globalvars.SURFACE_MAIN, menu_text, font,
                       (menu_x, menu_y), constants.COLOR_WHITE, constants.COLOR_GAME_BG)

        for event in event_list:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()
