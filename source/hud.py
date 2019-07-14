import pygame
from source import constants
from source import text
from source import globalvars


def draw_player_health(surface, tup_coords, percentage):

    if percentage < 0:
        percentage = 0

    pos_x, pos_y = tup_coords

    BAR_WIDTH = 200
    BAR_HEIGHT = 24

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


    back_surface.blit(healthy_surface, (0,0))
    # pygame.draw.rect(back_surface, color, healthy_rect)
    surface.blit(back_surface, tup_coords)
    pygame.draw.rect(surface, constants.COLOR_WHITE, outline_rect, 2)
    health_text = "hp:  {}/{}".format(globalvars.PLAYER.creature.current_hp, globalvars.PLAYER.creature.maxHp)
    text_coords = (pos_x + int(BAR_WIDTH/2), pos_y + int(BAR_HEIGHT/2))
    text.draw_text(surface, health_text, constants.FONT_BEST, text_coords, constants.COLOR_WHITE, center=True)

