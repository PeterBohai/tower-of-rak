import pygame, copy, random
from source import globalvars

class StructTile:

    """A class which functions like a struct that tracks the data for each tile within a map.

    Attributes:
        block_path (arg, bool) : True if the tile is like a wall, which blocks any movement onto or through the tile.
        explored (bool): Indicates whether the player has encountered the tile before and is initialized to False.

    """

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False
        self.wall_assignment = 0     # for wall bitmasking purposes
        self._floor_assignment = 0    # for floor bitmasking purposes
        self.floor_rand_index = 0  # for floor variation

    @property
    def floor_assignment(self):
        return self._floor_assignment

    @floor_assignment.setter
    def floor_assignment(self, value):

        # set random tile pattern for room tiles (not tunnel) when setting floor bitmask
        if value in (0, 1, 2, 4, 8):
            self.floor_rand_index = random.randrange(len(globalvars.ASSETS.floor_explored_dict[value]))

        self._floor_assignment = value


class StructPreferences:
    def __init__(self):
        self.sfx_volume_val = 0.5
        self.music_volume_val = 0.15
        self.master_volume_vol = 0.5

        # will never be changed
        self.default_keybindings = {"left": ("←", pygame.K_LEFT),
                                    "right": ("→", pygame.K_RIGHT),
                                    "up": ("↑", pygame.K_UP),
                                    "down": ("↓", pygame.K_DOWN),
                                    "stay": ("Spc", pygame.K_SPACE),
                                    "grab": ("G", pygame.K_g),
                                    "drop": ("D", pygame.K_d),
                                    "inventory": ("I", pygame.K_i),
                                    "next": (">", pygame.K_PERIOD, pygame.K_LSHIFT),
                                    "back": ("Esc", pygame.K_ESCAPE),
                                    "pause": ("P", pygame.K_p)
                                    }

        # user changes this
        self.keybindings = copy.deepcopy(self.default_keybindings)

        self.default_display_window = "default"
        self.display_window = self.default_display_window

