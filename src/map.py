import random

import tcod

from src import constants, globalvars, data
from src.generators import itemgen, creaturegen, specialgen


class ObjRoom:
    """Rectangular room object containing relevant properties such boundary and center coordinates.

    Attributes
    ----------
    x1 : int
        The map-grid x-coordinate of the room's left side.
    y1 : int
        The map-grid y-coordinate of the room's top side.
    width : int
        The number of map-grids the room spans width-wise.
    height : int
        The number of map-grids the room spans height-wise.
    x2 : int
        The map-grid x-coordinate of the room's right side.
    y2 : int
        The map-grid y-coordinate of the room's bottom side.
    center_x : int
        The center map-grid x-coordinate of the room.
    center_y : int
        The center map-grid y-coordinate of the room.
    """

    def __init__(self, coords_topleft, size):
        self.x1, self.y1 = coords_topleft
        self.width, self.height = size

        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.center_x = None
        self.center_y = None

    @property
    def center(self):
        """tuple: Calculates and returns the center (x, y) coordinate of the room."""
        self.center_x = int((self.x1 + self.x2)/2)
        self.center_y = int((self.y1 + self.y2)/2)

        return self.center_x, self.center_y

    def intersects(self, other):
        """Determines whether this room intersects with another room object.

        Parameters
        ----------
        other : ObjRoom
            Another room object.

        Returns
        -------
        bool:
            True if this room intersects with `other` room.

        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def map_create():
    """Creates a map.

    Procedurally generates a map using Tunneling Algorithm, which initiates all map tiles as wall
    first and "digs" out rectangular rooms and connects them with passages.

    Returns
    -------
    tuple
        Contains the new_map, which is a 2d array of StrucTile objects (walls, floors)
        and a list of room objects in this map
    """
    # initialize empty map with wall tiles
    new_map = [[data.StructTile(True) for y in range(0, constants.MAP_HEIGHT)]
               for x in range(0, constants.MAP_WIDTH)]

    list_of_rooms = []

    # generate new rooms
    for i in range(constants.MAP_MAX_NUM_ROOMS):
        room_width = tcod.random_get_int(0, constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        room_height = tcod.random_get_int(0, constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)

        room_x = tcod.random_get_int(0, 2, constants.MAP_WIDTH - 2 - room_width)
        room_y = tcod.random_get_int(0, 2, constants.MAP_HEIGHT - 2 - room_height)

        new_room = ObjRoom((room_x, room_y), (room_width, room_height))

        failed = False
        for other_room in list_of_rooms:
            if new_room.intersects(other_room):
                failed = True
                break

        if not failed:
            # dig out the walls and make them into floors
            map_create_room(new_map, new_room)

            if len(list_of_rooms) != 0:
                previous_room = list_of_rooms[-1]
                map_create_tunnels(new_map, new_room.center, previous_room.center)

            list_of_rooms.append(new_room)

    # load in created map and assign bitmasking
    assign_tiles(new_map)

    create_fov_map(new_map)

    return new_map, list_of_rooms


def map_create_room(target_map, new_room):
    """Turn all walls in the room area to floor tiles and add random pillars in the room.

    Parameters
    ----------
    target_map : list (2d array)
        The map being worked on.
    new_room : ObjRoom
        The room object specifying properties to help dig out the area.

    Returns
    -------
    None
    """
    def add_to_x_y(_x, _y):
        rand_add_x = random.choice((-1, 0, 1))
        _x += rand_add_x

        if rand_add_x == 0:
            rand_add_y = random.choice((-1, 1))
        else:
            rand_add_y = random.choice((-1, 0, 1))
        _y += rand_add_y

        return _x, _y

    # change wall tiles to floor tiles in the room
    for x in range(new_room.x1, new_room.x2 + 1):
        for y in range(new_room.y1, new_room.y2 + 1):
            target_map[x][y].block_path = False

    pillar_x1, pillar_y1 = None, None

    # spawn a few "pillar" walls (80% chance) around the room if the room is "big"
    if new_room.width * new_room.height > 64 and tcod.random_get_int(0, 1, 100) < 80:

        # spawn at least 2 tiles from walls and not the middle tile
        pillar_x1 = tcod.random_get_int(0, new_room.x1 + 2, new_room.x2 - 2)
        pillar_y1 = tcod.random_get_int(0, new_room.y1 + 2, new_room.y2 - 2)

        if (pillar_x1, pillar_y1) == (new_room.center_x, new_room.center_y):
            pillar_x1, pillar_y1 = add_to_x_y(pillar_x1, pillar_y1)

        target_map[pillar_x1][pillar_y1].block_path = True

    # spawn a double pillar
    if new_room.width * new_room.height > 100:

        pillar_x2 = tcod.random_get_int(0, new_room.x1 + 3, new_room.x2 - 3)
        pillar_y2 = tcod.random_get_int(0, new_room.y1 + 3, new_room.y2 - 3)

        while (pillar_x2, pillar_y2) == (new_room.center_x, new_room.center_y) or \
                (pillar_x2, pillar_y2) == (pillar_x1, pillar_y1):

            pillar_x2, pillar_y2 = add_to_x_y(pillar_x2, pillar_y2)

        adj_possible_list = [(pillar_x2, pillar_y2 - 1), (pillar_x2 + 1, pillar_y2),
                             (pillar_x2, pillar_y2 + 1), (pillar_x2 - 1, pillar_y2)]
        pillar_x2_adj, pillar_y2_adj = random.choice([(x, y) for (x, y) in adj_possible_list
                                                      if (x, y) != (new_room.center_x, new_room.center_y)
                                                      or (x, y) != (pillar_x1, pillar_y1)])

        target_map[pillar_x2][pillar_y2].block_path = True
        target_map[pillar_x2_adj][pillar_y2_adj].block_path = True


def map_create_tunnels(target_map, new_center, prev_center):
    """Creates a one-tile width horizontal and/or vertical tunnel connecting one room to another.

    Parameters
    ----------
    target_map : list (2d array)
        The map being worked on.
    new_center : tuple
        The center coordinates of the newer room.
    prev_center : tuple
        The center coordinates of a previous room.

    Returns
    -------
    None
    """

    x1, y1 = new_center
    x2, y2 = prev_center

    # give a 50% chance that the tunnel will be created in the horizontal direction first
    order_of_tunnel_drawn = tcod.random_get_int(0, 0, 1)

    if order_of_tunnel_drawn == 1:
        # create horizontal tunnel first
        for x in range(min(x1, x2), max(x1, x2) + 1):
            target_map[x][y1].block_path = False

        # create vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            target_map[x2][y].block_path = False
    else:

        # create vertical tunnel first
        for y in range(min(y1, y2), max(y1, y2) + 1):
            target_map[x1][y].block_path = False

        # create horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) + 1):
            target_map[x][y2].block_path = False


def map_place_items_creatures(room_list):
    """Randomly generates items and mobs in each room on the map.

    Parameters
    ----------
    room_list : list
        List of room objects.

    Returns
    -------
    None
    """
    floor_num = globalvars.GAME.max_floor_reached
    cur_floor = globalvars.GAME.cur_floor
    is_top_floor = (floor_num == constants.MAP_MAX_NUM_FLOORS)
    first_floor = (len(globalvars.GAME.maps_prev) == 0)

    for i, room in enumerate(room_list):
        first_room = (i == 0)
        last_room = (room == room_list[-1])

        min_x, max_x = room.x1, room.x2
        min_y, max_y = room.y1, room.y2

        # generate PLAYER in the center of the first room (no monsters unless for testing)
        if first_room:
            globalvars.PLAYER.x, globalvars.PLAYER.y = room.center
            creaturegen.gen_enemy((min_x, max_x), (min_y, max_y), cur_floor)
            creaturegen.gen_friendly_mob((min_x, max_x), (min_y, max_y), cur_floor)

        # only generate enemies in the rooms that the player doesnt start in
        if not first_room:
            creaturegen.gen_enemy((min_x, max_x), (min_y, max_y), cur_floor)
            creaturegen.gen_friendly_mob((min_x, max_x), (min_y, max_y), cur_floor)

            if room.width * room.height > 81:
                creaturegen.gen_enemy((min_x, max_x), (min_y, max_y), cur_floor)

            if room.width * room.height > 144:
                creaturegen.gen_enemy((min_x, max_x), (min_y, max_y), cur_floor)

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

        # items are not allowed to spawn on top of player
        while (item_x, item_y) == (globalvars.PLAYER.x, globalvars.PLAYER.y) \
                or wall_at_coords(globalvars.GAME.current_map, item_x, item_y):
            item_x = tcod.random_get_int(0, min_x, max_x)
            item_y = tcod.random_get_int(0, min_y, max_y)

        itemgen.gen_item(cur_floor, (item_x, item_y))


def creature_at_coords(x, y, exclude=None):
    """Return the creature object at (x, y) if there is one.

    Parameters
    ----------
    x : int
        The map-grid x-coordinate to query.
    y : int
        The map-grid y-coordinate to query.
    exclude : ObjActor, optional
        An actor object that needs to be excluded from the query.

    Returns
    -------
    ObjActor or None
        A creature object or None if there is no creature there.
    """

    for obj in globalvars.GAME.current_objects:
        if obj is not exclude and obj.x == x and obj.y == y and obj.creature is not None:
            return obj

    return None


def create_fov_map(target_map):
    """Creates the fov map for the `target_map`.

    Parameters
    ----------
    target_map : list (2d array)
        The target map for the fov map.

    Returns
    -------
    None

    """
    globalvars.FOV_MAP = tcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            tcod.map_set_properties(globalvars.FOV_MAP, x, y,
                                    not target_map[x][y].block_path,
                                    not target_map[x][y].block_path)


def update_fov():
    """Update the fov based on the PLAYER's current position on the map.

    Returns
    -------
    None

    """
    if globalvars.FOV_CALCULATE:
        tcod.map_compute_fov(globalvars.FOV_MAP, globalvars.PLAYER.x, globalvars.PLAYER.y,
                             constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALG)
        globalvars.FOV_CALCULATE = False


def objects_at_coords(x, y):
    """Returns a list of all actor objects at the map-grid (x, y) coordinate.

    Parameters
    ----------
    x : int
        The map-grid x-coordinate to query.
    y : int
        The map-grid y-coordinate to query

    Returns
    -------
    list
        A list of all actor objects at (x, y).

    """
    return [obj for obj in globalvars.GAME.current_objects if obj.x == x and obj.y == y]


def tiles_in_line(coords1, coords2):
    """Generates a list of map-grid coordinates of tiles in between `coords1` and `coords2`.

    Parameters
    ----------
    coords1 : tuple
        Start map-grid coordinate (x, y) for the line path.
    coords2 : tuple
        End map-grid coordinate (x, y) for the line path.

    Returns
    -------
    list
        A list of map-grid coordinates in the line path.

    """
    coords_iter = tcod.line_iter(*coords1, *coords2)

    return list(coords_iter)


def tiles_in_radius(center_coords, radius):
    """Generates a list of map-grid coordinates of tiles in a `radius` around the center `coords`

    Parameters
    ----------
    center_coords :tuple
        The center map-grid coordinates of this area of tiles.
    radius : int
        The radius of the circle area.

    Returns
    -------
    list
        A list of map-grid coordinates in the area.

    """
    center_x, center_y = center_coords

    coords_list = []
    start_x = center_x - radius
    end_x = center_x + radius

    start_y = center_y - radius
    end_y = center_y + radius

    for tile_in_radius_x in range(start_x, end_x + 1):
        for tile_in_radius_y in range(start_y, end_y + 1):
            coords_list.append((tile_in_radius_x, tile_in_radius_y))

    if radius >= 2:
        coords_remove = ((start_x, start_y), (end_x, end_y), (start_x, end_y), (end_x, start_y))
        coords_list = [coord for coord in coords_list if coord not in coords_remove]

    return coords_list


def wall_at_coords(target_map, x, y):
    """Checks whether there is a wall at the specified coordinates.

    Parameters
    ----------
    target_map : list (2d array)
        The target map to check.
    x : int
        The map-grid x-coordinate of the query.
    y : int
        The map-grid y-coordinate of the query.

    Returns
    -------
    bool
        True if there is a wall, False otherwise.

    """
    if x < 0 or y < 0 or x >= constants.MAP_WIDTH or y >= constants.MAP_HEIGHT:
        return True
    else:
        return target_map[x][y].block_path


def assign_tiles(target_map):
    """Assigns bitmask value to wall and floor tiles.

    Parameters
    ----------
    target_map : list (2d array)
        The target map to assign bitmasks to.

    Returns
    -------
    None

    """
    for x in range(len(target_map)):
        for y in range(len(target_map[0])):
            tile_is_wall = wall_at_coords(target_map, x, y)
            if tile_is_wall:
                wall_assign_num = 0

                # check surrounding walls
                if wall_at_coords(target_map, x, y-1):
                    wall_assign_num += 1
                if wall_at_coords(target_map, x+1, y):
                    wall_assign_num += 2
                if wall_at_coords(target_map, x, y+1):
                    wall_assign_num += 4
                if wall_at_coords(target_map, x-1, y):
                    wall_assign_num += 8

                if wall_assign_num == 15 and not wall_at_coords(target_map, x-1, y-1):
                    wall_assign_num = 22
                elif wall_assign_num == 15 and not wall_at_coords(target_map, x+1, y-1):
                    wall_assign_num = 33
                elif wall_assign_num == 15 and not wall_at_coords(target_map, x-1, y+1):
                    wall_assign_num = 44
                elif wall_assign_num == 15 and not wall_at_coords(target_map, x+1, y+1):
                    wall_assign_num = 55

                # for the dungeon_tileset walls
                if wall_assign_num == 6 and wall_at_coords(target_map, x+1, y+1) or \
                        (wall_assign_num == 14 and wall_at_coords(target_map, x+1, y+1)
                         and not wall_at_coords(target_map, x-1, y+1)):
                    wall_assign_num = 77
                elif (wall_assign_num == 3 and wall_at_coords(target_map, x+1, y-1)) or \
                        (wall_assign_num == 9 and wall_at_coords(target_map, x-1, y-1)):
                    wall_assign_num = 11

                elif wall_assign_num == 12 and wall_at_coords(target_map, x-1, y+1):
                    wall_assign_num = 66

                elif wall_assign_num == 14 and wall_at_coords(target_map, x-1, y+1) and \
                        not wall_at_coords(target_map, x+1, y+1):
                    wall_assign_num = 88

                elif wall_assign_num == 7 and not wall_at_coords(target_map, x+1, y+1) and \
                        not wall_at_coords(target_map, x-1, y):
                    wall_assign_num = 99
                elif wall_assign_num == 7 and not wall_at_coords(target_map, x+1, y+1):
                    wall_assign_num = 55
                elif wall_assign_num == 7 and not wall_at_coords(target_map, x+1, y-1) and \
                        not wall_at_coords(target_map, x-1, y):
                    wall_assign_num = 100
                elif wall_assign_num == 7 and not wall_at_coords(target_map, x+1, y-1):
                    wall_assign_num = 33

                elif wall_assign_num == 9 and wall_at_coords(target_map, x - 1, y - 1):
                    wall_assign_num = 10

                elif wall_assign_num == 13 and not wall_at_coords(target_map, x-1, y+1) and \
                        not wall_at_coords(target_map, x+1, y):
                    wall_assign_num = 122
                elif wall_assign_num == 13 and not wall_at_coords(target_map, x-1, y+1):
                    wall_assign_num = 44
                elif wall_assign_num == 13 and not wall_at_coords(target_map, x-1, y-1) and \
                        not wall_at_coords(target_map, x+1, y):
                    wall_assign_num = 111

                target_map[x][y].wall_assignment = wall_assign_num

            # bitmask for floor tiles
            else:
                floor_assign_num = 0

                if wall_at_coords(target_map, x, y-1):
                    floor_assign_num += 1
                if wall_at_coords(target_map, x+1, y):
                    floor_assign_num += 2
                if wall_at_coords(target_map, x, y+1):
                    floor_assign_num += 4
                if wall_at_coords(target_map, x-1, y):
                    floor_assign_num += 8

                target_map[x][y].floor_assignment = floor_assign_num
