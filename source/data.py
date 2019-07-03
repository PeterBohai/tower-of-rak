
class StructTile:

    """A class which functions like a struct that tracks the data for each tile within a map.

    Attributes:
        block_path (arg, bool) : True if the tile is like a wall, which blocks any movement onto or through the tile.
        explored (bool): Indicates whether the player has encountered the tile before and is initialized to False.

    """

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False
        self.assignment = 0     # for bitmasking purposes

class StructPreferences:
    def __init__(self):
        self.sfx_volume_val = 0.5
        self.music_volume_val = 0.15
        self.master_volume_vol = 0.5
