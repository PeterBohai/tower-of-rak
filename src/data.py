import copy
import random

import pygame

from src import globalvars


class StructTile:
    """A tile object class that tracks the data of a tile (wall/floor) within a map.

    Attributes
    ----------
    block_path : bool
        True if the tile is wall-like and False for floor tiles.
    explored : bool
        True if PLAYER has seen the tile (default is False).
    wall_assignment : int
        The bit-mask value for wall tiles.
    _floor_assignment : int
        The bit-mask value for floor tiles.
    floor_rand_index : int
        The index that assigns a random floor tile design accordingly.
    """

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False
        self.wall_assignment = 0
        self._floor_assignment = 0
        self.floor_rand_index = 0

    @property
    def floor_assignment(self):
        """int: Gets the floor bit-mask value and assigns a random floor design when set."""
        return self._floor_assignment

    @floor_assignment.setter
    def floor_assignment(self, value):
        # set random tile pattern for room tiles (not tunnel)
        if value in (0, 1, 2, 4, 8):
            self.floor_rand_index = random.randrange(
                len(globalvars.ASSETS.floor_explored_dict[value]))

        self._floor_assignment = value


class StructPreferences:
    """A preferences object that tracks general game settings like volume, display, or key bindings

    Attributes
    ----------
    sfx_volume_val : float
    music_volume_val : float
    master_volume_vol : float
    default_keybindings : dict
    keybindings : dict
    default_display_window : str
    display_window: str
    """
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
                                    }
        # user changes this
        self.keybindings = copy.deepcopy(self.default_keybindings)

        self.default_display_window = "default"
        self.display_window = self.default_display_window

