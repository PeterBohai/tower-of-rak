# Standard library imports
import math

# Third party imports
import tcod

# Local project imports
from source import constants, globalvars, data
from source.generators import itemgen, creaturegen, playergen, specialgen



# ================================================================= #
#                         -----  Map  -----                         #
#                          --- SECTION ---                          #
# ================================================================= #

class ObjRoom:
    """Rectangular room objects on the map that have various useful properties.

    Contains the property of returning the coordinate that is closest to the room object's "center".
    Also have the property of returning a boolean to determine whether it intersects with another room object

    Attributes:
        tup_coords (arg, tuple): The x and y coordinates of the upper-left corner of the rectangular room.
        tup_size (arg, tuple): Integer values of the room's width and height (in that order).
        x1 (int): The x-coordinate specified by tup_coords (upper-left coords) in the initialization.
        y1 (int): The y-coordinate specified by tup_coords (upper-left coords) in the initialization.
        width (int): The width of the room specified by the first integer in tup_size in the initialization.
        height (int): The height of the room specified by the first integer in tup_size in the initialization.
        x2 (int): The right side x-coordinate of the room.
        y2 (int): The bottom y-coordinate of the room.

    """

    def __init__(self, tup_coords, tup_size):
        self.x1, self.y1 = tup_coords
        self.width, self.height = tup_size

        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.center_x = None
        self.center_y = None

    @property
    def center(self):
        """A property method that takes x and y coordinates and calculates the center coordinate of the room.

        Returns:
            center_x (int): The x coordinate of the center of the room.
            center_y (int): The y coordinate of the center of the room.

        """
        self.center_x = int((self.x1 + self.x2)/2)
        self.center_y = int((self.y1 + self.y2)/2)

        return self.center_x, self.center_y

    def intersect(self, other):
        """Determines whether a room object intersects with another room object.

        Args:
            other (ObjRoom): Another room object created by ObjRoom.

        Returns:
            intersects_other (bool):  True if the room object intersects with the "other" room object.

        """

        intersects_other = (self.x1 <= other.x2 and self.x2 >= other.x1 and
                            self.y1 <= other.y2 and self.y2 >= other.y1)

        return intersects_other


def map_create():
    """Creates the default map.

    Currently, only walls bordering the window are created, with 2 walls placed at (10,10) and (10, 15).
    This is for testing purposes and will change into a more procedurally generated map in the future.
    Calls map_make_fov() on new_map to create the fov (field of view) map.

    Returns:
        new_map (2d array) : An array of StructTile objects.
        list_of_rooms (list): A list containing all valid ObjRoom objects on the displayed map.

    """

    # initialize empty map with wall tiles (True arg for StructTile)
    new_map = [[data.StructTile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    # list of rooms containing room objects
    list_of_rooms = []

    # generate new room
    for i in range(constants.MAP_MAX_NUM_ROOMS):

        # randomize room dimensions and position (upper-left corner) coordinate
        room_width = tcod.random_get_int(0, constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        room_height = tcod.random_get_int(0, constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)

        room_x = tcod.random_get_int(0, 2, constants.MAP_WIDTH - 2 - room_width)
        room_y = tcod.random_get_int(0, 2, constants.MAP_HEIGHT - 2 - room_height)

        # create the room
        new_room = ObjRoom((room_x, room_y), (room_width, room_height))
        failed = False

        # check for interference
        for other_room in list_of_rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:

            # place the room onto the map
            map_create_room(new_map, new_room)

            # place the globalvars.PLAYER inside the center of the very first of room of this map
            if len(list_of_rooms) != 0:
                previous_room = list_of_rooms[-1]

                map_create_tunnels(new_map, new_room.center, previous_room.center)

            list_of_rooms.append(new_room)

    # load in created map and assign bitmasking
    assign_tiles(new_map)

    # create FOV_MAP
    map_make_fov(new_map)

    return new_map, list_of_rooms


def map_create_room(map_array, new_room):
    """Creates a room in the map.

    Turns all the tiles of the specified room to floor tiles.

    Args:
        map_array (2d array): The map (array of tiles) to create/dig the room in.
        new_room (ObjRoom): The room object with coordinate attributes specifying the tiles to be turned to floor.

    """

    for x in range(new_room.x1, new_room.x2 + 1):
        for y in range(new_room.y1, new_room.y2 + 1):
            map_array[x][y].block_path = False


def map_place_items_creatures(room_list):
    """Randomly generates different items and creatures to random coordinates in each room on the map.

    Args:
        room_list (list): List of ObjRoom objects.

    """

    floor_num = globalvars.GAME.max_floor_reached
    is_top_floor = (floor_num == constants.MAP_MAX_NUM_FLOORS)
    first_floor = (len(globalvars.GAME.maps_prev) == 0)

    for i, room in enumerate(room_list):

        first_room = (i == 0)
        last_room = (room == room_list[-1])

        min_x = room.x1
        max_x = room.x2
        min_y = room.y1
        max_y = room.y2

        enemy_x = tcod.random_get_int(0, min_x, max_x)
        enemy_y = tcod.random_get_int(0, min_y, max_y)

        # generate PLAYER in the center of the first room
        if first_room:
            globalvars.PLAYER.x, globalvars.PLAYER.y = room.center
            creaturegen.gen_enemy((enemy_x, enemy_y))

        # only generate enemies in the rooms that the player doesnt start in
        if not first_room:
            creaturegen.gen_enemy((enemy_x, enemy_y))

        # only generate stairs leading down in the first room if the map is not the top level
        if first_room and not first_floor:
            specialgen.gen_stairs((globalvars.PLAYER.x, globalvars.PLAYER.y), up=False)

        # generate stairs leading up in the last room
        if last_room and not is_top_floor:
            specialgen.gen_stairs(room.center)

        # generate magic rock as item to obtain in order to win
        elif last_room and is_top_floor:
            specialgen.gen_magic_rock(room.center)
            specialgen.gen_portal((room.center_x, room.center_y - 1))

        item_x = globalvars.PLAYER.x
        item_y = globalvars.PLAYER.y

        # items are not allowed to span on top of player's spawn point
        while (item_x, item_y) == (globalvars.PLAYER.x, globalvars.PLAYER.y):
            item_x = tcod.random_get_int(0, min_x, max_x)
            item_y = tcod.random_get_int(0, min_y, max_y)

        itemgen.gen_item((item_x, item_y))



def map_create_tunnels(map_array, tup_center1, tup_center2):
    """Creates (one tile-width) a horizontal and a vertical tunnel connecting one room to another.

    Provides a 50% chance to create the horizontal tunnel first.

    Args:
        map_array (2d array): The map (array of tiles) to create/dig the horizontal tunnel in.
        tup_center1 (tuple): The center coordinate of a room (usually the room that was just created).
        tup_center2 (tuple): The center coordinate of another room (usually the previously created room).

    """

    x1, y1 = tup_center1
    x2, y2 = tup_center2

    # give a 50% chance that the tunnel will be created in the horizontal direction first
    order_of_tunnel_drawn = tcod.random_get_int(0, 0, 1)

    # If this horizontal tunnel is drawn first, y coord would be y1. Otherwise, y coord would be y2.
    if order_of_tunnel_drawn == 1:

        # create horizontal tunnel first
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map_array[x][y1].block_path = False

        # create vertical tunnel next
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map_array[x2][y].block_path = False

    else:

        # create vertical tunnel first
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map_array[x1][y].block_path = False

        # create horizontal tunnel next
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map_array[x][y2].block_path = False


def map_check_for_creatures(coords_x, coords_y, exclude_object=None):
    """Check if there is a creature object at the specified x, y coordinates.

    Args:
        coords_x (int): x coordinate of tile to be checked for creatures.
        coords_y (int): y coordinate of tile to be checked for creatures.
        exclude_object (ObjActor): Optional argument for an actor to be excluded from the check.

    Returns:
        target (ObjActor):

    """

    # if no creature on that tile, return None
    target = None

    if exclude_object:
        # check object list to find creature at that location that isn't excluded
        for obj in globalvars.GAME.current_objects:
            if (obj is not exclude_object and
                obj.x == coords_x and
                obj.y == coords_y and
                obj.creature):

                target = obj

            if target:
                return target

    else:
        # check object list to find any creature at that location (eg. confuse spell hurting themselves)
        for obj in globalvars.GAME.current_objects:
            if (obj.x == coords_x and
                obj.y == coords_y and
                obj.creature):
                target = obj

            if target:
                return target


def map_make_fov(incoming_map):
    """Creates a fov map based on a specified map.

    Generates the global tcod map object FOV_MAP.

    Args:
        incoming_map (2D array): A map that's usually created by map_create().

    Returns:
        None

    """
    globalvars.FOV_MAP = tcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    # for every cell, set the properties
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            tcod.map_set_properties(globalvars.FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
    """Calculates the fov based on the PLAYER's position on the map.

    Only calculates the fov when the global variable FOV_CALCULATE is True.

    Returns:
        None
    """

    if globalvars.FOV_CALCULATE:
        globalvars.FOV_CALCULATE = False   # prevent calculating fov every frame, if standing still
        tcod.map_compute_fov(globalvars.FOV_MAP, globalvars.PLAYER.x, globalvars.PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                             constants.FOV_ALG)


def map_object_at_coords(coords_x, coords_y):
    """Check if there is an object at the specified x, y coordinates.

    Args:
        coords_x (int): x coordinate of tile to be checked for creatures.
        coords_y (int): y coordinate of tile to be checked for creatures.

    Returns:
        object_options (List): List of all actor objects at specified coordinates.

    """

    object_options = [obj for obj in globalvars.GAME.current_objects if obj.x == coords_x and obj.y == coords_y]

    return object_options


def map_find_line(coords1, coords2):
    """Coverts two different (x, y) coordinates into a list of map tiles

    Args:
        coords1 (tuple): (x1, y1) The start coordinates for the line.
        coords2 (tuple): (x2, y2) The end coordinates for the line.

    Returns:
        coord_list (list): A list of map tile coordinates.
    """

    x1, y1 = coords1
    x2, y2 = coords2

    # line_iter returns an iterator of tuples
    coord_iter = tcod.line_iter(x1, y1, x2, y2)

    # list of coords in the line
    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1, y2)]

    # append each set of (x,y) coords that's in the line onto coord_list
    while True:
        calc_x, calc_y = next(coord_iter)
        coord_list.append((calc_x, calc_y))

        if calc_x == x2 and calc_y == y2:
            break

    return coord_list


def map_find_radius(coords, radius):
    """Converts a map coordinate to a list of all tiles in the area specified by the radius.

    Args:
        coords (tuple): X and y map coordinates of the center tile of the circular (square) area.
        radius (int): Radius of the area.

    Returns:
        tile_coord_list (list): List of tuples containing all tile coordinates within the area.

    """

    center_x, center_y = coords

    tile_coord_list = []
    start_x = center_x - radius
    end_x = center_x + radius + 1
    start_y = center_y - radius
    end_y = center_y + radius + 1

    for tile_in_radius_x in range(start_x, end_x):
        for tile_in_radius_y in range(start_y, end_y):
            tile_coord_list.append((tile_in_radius_x, tile_in_radius_y))

    return tile_coord_list


def map_check_for_wall(incoming_map, coords_x, coords_y):

    if coords_x < 0 or coords_y < 0 or coords_x >= constants.MAP_WIDTH or coords_y >= constants.MAP_HEIGHT:
        return False

    else:
        return incoming_map[coords_x][coords_y].block_path


def assign_tiles(incoming_map):
    """ Assigns bitmasking value to each wall piece.

    Args:
        incoming_map: map object

    Returns:
        None

    """

    for x in range(len(incoming_map)):
        for y in range(len(incoming_map[0])):

            tile_is_wall = map_check_for_wall(incoming_map, x, y)

            if tile_is_wall:
                assign_num = 0

                # check surrounding walls
                if map_check_for_wall(incoming_map, x, y-1):
                    assign_num += 1
                if map_check_for_wall(incoming_map, x+1, y):
                    assign_num += 2
                if map_check_for_wall(incoming_map, x, y+1):
                    assign_num += 4
                if map_check_for_wall(incoming_map, x-1, y):
                    assign_num += 8

                if assign_num == 15 and not map_check_for_wall(incoming_map, x-1, y-1):
                    assign_num = 22
                elif assign_num == 15 and not map_check_for_wall(incoming_map, x+1, y-1):
                    assign_num = 33
                elif assign_num == 15 and not map_check_for_wall(incoming_map, x-1, y+1):
                    assign_num = 44
                elif assign_num == 15 and not map_check_for_wall(incoming_map, x+1, y+1):
                    assign_num = 55

                incoming_map[x][y].assignment = assign_num
