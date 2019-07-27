
#
#   _______                              __   _____       _
#  |__   __|                            / _| |  __ \     | |
#     | | _____      _____ _ __    ___ | |_  | |__) |__ _| | __
#     | |/ _ \ \ /\ / / _ \ '__|  / _ \|  _| |  _  // _` | |/ /
#     | | (_) \ V  V /  __/ |    | (_) | |   | | \ \ (_| |   <
#     |_|\___/ \_/\_/ \___|_|     \___/|_|   |_|  \_\__,_|_|\_\
#
#

# Local project imports
import pygame
from source.menu import mainmenu

if __name__ == '__main__':
    mainmenu.menu_main()
    icon = pygame.image.load("data/graphics/Rak.png")
    pygame.display.set_icon(icon)
    