# Game Title: Tower of Rak
# 3rd party modules
import pygame
import sys
import pickle
import gzip
import tcod
import textwrap
import math
import random

# game files
import constants


# ================================================================= #
#                       -----  Structs  -----                       #
#                          --- SECTION ---                          #
# ================================================================= #
class StructTile:
    """A class which functions like a struct that tracks the data for each tile within a map.

    Attributes:
        block_path (arg, bool) : True if the tile is like a wall, which blocks any movement onto or through the tile.
        explored (bool): Indicates whether the player has encountered the tile before and is initialized to False.

    """

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


class StructAssets:
    """A class which functions like a struct and contains all the assets used in the game.

    Loads sprite sheets using the ObjSpriteSheet class and creates individual sprite images and animations from the
    ObjActor class. Will also include music and sound effects.

    """

    def __init__(self):

        # ========================== SPRITE SHEETS ========================== #

        # ---> Character folder
        self.reptile = ObjSpriteSheet("data/graphics/Characters/Reptile.png")
        self.aquatic = ObjSpriteSheet("data/graphics/Characters/Aquatic.png")
        self.player = ObjSpriteSheet("data/graphics/Characters/Player.png")
        self.avian = ObjSpriteSheet("data/graphics/Characters/Avian.png")
        self.slime = ObjSpriteSheet("data/graphics/Characters/Slime.png")

        # ---> Items folder
        self.flesh = ObjSpriteSheet("data/graphics/Items/Flesh.png")
        self.food = ObjSpriteSheet("data/graphics/Items/Food.png")
        self.medium_weapon = ObjSpriteSheet("data/graphics/Items/MedWep.png")
        self.shield = ObjSpriteSheet("data/graphics/Items/Shield.png")
        self.scroll = ObjSpriteSheet("data/graphics/Items/Scroll.png")

        # ---> Objects folder
        self.wall = ObjSpriteSheet("data/graphics/Objects/Wall.png")
        self.floor = ObjSpriteSheet("data/graphics/Objects/Floor.png")
        self.tile = ObjSpriteSheet("data/graphics/Objects/Tile.png")

        # ============================ SPRITES ============================= #

        #                        ||| Animations |||

        # ---> Player
        self.A_PLAYER = self.player.get_animation('a', 15, 2, 16, 16, (32, 32))

        # ---> Enemy creatures
        self.A_COBRA = self.reptile.get_animation('k', 5, 2, 16, 16, (32, 32))
        self.A_GIANT_BOA = self.reptile.get_animation('e', 5, 2, 16, 16, (32, 32))
        self.A_HEALER_SLIME = self.slime.get_animation('a', 4, 2, 16, 16, (32, 32))

        #                        ||| Still Sprites |||

        # ---> Dungeon structures
        self.S_WALL = self.wall.get_image('d', 7, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED = self.wall.get_image('d', 13, 16, 16, (32, 32))[0]

        self.S_FLOOR = self.floor.get_image('b', 8, 16, 16, (32, 32))[0]
        self.S_FLOOR_EXPLORED = self.floor.get_image('b', 14, 16, 16, (32, 32))[0]

        # ---> Items
        self.S_TOMATO = self.food.get_image('g', 3, 16, 16, (32, 32))
        self.S_RADISH = self.food.get_image('b', 4, 16, 16, (32, 32))
        self.S_CABBAGE = self.food.get_image('f', 4, 16, 16, (32, 32))
        self.S_WATER_CUP = self.food.get_image('f', 5, 16, 16, (32, 32))
        self.S_SCROLL_1 = self.scroll.get_image('e', 2, 16, 16, (32, 32))
        self.S_SCROLL_2 = self.scroll.get_image('c', 2, 16, 16, (32, 32))
        self.S_SCROLL_3 = self.scroll.get_image('d', 6, 16, 16, (32, 32))
        self.S_FLESH_SNAKE = self.flesh.get_image('b', 4, 16, 16, (32, 32))

        # ---> Equipment
        self.S_32_SWORD = self.medium_weapon.get_image('a', 1, 16, 16, (32, 32))
        self.S_32_SHIELD = self.shield.get_image('a', 1, 16, 16, (32, 32))

        # ---> Special
        self.S_STAIRS_UP = self.tile.get_image('a', 2, 16, 16, (32, 32))
        self.S_STAIRS_DOWN = self.tile.get_image('b', 2, 16, 16, (32, 32))
        self.S_MAIN_MENU = pygame.image.load("data/graphics/landscape.png")
        self.S_MAIN_MENU = pygame.transform.scale(self.S_MAIN_MENU, (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))


        # animation dictionary to reference when generating objects (a way to avoid saving error)
        self.animation_dict = {

            "A_PLAYER": self.A_PLAYER,
            "A_COBRA": self.A_COBRA,
            "A_GIANT_BOA": self.A_GIANT_BOA,
            "A_HEALER_SLIME": self.A_HEALER_SLIME,
            "S_TOMATO": self.S_TOMATO,
            "S_RADISH": self.S_RADISH,
            "S_CABBAGE": self.S_CABBAGE,
            "S_WATER_CUP": self.S_WATER_CUP,
            "S_SCROLL_1": self.S_SCROLL_1,
            "S_SCROLL_2": self.S_SCROLL_2,
            "S_SCROLL_3": self.S_SCROLL_3,
            "S_FLESH_SNAKE": self.S_FLESH_SNAKE,
            "S_32_SWORD": self.S_32_SWORD,
            "S_32_SHIELD": self.S_32_SHIELD,
            "S_STAIRS_UP": self.S_STAIRS_UP,
            "S_STAIRS_DOWN": self.S_STAIRS_DOWN
        }

        # =============================== AUDIO ================================== #

        #                             ||| Music |||

        self.main_menu_music = "data/audio/music/RPG-Blues_Looping.ogg"

        #                          ||| Sound Effects |||

        self.sfx_list = []

        self.sfx_hit_punch1 = self.sfx_add("data/audio/sfx/hit_punch_1.wav")
        self.sfx_hit_punch2 = self.sfx_add("data/audio/sfx/hit_punch_2.wav")
        self.sfx_hit_punch3 = self.sfx_add("data/audio/sfx/hit_punch_3.wav")
        self.sfx_hit_punch4 = self.sfx_add("data/audio/sfx/hit_punch_4.wav")
        self.sfx_hit_punch5 = self.sfx_add("data/audio/sfx/hit_punch_5.wav")

        self.sfx_hit_punch_list = [self.sfx_hit_punch1,
                                   self.sfx_hit_punch2,
                                   self.sfx_hit_punch3,
                                   self.sfx_hit_punch4,
                                   self.sfx_hit_punch5]

    def sfx_add(self, file_address):
        """ Loads new sound effect and adds the sfx to the master sfx list.

        Args:
            file_address (str): File address of the sfx to be loaded in.

        Returns:
            new_sfx (Sound obj): The loaded sfx Sound object.

        """

        new_sfx = pygame.mixer.Sound(file_address)

        self.sfx_list.append(new_sfx)

        return new_sfx


# ================================================================= #
#                       -----  Objects  -----                       #
#                          --- SECTION ---                          #
# ================================================================= #

class ObjActor:
    """An actor object class that essentially represents every entity in the game.

    This is an object that can be anything that appears in the game and is differentiated mainly through the components
    that make up and control the object.
    Note that this rouge-like game mainly uses the composition/component system over inheritance.

    Attributes:
        x (arg, int): Tile map address of the actor object on the x-axis.
        y (arg, int): Tile map address of the actor object on the y-axis.
        name_object (arg, str): Name of the object type, "scroll" or "snake" for example.
        animation (list): List of images for the object's display (can be a list of one image).
                          Created in the StructAssets class and usually denoted as "A_..." or "S_...".
        animation_speed (arg, float): Time in seconds it takes to loop through the object animation.
                                      Default value is initialized as 0.5

    Components:
        creature: Created from the ComCreature class. Has health, and can move and fight.
        ai: Created from classes that have the prefix "Ai" like AiChase. Gives actor object specific rules to follow.
        container: Created from the ComContainer class. Gives actor object ability to have an inventory.
        item: Created from the ComItem class. Gives actor objects the ability to be picked up and be potentially usable.

    """

    def __init__(self, x, y,
                 name_object,
                 animation_key,
                 animation_speed=0.5,
                 creature=None,
                 ai=None,
                 container=None,
                 item=None,
                 equipment=None,
                 stairs=None):   # None is implicitly False

        self.x = x  # map address (not pixel address)
        self.y = y  # map address (not pixel address)
        self.name_object = name_object  # name of object, might change to object_name or name_object_type
        self.animation_key = animation_key
        self.animation = ASSETS.animation_dict[animation_key]
        self.animation_speed = animation_speed/1.0   # in seconds (always converted to a float, even if its an int)

        # animation flicker speed (over the course of # of secs)
        self.flicker_speed = self.animation_speed/len(self.animation)   # amount of display time for each img
        self.flicker_timer = 0.0
        self.sprite_image = 0

        self.creature = creature
        if creature:
            self.creature.owner = self   # component system implementation

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:    # if it has a container component, then...
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            # automatically give item component to equipment actor object
            self.item = ComItem()
            self.item.owner = self

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

    @property
    def display_name(self):
        """Combines creature names and their object (type) name. Adds the "[E]" indicator for equipped items.

        Returns:
            name_to_display (str): The full name of a creature or the equip status of an equipment item.

        """

        if self.creature:
            name_to_display = "{} the {}".format(self.creature.name_instance, self.name_object)
            return name_to_display

        if self.item:
            if self.equipment and self.equipment.equipped is True:
                name_to_display = "{} [E]".format(self.name_object)
                return name_to_display
            else:
                name_to_display = self.name_object
                return name_to_display

    def draw(self):
        """Draws the actor object to the screen.

        Draws the actor object to the map screen if it appears within the PLAYER's fov. If the object as multiple sprite
        images in its animation list, it keeps track of the timing of the animations and triggers a transition to
        display the next image in the list. This will give off an "idle" animation look, where creatures usually bob up
        and down.

        """

        is_visible = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visible:
            if len(self.animation) == 1:
                # pixel address
                SURFACE_MAP.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

            elif len(self.animation) > 1:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1/CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0
                    else:
                        self.sprite_image += 1

            # fixes rare occurrence when self.sprite_image is 1 when len(self.animation) changed from 2 to 1 already,
            # which caused index out of bounds error
            if len(self.animation) == 1:
                self.sprite_image = 0

            SURFACE_MAP.blit(self.animation[self.sprite_image],
                              (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def distance_to(self, other):
        """Calculates the relative distance of this actor object to another.

        Args:
            other (ObjActor): Another actor object.

        Returns:
            shortest_distance_to_other (float): The straight distance to the "other" actor object.

        """

        dx = other.x - self.x
        dy = other.y - self.y

        # shortest distance to another actor object in tile number measurements
        shortest_distance_to_other = math.sqrt(dx ** 2 + dy ** 2)

        return shortest_distance_to_other

    def move_towards(self, other):
        """Moves this actor object closer towards another object.

            Used in the AiChase to chase after a specified actor object.
            Uses the move() method in the ComCreature component class.

        Args:
            other (ObjActor): Target actor object to move towards

        """

        dx = other.x - self.x
        dy = other.y - self.y

        # shortest distance to another actor object in tile number measurements
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        self.creature.move(dx, dy)

    def move_away(self, other):
        """Moves this actor object away from another object.

            Used in the AiFlee to get away from a specified actor object.
            Uses the move() method in the ComCreature component class.

        Args:
            other (ObjActor): Target actor object to move towards

        """

        dx = self.x - other.x
        dy = self.y - other.y

        # shortest distance to another actor object in tile number measurements
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        self.creature.move(dx, dy)

    def animation_del(self):
        """ Get rid of any animation assets.

        For the purpose of avoiding pygame.Surface objects dump, which can't be pickled.

        Returns:
            None

        """

        self.animation = None

    def animation_init(self):
        """ Sets animation back to referencing animations from ASSETS (and not None after animation_del)

        Returns:
            None
        """

        self.animation = ASSETS.animation_dict[self.animation_key]


class ObjGame:
    """A game object class that tracks game progress and entities.

    Stores and tracks all information including maps, objects, and a record of game messages.

    Attributes:
        current_objects (list): List of objects on the current map (and not in an actor's container inventory).
        message_history (list): List of messages that have been displayed to the player on the game screen.
        maps_next (list): List map data (tuple) saved before transitioning to previous maps.
        maps_prev (list): List map data (tuple) saved before transitioning to a new map.
        current_map (2d-array): The map that is currently loaded and displayed.
        current_rooms (list): List of all valid ObjRoom objects on the displayed map.

    """
    def __init__(self):
        self.current_objects = []
        self.message_history = []  # an empty list
        self.maps_next = []
        self.maps_prev = []
        self.current_map, self.current_rooms = map_create()

    def map_transition_next(self):
        """Creates a new map if there are no maps in maps_next queue. Otherwise, load the last map in maps_next.

        """
        global FOV_CALCULATE

        FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_del()

        # save data of current map (before creating new map) on to maps_prev list
        save_data = (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
        self.maps_prev.append(save_data)

        if len(self.maps_next) == 0:

            # erase all items from previous map except the PLAYER
            self.current_objects = [PLAYER]
            PLAYER.animation_init()

            self.current_map, self.current_rooms = map_create()
            map_place_items_creatures(self.current_rooms)

        else:

            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map_make_fov(self.current_map)

            FOV_CALCULATE = True

            del self.maps_next[-1]

        game_message("{} moved up a floor!".format(PLAYER.creature.name_instance), constants.COLOR_BLUE)

    def map_transition_prev(self):
        """Loads the last map in maps_prev, saving data of current map before doing so.

        """
        global FOV_CALCULATE

        if len(self.maps_prev) != 0:
            for obj in self.current_objects:
                obj.animation_del()

            save_data = (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
            self.maps_next.append(save_data)

            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_prev[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map_make_fov(self.current_map)

            FOV_CALCULATE = True

            del self.maps_prev[-1]

        game_message("{} moved down a floor!".format(PLAYER.creature.name_instance), constants.COLOR_BLUE)


class ObjSpriteSheet:
    """A sprite sheet object class that contain methods to grab images out of a sprite sheet.

    Access and grab subsections or individual sprites after loading in a sprite sheet. Will also scale the sprites to
    32 x 32.

    Attributes:
        file_name (arg, str): String that specifies the directory/filename of the sprite sheet to be loaded.
        sprite_sheet (pygame.Surface): The loaded sprite sheet.
        tileDict (dict): Dictionary mapping alphabetical letters to column numbers.

    """

    def __init__(self, file_name):
        # load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tileDict = {'A': 0,
                         'a': 1, 'b': 2, 'c': 3, 'd': 4,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8,
                         'i': 9, 'j': 10, 'k': 11, 'l': 12,
                         'm': 13, 'n': 14, 'o': 15, 'p': 16}    # Thus, (A, 0) will get the upper left corner sprite

    def get_image(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, scale=None):
        """Returns a single sprite.

        Given a loaded sprite sheet, blits a single sprite specified by column (char) and row (int) onto a new pygame
        surface and appends that image onto image_list (list).

        Args:
            column (str): Letter that's converted into an integer, which gives the column in the loaded sprite sheet.
            row (int): Gives the row in the loaded sprite sheet.
            width (int): Individual sprite width in pixels
            height (int): Individual sprite height in pixels
            scale ((width, height)) = Optional argument that scales the sprites to the new specified size.

        Returns:
            image_list (list): A list of length 1 containing a single sprite from the sprite sheet loaded
                              from initialization.

        """

        # create a new image

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (self.tileDict[column] * width, row * height, width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list

    def get_animation(self, column, row, num_sprites=1, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT,
                      scale=None):
        """Returns a sequence of sprites.

        Given a loaded sprite sheet, appends a sequence of sprites specified by column (char) and row (int) and number
        of sprites in the animation sequence onto image_list (list).

        Args:
            column (str): Letter that's converted into an integer, which gives the column in the loaded sprite sheet.
            row (int): Gives the row in the loaded sprite sheet.
            num_sprites (int): Number of sequential sprites to be loaded. Includes the one specified by the column and
                               row arguments as well as the sprites following it.
            width (int): Individual sprite width in pixels
            height (int): Individual sprite height in pixels
            scale ((width, height)) = Optional argument that scales the sprites to the new specified size.

        Returns:
            image_list (list): A list containing a sequence of sprites from the sprite sheet loaded from initialization.

        """

        # create a new image

        image_list = []

        for i in range(num_sprites):
            # create blank image
            image = pygame.Surface([width, height]).convert()

            # copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0, 0), (self.tileDict[column] * width + (width * i), row * height, width, height))

            # set transparency key to black
            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list


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

    @property
    def center(self):
        """A property method that takes x and y coordinates and calculates the center coordinate of the room.

        Returns:
            center_x (int): The x coordinate of the center of the room.
            center_y (int): The y coordinate of the center of the room.

        """
        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)

        return center_x, center_y

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


class ObjCamera:
    """Camera object that updates the view of the map as the player moves around.

    Attributes:
        width (int): The width of the rectangular camera display in pixels
        height (int): The height of the rectangular camera display in pixels
        x (int): The x (pixel) coordinate of the camera rectangle to be aligned to a surface.
        y (int): The y (pixel) coordinate of the camera rectangle to be aligned to a surface.

    """

    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.x, self.y = (0, 0)

    @property
    def rectangle(self):
        """Creates the rectangle area of the camera object and aligns its center coordinates accordingly.

        Returns:
            pos_rect (Rect): A pygame's rectangle object aligned at the center.

        """
        pos_rect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

        pos_rect.center = (self.x, self.y)

        return pos_rect

    @property
    def map_address(self):
        """Converts the camera's center map-pixel coordinates to map-tile coordinates.

        Returns:
            tup_map_tile_coords (tuple): The converted map-tile coordinates of the camera's center position on the map.

        """

        map_x = int(self.x / constants.CELL_WIDTH)
        map_y = int(self.y / constants.CELL_HEIGHT)

        tup_map_tile_coords = (map_x, map_y)

        return tup_map_tile_coords

    def update_pos(self):
        """Updates and sets the position of the x, y coordinates of camera.

        Follows the coordinate (relative to SURFACE_MAP) of the center of the player. Have the option of making the
        camera lag behind a bit, or have to catch up in a smooth motion.

        """

        # add half the pixel dimensions of one cell as PLAYER coordinates are aligned to the cell's upper-left corner
        target_x = (PLAYER.x * constants.CELL_WIDTH) + (constants.CELL_WIDTH/2)
        target_y = (PLAYER.y * constants.CELL_HEIGHT) + (constants.CELL_HEIGHT/2)

        distance_to_target_x, distance_to_target_y = self. map_dist_to_cam((target_x, target_y))

        camera_speed = 1

        self.x += int(distance_to_target_x * camera_speed)
        self.y += int(distance_to_target_y * camera_speed)

    def map_dist_to_cam(self, tup_coords):
        """Gives x and y distance from specified map-coordinate to camera's center map-coordinate.

        Calculates the x and y coordinate difference between a specified coordinate on the map and the center
        map-coordinate of the camera. Every value is expressed in pixels.

        Args:
            tup_coords (tuple): Pixel coordinates relative to the map, or SURFACE_MAP.

        Returns:
            tup_diff_coord (tuple): Pixel coordinates relative to the map of the calculated x and y difference.

        """

        map_x, map_y = tup_coords

        distance_diff_x = map_x - self.x
        distance_diff_y = map_y - self.y

        tup_diff_coord = (distance_diff_x, distance_diff_y)

        return tup_diff_coord

    def window_dist_to_cam(self, tup_coords):
        """Gives x and y distance from specified window-coordinate to camera's center window-coordinate.

        Calculates the x and y coordinate difference between a specified coordinate on the window and the center
        window-coordinate of the camera. Every value is expressed in pixels.

        Args:
            tup_coords (tuple): Pixel coordinates relative to the window, or SURFACE_MAIN.

        Returns:
            tup_diff_coord (tuple): Pixel coordinates relative to the window of the calculated x and y difference.

        """

        window_x, window_y = tup_coords

        distance_diff_x = window_x - (self.width / 2)
        distance_diff_y = window_y - (self.height / 2)

        tup_diff_coord = (distance_diff_x, distance_diff_y)

        return tup_diff_coord

    def window_to_map(self, tup_coords):
        target_x, target_y = tup_coords

        # convert window coordinates to distance from camera
        cam_wind_dx, cam_wind_dy = self.window_dist_to_cam((target_x, target_y))

        # distance from camera to map coordinate
        map_pix_x = self.x + cam_wind_dx
        map_pix_y = self.y + cam_wind_dy

        # pixel map coordinates converted from window pixel coordinates
        tup_map_coords = (map_pix_x, map_pix_y)

        return tup_map_coords


# ================================================================= #
#                      -----  Components  -----                     #
#                          --- SECTION ---                          #
# ================================================================= #


class ComCreature:
    """Creature component gives actor objects health and fighting properties.

    Creatures have health, can damage other objects by attacking them and possibly die.

    Attributes:
        name_instance (arg, str): Name of the individual creature. Randomly generated using namegen methods in tcod
                                  library. See gen_enemy() function under Generation for details.
        max_hp (arg, int): Max hit points of the creature. Default value initialized as 10.
        base_atk (arg, int): Base attack power of the creature. Default value initialized as 2.
        base_def (arg, int): Base defence of the creature. Default value initialized as 0.
        death_function (arg, function): Function to be executed when current_hp is 0 or below.
        current_hp (int): Current health of the creature.

    """

    def __init__(self, name_instance,
                 max_hp=10,
                 base_atk=2,
                 base_def=0,
                 death_function=None):

        self.name_instance = name_instance
        self.maxHp = max_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.current_hp = max_hp
        self.death_function = death_function

    def move(self, dx, dy):
        """Moves the creature object on the map.

        Args:
            dx (int): Distance in tile map coordinates to move object along the x-axis.
            dy (int): Distance in tile map coordinates to move object along the y-axis.

        """

        # boolean to check if a tile is a wall
        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path is True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            # player or a confused creature (not normal ai)can hurt anyone
            if self.owner is PLAYER or self.owner.ai.hurt_kin is True:
                self.attack(target)

            # creatures can only harm the player and not their kin
            elif self.owner is not PLAYER and target is PLAYER:
                self.attack(PLAYER)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):
        """Attacks another "target" ObjActor object.

        Uses the take_damage() method in this ComCreature class to implement harming of target. Will display a game
        message indicating how much damage the creature did to the target. The damage dealt to the target is influenced
        by the power and defence properties.

        Args:
            target (ObjActor): Target actor object (that also contains a creature component)to be attacked and harmed.

        Returns:

        """

        damage_dealt = self.power - target.creature.defence

        # naming convention for attack message
        # (PLAYER will only display nickname, creatures display nickname and creature type)
        if target is PLAYER:
            victim_name = target.creature.name_instance
        else:
            victim_name = target.display_name

        if self.owner is PLAYER:
            attacker_name = self.name_instance
        else:
            attacker_name = self.owner.display_name

        if damage_dealt > 0 and self.owner is PLAYER:
            pygame.mixer.Sound.play(random.choice(ASSETS.sfx_hit_punch_list))

        # attack message
        attack_msg = "{} attacks {} for {} damage!".format(attacker_name, victim_name, damage_dealt)
        game_message(attack_msg, constants.COLOR_WHITE)

        # target creature takes damage
        target.creature.take_damage(damage_dealt)

    def take_damage(self, damage):
        """Applies damage amount to current_hp.

        Decreases current_hp of self and displays a game message indicating how much health remains. The name displayed
        is different for PLAYER and other creatures. Runs death_function specified in the initialization of the creature
        object when health falls to 0 or below.

        Args:
            damage (int): Amount of damage to be taken away from current_hp of self.

        """

        self.current_hp -= damage

        if self.owner is not PLAYER:
            msg_color = constants.COLOR_ORANGE

            if self.current_hp < 0:
                damage_taken = "{}'s health is 0/{}".format(self.owner.display_name, self.maxHp)
            else:
                damage_taken = "{}'s health is {}/{}".format(self.owner.display_name, self.current_hp, self.maxHp)

        elif self.owner is PLAYER:
            msg_color = constants.COLOR_RED

            if self.current_hp < 0:
                damage_taken = "{}'s health is 0/{}".format(self.name_instance, self.maxHp)
            else:
                damage_taken = "{}'s health is {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

        game_message(damage_taken, msg_color)

        if self.current_hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, amount):
        """Applies health to creature's current_hp.

        Increases current_hp of self and displays a game message indicating the amount healed and another game message
        indicating the current health of the creature. Makes sure that the current_hp of creature does not go past its
        maximum health.

        Args:
            amount (int): Amount of health to be regained.

        """

        hp_before_heal = self.current_hp
        self.current_hp += amount

        if self.current_hp <= self.maxHp:
            healed_amt_msg = "{} healed for {}".format(self.name_instance, amount)
            curr_hp_msg = "{}'s health is now {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

            game_message(healed_amt_msg, constants.COLOR_GREEN)
            game_message(curr_hp_msg, constants.COLOR_WHITE)

        # when healing gave creature more hp than max hp
        elif self.current_hp > self.maxHp:
            actual_healed_amt = self.maxHp - hp_before_heal
            self.current_hp = self.maxHp

            healed_amt_msg = "{} healed for {}".format(self.name_instance, actual_healed_amt)
            curr_hp_msg = "{}'s health is now {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

            game_message(healed_amt_msg, constants.COLOR_GREEN)
            game_message(curr_hp_msg, constants.COLOR_WHITE)

    @property
    def power(self):
        """A property that calculates and returns the current total power of the creature.

        Adds base_atk and all attack bonuses currently available to the creature (equipped items, etc.) to its
        total power.

        Returns:
            total_power (int): The current total power of the creature (including base and bonuses)

        """
        total_power = self.base_atk

        if self.owner.container:
            equipment_power_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_items]

            for power_bonus in equipment_power_bonuses:
                total_power += power_bonus

        return total_power

    @property
    def defence(self):
        """A property that calculates and returns the current total defence of the creature.

        Adds base_def and all defence bonuses currently available to the creature (equipped items, etc.) to its
        total defence.

        Returns:
            total_defence (int): The current total defence of the creature (including base and bonuses)

        """
        total_defence = self.base_def

        if self.owner.container:
            equipment_defence_bonuses = [obj.equipment.defence_bonus for obj in self.owner.container.equipped_items]

            for def_bonus in equipment_defence_bonuses:
                total_defence += def_bonus

        return total_defence


class ComItem:
    """Item component gives actor objects the property of being picked up and used.

    Attributes:
        weight (arg, float): The weight of the object with precision of one decimal point.
        volume (arg, float): The volume of the object with precision of one decimal point.
        use_function (arg, func): Optional argument that specifies the function to be executed when an item object is
                                  used. These use functions have the form use_function(target/caster, value).
        value (arg, int or tuple): Optional argument that gives the value to be passed into the use_function.

    """

    def __init__(self, weight=0.0,
                 volume=0.0,
                 use_function=None,
                 value=None):

        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
        self.container = None
        # self.owner = self.owner

    def pick_up(self, actor):
        """Picks up the item object and places it into specified actor's container inventory.

        Appends item to actor's inventory (list) in its container component and removes the items from the list of
        current_objects in GAME (ObjGame). Displays appropriate messages indicating whether the item can be picked up.
        This method is linked to the keyboard shortcut key "g".

        Args:
            actor (ObjActor): The actor that is picking up the item (the actor object with a container component
                              that the item will append itself).

        """

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room to pick up", constants.COLOR_WHITE)

            else:
                game_message("Picking up [{}]".format(self.owner.name_object))
                actor.container.inventory.append(self.owner)

                self.owner.animation_del()

                GAME.current_objects.remove(self.owner)      # remove from global map and list of objects in the game
                self.container = actor.container

    def drop(self, new_x, new_y):
        """Drops the item object onto the ground specified by the coordinate arguments.

        Removes the item object from the actor's inventory that the item is being contained in and places it into the
        GAME's current_object list. Displays a game message indicating which object has been dropped.

        Args:
            new_x (int): The x-coord on the map to drop the item (usually PLAYER's current position).
            new_y (int): The y-coord on the map to drop the item (usually PLAYER's current position).

        Returns:
            A game message that says the item is dropped.

        """

        # inserting at the front of the list to make sure that it is drawn underneath any creature or PLAYER
        GAME.current_objects.insert(0, self.owner)

        self.owner.animation_init()

        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game_message("Dropped [{}]".format(self.owner.name_object))

    def use(self):
        """Uses the item to produce an effect and removes it from the inventory.

        Passes in the caster (the creature/actor using the item) and the value associated with the use_function.
        Removes the used item from the inventory that it was held in. Prints error message to console if an error
        occurred when executing the use_function.

        """

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:

            # self.owner would be the item itself.
            # However, self.container, which was initialized in the pick_up(actor) method, is related to the actor
            # holding the item.

            result = self.use_function(self.container.owner, self.value)
            if result != "unused":
                self.container.inventory.remove(self.owner)


class ComContainer:
    """Container component gives actor objects an inventory that can hold item objects.

    Attributes:
        inventory (arg, list): Optional argument that initializes a list of ObjActor with the item component. Default
                               list is empty.
        max_volume (arg, float): Optional argument that specifies the maximum volume of the container. Default value is
                                 initialized to 10.0.

    Todo:
        * Implement a method that gets the names of every item in the inventory.
        * Implement a method that gets the weight of every item in the inventory.
        * Implement a system if method for weight and volume use.

    """

    def __init__(self, volume=10.0, inventory=[]):
        self.inventory = inventory
        self.max_volume = volume    # further usage of this in the future for more strategic and robust inventory system

    # TODO: Get Names of everything in inventory

    # Get volume within container
    @property
    def volume(self):
        """Gets the current total volume of the container.

        Returns:
            total_volume (float): The total volume that the current items in the inventory sum up to.

        """

        total_volume = 0.0

        return total_volume

    @property
    def equipped_items(self):
        """Gives a list of all equipped items on the character.

        Returns:
             list_of_equipped_items (list): list of all equipment items in the inventory that have their equipped
             attribute set to True.

        """

        list_of_equipped_items = [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped is True]

        return list_of_equipped_items

    # TODO: Get weight of everything in inventory


class ComEquipment:
    """Equipment component gives actor objects item component properties as well as extra combat bonuses and statuses.

    Equipments are a component of actor objects, but also contain the item component (see ObjActor initialization).

    Attributes:
        attack_bonus (arg, int): Optional argument that specifies the attack bonus of the equipment. Default value is
                                 initialized to 0.
        defence_bonus (arg, int): Optional argument that specifies the defence bonus of the equipment. Default value is
                                  initialized to 0.
        slot (arg, str): Indicates the slot that the equipment should occupy
                        (currently only "Right Hand" and "Left Hand").

    """

    def __init__(self, attack_bonus=0, defence_bonus=0, slot=None):   # might need to delete None initialization of slot

        self.attack_bonus = attack_bonus
        self.defence_bonus = defence_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):
        """Toggles and sets equipment's status attribute "equipped".

        """

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        """Equips the item and sets the equipped attribute to True.

        Checks the slot of the equipment to see if that particular slot is already occupied. Display appropriate game
        messages to PLAYER. If the slot is empty, set equipped attribute to true.

        Returns:
            A game message indicating player of equipment status of the object or any problems when attempting to equip.

        """

        # check for equipment in the corresponding slot
        all_equipped_items = self.owner.item.container.equipped_items

        if all_equipped_items:  # do check only if there are equipped items on already, if not, equip as normal
            for equipped_item in all_equipped_items:
                if equipped_item.equipment.slot == self.slot:
                    game_message("There is already an item in the {} slot!".format(self.slot), constants.COLOR_WHITE)
                    return

        self.equipped = True
        game_message("Equipped [{}] in the {} slot".format(self.owner.name_object, self.slot))

    def unequip(self):
        """Unequips the item and sets the equipped attribute to False.

        Display a game messages to PLAYER indicating the equipment has been unequipped.

        Returns:
            A game message indicating the equipment has been unequipped.

        """
        self.equipped = False

        game_message("Unequipped [{}]".format(self.owner.name_object))


class ComStairs:
    """Stairs component that is defaulted to lead the player up to the next floor.

    Attributes:
        upwards (arg, bool): Specifies whether it should take the player up/to the next map. Default set to True.
                             False would mean stairs lead down and to the previous map.

    """

    def __init__(self, upwards=True):
        self.upwards = upwards

    def use(self):
        """Implements map transitioning when called.

        When only upwards attribute is set to True, the player progresses to the next map. Otherwise, the player goes
        to the previous map.

        TODO:  Possibly implement "locking" the player in until a task is done (rendering stairs unusable).

        Returns:
            None

        """

        if self.upwards:
            GAME.map_transition_next()

        else:
            GAME.map_transition_prev()


# ================================================================= #
#                    -----  Ai Components  -----                    #
#                          --- SECTION ---                          #
# ================================================================= #


class AiConfuse:
    """Ai component class that makes a creature actor walk in random directions.

    Attributes:
        original_ai (arg, Ai class): The ai component the actor had originally before being set to AiConfuse.
        num_turns (arg, int): The number of turns it takes before the affected creature's ai is reset to original_ai.
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to True.

    """

    def __init__(self, original_ai, num_turns):
        self.original_ai = original_ai
        self.num_turns = num_turns
        self.hurt_kin = True

    def take_turn(self):
        """Performs one move action towards a random direction/tile.

        Resets the affected creature's ai to its previous (normal) ai after num_turns have been exhausted to 0.

        Returns:
            Displays a game message when the creature actor has broken free of this AiConfuse.

        """

        if self.num_turns > 0:
            # default (0) random gen
            self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

            self.num_turns -= 1

        # reset creature's ai
        else:
            self.owner.ai = self.original_ai
            game_message("{} has broken out of its confusion!".format(self.owner.display_name), constants.COLOR_YELLOW)


class AiChase:
    """Ai component class for enemy creatures that chases the PLAYER and attacks when the it is next to the PLAYER.

    Attributes:
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to False.

    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action towards the PLAYER's current location when the creature is in the PLAYER's fov.

        When the creature is adjacent to the PLAYER, attack. Prevents creatures from hurt other creatures when moving
        towards PLAYER together (implemented in the move() method of ComCreature).

        """

        monster = self.owner

        # when the monster creature is in the field of vision of the player
        if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

            # move towards player
            if monster.distance_to(PLAYER) >= 2:
                monster.move_towards(PLAYER)

            else:
                monster.creature.attack(PLAYER)


class AiFlee:
    """Ai component class for enemy creatures that chases the PLAYER and attacks when the it is next to the PLAYER.

    Attributes:
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to False.

    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action towards the PLAYER's current location when the creature is in the PLAYER's fov.

        When the creature is adjacent to the PLAYER, attack. Prevents creatures from hurt other creatures when moving
        towards PLAYER together (implemented in the move() method of ComCreature).

        """

        monster = self.owner

        # when the monster creature is in the field of vision of the player
        if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

            # move away from player
            monster.move_away(PLAYER)



# ================================================================= #
#                   -----  Death Functions -----                    #
#                          --- SECTION ---                          #
# ================================================================= #

def death_snake_monster(monster):
    """Death_function for dead snake creatures.

    Creature stops moving, loses its creature component and its idle animation becomes a still piece of snake flesh.

    Args:
        monster (ObjActor): The actor creature object that will execute this death function when it dies.

    """

    death_msg = "{} is dead!".format(monster.display_name)
    # death_msg = monster.creature.name_instance + " is dead!"
    game_message(death_msg, constants.COLOR_WHITE)

    monster.animation_key = "S_FLESH_SNAKE"
    monster.animation = ASSETS.animation_dict[monster.animation_key]

    monster.creature = None
    monster.ai = None


def death_healer_monster(monster):
    """Death_function for dead healing creatures.

    Creature stops moving, loses its creature component and its idle animation becomes a still piece of healing item.

    Args:
        monster (ObjActor): The actor creature object that will execute this death function when it dies.

    """

    death_msg = "{} is dead and dropped a healing element!".format(monster.display_name)
    game_message(death_msg, constants.COLOR_GREEN)

    monster.animation_key = "S_WATER_CUP"
    monster.animation = ASSETS.animation_dict[monster.animation_key]
    monster.name_object = "Water Cup"

    monster.creature = None
    monster.ai = None


# ================================================================= #
#                         -----  Map  -----                         #
#                          --- SECTION ---                          #
# ================================================================= #

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
    new_map = [[StructTile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

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

            # place the PLAYER inside the center of the very first of room of this map
            if len(list_of_rooms) != 0:
                previous_room = list_of_rooms[-1]

                map_create_tunnels(new_map, new_room.center, previous_room.center)

            list_of_rooms.append(new_room)

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

    top_level = (len(GAME.maps_prev) == 0)

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
            PLAYER.x, PLAYER.y = room.center

        # only generate enemies in the rooms that the player doesnt start in
        if not first_room:
            gen_enemy((enemy_x, enemy_y))

        # only generate stairs leading down in the first room if the map is not the top level
        if first_room and not top_level:
            gen_stairs((PLAYER.x, PLAYER.y), up=False)

        # generate stairs leading up in the last room
        if last_room:
            gen_stairs(room.center)

        item_x = PLAYER.x
        item_y = PLAYER.y

        # items are not allowed to span on top of player's spawn point
        while (item_x, item_y) == (PLAYER.x, PLAYER.y):
            item_x = tcod.random_get_int(0, min_x, max_x)
            item_y = tcod.random_get_int(0, min_y, max_y)

        gen_item((item_x, item_y))


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
        for obj in GAME.current_objects:
            if (obj is not exclude_object and
                obj.x == coords_x and
                obj.y == coords_y and
                obj.creature):

                target = obj

            if target:
                return target

    else:
        # check object list to find any creature at that location (eg. confuse spell hurting themselves)
        for obj in GAME.current_objects:
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
    global FOV_MAP

    FOV_MAP = tcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    # for every cell, set the properties
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            tcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
    """Calculates the fov based on the PLAYER's position on the map.

    Only calculates the fov when the global variable FOV_CALCULATE is True.

    Returns:
        None
    """
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False   # prevent calculating fov every frame, if standing still
        tcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                             constants.FOV_ALG)


def map_object_at_coords(coords_x, coords_y):
    """Check if there is an object at the specified x, y coordinates.

    Args:
        coords_x (int): x coordinate of tile to be checked for creatures.
        coords_y (int): y coordinate of tile to be checked for creatures.

    Returns:
        object_options (List): List of all actor objects at specified coordinates.

    """

    object_options = [obj for obj in GAME.current_objects if obj.x == coords_x and obj.y == coords_y]

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


# ================================================================= #
#                        -----  Draw  -----                         #
#                          --- SECTION ---                          #
# ================================================================= #

def draw_game():
    """Main function for drawing the entire game.

    Order of draw operations:
        1) Clear the screen window and map Surface
        2) Update the camera position
        3) Draw the map Surface
        4) Draw all appropriate actor objects onto the map Surface
        5) Render the map Surface onto the screen window
        5) Draw the debug fps message in the top-left corner of the screen window
        6) Draw the player messages on the screen window

    Returns:
        None

    """

    # clear the surface (filling it with some color, wipe the color out)
    SURFACE_MAIN.fill(constants.COLOR_BLACK)
    SURFACE_MAP.fill(constants.COLOR_BLACK)

    CAMERA.update_pos()

    # draw the map Surface
    draw_map(GAME.current_map)

    # draw the character
    for obj in GAME.current_objects:
        obj.draw()

    # Display map onto main game screen window
    SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

    # Draw fps message
    draw_debug()

    # Draw all player interactive messages
    draw_messages()


def draw_map(map_to_draw):
    """ Draws specified map onto the main SURFACE_MAP map Surface.

    Only renders the camera area of the map to prevent performance loss when exploring large maps.

    Args:
        map_to_draw (2D array): Map to be drawn onto SURFACE_MAP.

    Returns:
        None

    """

    # render only the visible portion of the map
    cam_tile_x, cam_tile_y = CAMERA.map_address

    window_tile_width = int(constants.CAMERA_WIDTH / constants.CELL_WIDTH)
    window_tile_height = int(constants.CAMERA_HEIGHT / constants.CELL_HEIGHT)

    render_min_x = int(cam_tile_x - (window_tile_width / 2))
    render_min_y = int(cam_tile_y - (window_tile_height / 2))

    render_max_x = int(cam_tile_x + (window_tile_width / 2))
    render_max_y = int(cam_tile_y + (window_tile_height / 2))

    if render_min_x < 0:
        render_min_x = 0
    if render_min_y < 0:
        render_min_y = 0
    if render_max_x > constants.MAP_WIDTH:
        render_max_x = constants.MAP_WIDTH
    if render_max_y > constants.MAP_HEIGHT:
        render_max_y = constants.MAP_HEIGHT

    for x in range(render_min_x, render_max_x):
        for y in range(render_min_y, render_max_y):

            is_visible = tcod.map_is_in_fov(FOV_MAP, x, y)      # to check whether or not a tile is visible

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path is True:
                    SURFACE_MAP.blit(ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                else:
                    SURFACE_MAP.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            else:
                if map_to_draw[x][y].explored:
                    if map_to_draw[x][y].block_path is True:
                        SURFACE_MAP.blit(ASSETS.S_WALL_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

                    else:
                        SURFACE_MAP.blit(ASSETS.S_FLOOR_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            # else if not visible:
                # the background fill color of the surface being drawn on is displayed (black at the moment)


def draw_debug():
    """Draws the debug console onto the game screen window.

    Draws debug message text to the upper left corner of the screen.
    Displays only the current FPS for now.

    Returns:
        None

    """

    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), constants.FONT_BEST, (0, 0),
              constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_messages():
    """Draws the message console to the game screen window.

    Displays a max number of messages from the game's list of messages stored in GAME.message_history in sequence to
    the lower left corner of the screen. The order of messages starts at the bottom with the most recent message.

    Returns:
        None

    """
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        GAME.message_history = GAME.message_history   # the last 4 messages in the list
    else:
        del GAME.message_history[0]
        # GAME.message_history = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(constants.FONT_BEST)
    start_y = constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)

    for i, (message, color) in enumerate(GAME.message_history):

        draw_text(SURFACE_MAIN, message, constants.FONT_BEST, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)


def draw_text(display_surface, text_to_display, font, t_coords, text_color, back_color=None, center=False):
    """ Displays text to the specified Surface.

    Args:
        display_surface (pygame.Surface):
        text_to_display (str):
        font (pygame.font.Font):
        t_coords (tuple):
        text_color(tuple):
        back_color (tuple):
        center (bool):

    Returns:
        None

    """

    text_surf, text_rect = helper_text_objects(text_to_display, font, text_color, back_color)

    if not center:
        text_rect.topleft = t_coords
    else:
        text_rect.center = t_coords

    display_surface.blit(text_surf, text_rect)


def draw_tile_rect(display_surface, tile_coords, color, alpha=150, mark=None):

    x, y = tile_coords

    # convert map tile coordinates into actual pixel map addresses for proper blitting
    map_x = x * constants.CELL_WIDTH
    map_y = y * constants.CELL_HEIGHT

    # Create a rectangular image/Surface object that's the size of one tile (cell)
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    # fill the Surface with a solid color
    new_surface.fill(color)

    # Draw pixels of this Surface slightly transparent according to value (0 being transparent and 255 being opaque)
    new_surface.set_alpha(alpha)

    if mark:
        draw_text(new_surface, mark, constants.FONT_TARGET_X,
                  (constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2),
                  constants.COLOR_BLACK, center=True)

    display_surface.blit(new_surface, (map_x, map_y))


# ================================================================= #
#                        -----  Helper  -----                       #
#                          --- SECTION ---                          #
# ================================================================= #

def helper_text_objects(incoming_text, font, incoming_color, incoming_bg):

    if incoming_bg:
        text_surface = font.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = font.render(incoming_text, False, incoming_color)  # constants.FONT_BEST

    return text_surface, text_surface.get_rect()


def helper_text_height(font):
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height       # return font's height in pixels


def helper_text_width(font, text):
    font_object = font.render(text, False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.width

# ================================================================= #
#                        -----  Magic  -----                        #
#                          --- SECTION ---                          #
# ================================================================= #


def cast_heal(target, value):
    if target.creature.current_hp == target.creature.maxHp:
        full_hp_msg = target.creature.name_instance + " is already at full health!"
        game_message(full_hp_msg, constants.COLOR_BLUE)
        return "Already full health!"

    else:
        target.creature.heal(value)
    return None


def cast_lightening(caster, tup_dmg_range):

    # might set this from a parameter in the future if enemies, other creatures other than the PLAYER uses this spell
    caster_location = (caster.x, caster.y)

    damage, max_r = tup_dmg_range

    # prompt player for a target tile
    selected_tile_address = menu_tile_select(coords_origin=caster_location,
                                             max_range=max_r,
                                             wall_penetration=False)

    # continue with casting of spell only if caster did not "cancel" the spell (by escaping from menu_tile_select)
    if selected_tile_address:
        game_message("{} casts lightening".format(caster.creature.name_instance),
                     constants.COLOR_WHITE)

        # convert tile into a list of coords between a and b
        list_of_tiles_affected = map_find_line(caster_location, selected_tile_address)

        # cycle through list and damage everything in that list
        for i, (x, y) in enumerate(list_of_tiles_affected):
            target_creature = map_check_for_creatures(x, y)

            if target_creature and i != 0:
                target_creature.creature.take_damage(damage)

    else:
        return "unused"


def cast_fireball(caster, tup_dmg_range_radius):

    damage, spell_range, spell_radius = tup_dmg_range_radius

    # caster is the one holding the spell
    caster_location = (caster.x, caster.y)

    # prompt player for a target tile
    selected_tile_address = menu_tile_select(coords_origin=caster_location,
                                             max_range=spell_range,
                                             radius=spell_radius,
                                             wall_penetration=False,
                                             creature_penetration=False)
    # get sequence of tiles
    if selected_tile_address:
        game_message("{} casts fireball".format(caster.creature.name_instance),
                     constants.COLOR_WHITE)

        list_of_tiles_to_damage = map_find_radius(selected_tile_address, spell_radius)

        # damage all creatures in tiles
        for (x, y) in list_of_tiles_to_damage:
            target_creature = map_check_for_creatures(x, y)

            if target_creature:
                target_creature.creature.take_damage(damage)

    else:
        return "unused"


def cast_confusion(caster, effect_length):

    # prompt player for a target tile
    selected_tile_address = menu_tile_select(wall_penetration=False)

    # get target
    if selected_tile_address:

        target_tile_x, target_tile_y = selected_tile_address

        target_creature = map_check_for_creatures(target_tile_x, target_tile_y)

        if target_creature:
            game_message("{} casts confusion on {}".format(caster.creature.name_instance, target_creature.display_name),
                         constants.COLOR_WHITE)

            normal_ai = target_creature.ai

            target_creature.ai = AiConfuse(original_ai=normal_ai, num_turns=effect_length)
            target_creature.ai.owner = target_creature

            game_message("{} is now confused!".format(target_creature.display_name), constants.COLOR_GREEN)

    else:
        return "unused"



# ================================================================= #
#                         -----  UI  -----                          #
#                          --- SECTION ---                          #
# ================================================================= #

class UiButton:

    def __init__(self, surface, text, tup_coords_center, tup_size,
                 color_button_hovered=constants.COLOR_GREEN,
                 color_button_default=constants.COLOR_BLUE,
                 color_text_hovered=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_GREY):

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

    def update(self, mouse_input):

        button_clicked = False
        mouse_clicked = False

        mouse_x, mouse_y = mouse_input
        pygame.event.get()

        if pygame.mouse.get_pressed()[0]:
            mouse_clicked = True

        mouse_hovered = (self.button_rect.left <= mouse_x <= self.button_rect.right and
                         self.button_rect.top <= mouse_y <= self.button_rect.bottom)

        if mouse_hovered:
            self.color_button_current = self.color_button_hovered
            self.color_text_current = self.color_text_hovered

        else:
            self.color_button_current = self.color_button_default
            self.color_text_current = self.color_text_default

        if mouse_hovered and mouse_clicked:
            button_clicked = True

        return button_clicked


    def draw(self):
        pygame.draw.rect(self.surface, self.color_button_current, self.button_rect)

        draw_text(self.surface, self.text, constants.FONT_BEST, self.coords_center,
                  self.color_text_current, self.color_button_current, center=True)


# ================================================================= #
#                         -----  Menu  -----                        #
#                          --- SECTION ---                          #
# ================================================================= #

def menu_main():
    game_initialize()
    menu_running = True

    # tile address
    center_x = constants.CAMERA_WIDTH / 2
    title_y = constants.CAMERA_HEIGHT / 2 - (constants.CAMERA_HEIGHT/4)

    # button sizes
    button_width = 150
    button_height = 30
    button_offset_y = 5/4 * button_height

    # button address
    new_game_button_y = title_y + constants.CAMERA_HEIGHT/5
    cont_button_y = new_game_button_y + button_offset_y
    options_button_y = cont_button_y + button_offset_y
    quit_button_y = options_button_y + button_offset_y

    # buttons
    new_game_button = UiButton(SURFACE_MAIN, "NEW GAME",
                            (center_x, new_game_button_y),
                            (button_width, button_height))

    cont_button = UiButton(SURFACE_MAIN, "CONTINUE",
                           (center_x, cont_button_y),
                           (button_width, button_height))

    options_button = UiButton(SURFACE_MAIN, "OPTIONS",
                              (center_x, options_button_y),
                              (button_width, button_height))

    quit_button = UiButton(SURFACE_MAIN, "QUIT",
                           (center_x, quit_button_y),
                           (button_width, button_height))

    # draw menu background and title
    SURFACE_MAIN.blit(ASSETS.S_MAIN_MENU, (0, 0))
    draw_text(SURFACE_MAIN, "Tower of Rak",
              constants.FONT_GAME_TILE,
              (center_x, title_y),
              constants.COLOR_RED,
              center=True)

    # play background music
    pygame.mixer.music.load(ASSETS.main_menu_music)
    pygame.mixer.music.play(-1)

    while menu_running:

        # process inputs
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        for event in events_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # start new game if clicked
        if new_game_button.update(mouse_pos):
            pygame.mixer.music.fadeout(3000)
            game_new()
            game_main_loop()

        # load previous game if clicked
        if cont_button.update(mouse_pos):
            pygame.mixer.music.fadeout(3000)
            game_start()

        # display options menu
        if options_button.update(mouse_pos):
            menu_main_options()
            SURFACE_MAIN.blit(ASSETS.S_MAIN_MENU, (0, 0))
            draw_text(SURFACE_MAIN, "Tower of Rak",
                      constants.FONT_GAME_TILE,
                      (center_x, title_y),
                      constants.COLOR_RED,
                      center=True)


        # quit the game
        if quit_button.update(mouse_pos):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        # draw buttons
        new_game_button.draw()
        cont_button.draw()
        options_button.draw()
        quit_button.draw()

        pygame.display.update()


def menu_main_options():
    menu_width = 300
    menu_height = 200
    center_x = constants.CAMERA_WIDTH / 2
    center_y = constants.CAMERA_HEIGHT / 2

    option_menu_surface = pygame.Surface((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
    menu_rect = pygame.Rect((0, 0), (menu_width, menu_height))
    menu_rect.center = (center_x, center_y)

    menu_close = False

    while not menu_close:

        option_menu_surface.fill(constants.COLOR_YELLOW)
        SURFACE_MAIN.blit(option_menu_surface, menu_rect.topleft, menu_rect)

        # get player input
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        pygame.display.update(menu_rect)



def menu_pause():
    """Menu that pauses the game and displays a simple pause message.

    """

    menu_close = False

    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    pause_menu_text = "PAUSED"
    pause_menu_font = constants.FONT_BEST

    pause_text_height = helper_text_height(pause_menu_font)
    pause_text_width = helper_text_width(pause_menu_font, pause_menu_text)

    pause_menu_x = (window_width/2) - (pause_text_width/2)
    pause_menu_y = (window_height/2) - (pause_text_height/2)

    while not menu_close:
        event_list = pygame.event.get()

        draw_text(SURFACE_MAIN, pause_menu_text, pause_menu_font, (pause_menu_x, pause_menu_y),
                  constants.COLOR_WHITE, constants.COLOR_BLACK)

        for event in event_list:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    menu_close = True       # pressing pause button again means break out and unpause game

        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()


def menu_inventory():

    menu_close = False

    # game window dimensions
    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    # menu characteristics
    menu_width = (2/5) * window_width
    menu_height = (2/5) * window_height
    menu_x = (window_width/2) - (menu_width/2)          # number of pixels to the right from the left game window side
    menu_y = (window_height/2) - (menu_height/2)        # number of pixels down from the top game window side
    menu_text_font = constants.FONT_BEST
    menu_text_height = helper_text_height(constants.FONT_BEST)
    menu_text_color = constants.COLOR_WHITE

    local_inventory_menu_surface = pygame.Surface((menu_width, menu_height))
    while not menu_close:

        draw_game()

        # Clear the menu
        local_inventory_menu_surface.fill(constants.COLOR_GREY)

        # mouse control inside menu
        mouse_x, mouse_y = pygame.mouse.get_pos()  # gets mouse position coordinates relative to game window
        mouse_rel_x = mouse_x - menu_x      # mouse position relative to the menu
        mouse_rel_y = mouse_y - menu_y
        mouse_in_menu = (0 < mouse_rel_x < menu_width and
                         0 < mouse_rel_y < menu_height)

        mouse_line_selection = int(mouse_rel_y/menu_text_height)   # starting from 0, each line of text is an int number

        # for testing
        # if mouse_in_menu:
            # print(mouse_line_selection)

        # Register changes (draw text on the local_inventory_menu_surface)
        print_list = [obj.display_name for obj in PLAYER.container.inventory]    # list comprehension

        for line, name in enumerate(print_list):
            if mouse_in_menu and line == mouse_line_selection:
                draw_text(local_inventory_menu_surface, name, menu_text_font, (0, 0 + (line * menu_text_height)),
                          constants.COLOR_BLACK, constants.COLOR_WHITE)
            else:
                draw_text(local_inventory_menu_surface, name, menu_text_font, (0, 0 + (line * menu_text_height)),
                          menu_text_color)

        # draw menu
        SURFACE_MAIN.blit(local_inventory_menu_surface,
                          (menu_x, menu_y))

        # get list of events input
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:    # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    if mouse_in_menu and mouse_line_selection + 1 <= len(print_list):

                        # exit out of inventory menu if using an item
                        # stay inside inventory menu if putting on equipment
                        if not PLAYER.container.inventory[mouse_line_selection].equipment:
                            menu_close = True

                        # use or equip the item
                        PLAYER.container.inventory[mouse_line_selection].item.use()

        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()   # pygame.display.update() does the same thing if given without any arguments


def menu_tile_select(coords_origin=None,
                     max_range=None,
                     radius=None,
                     wall_penetration=True,
                     creature_penetration=True):
    """Enables the player to select a tile on the map.

    This function will produce a rectangular indication when the mouse is hovered over a tile. When the player
    left-clicks the selected tile, the map address will be returned for use in other functions like spells.

    Returns:
         Map address of the selected tile when the player left-clicks the mouse button.

    """

    menu_close = False

    while not menu_close:

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # convert mouse window address to map pixel address
        map_x_pixel, map_y_pixel = CAMERA.window_to_map((mouse_x, mouse_y))

        # convert to map tile address
        map_tile_x = int(map_x_pixel/constants.CELL_WIDTH)
        map_tile_y = int(map_y_pixel/constants.CELL_HEIGHT)



        if coords_origin:
            list_of_tiles = map_find_line(coords_origin, (map_tile_x, map_tile_y))

            # deal with "valid" tiles
            for i, (tile_x, tile_y) in enumerate(list_of_tiles):

                # stop at max_range
                if max_range and i == max_range:
                    # only take the map address tuples before the range
                    list_of_tiles = list_of_tiles[:i+1]

                # stop at wall
                if not wall_penetration:
                    # boolean checking if the tile is a wall or not (True if it is, False if not)
                    tile_is_wall = GAME.current_map[tile_x][tile_y].block_path is True
                    if tile_is_wall:
                        list_of_tiles = list_of_tiles[:i]

                # stop at first creature encountered
                # same as slicing used above but slightly faster truncation method with deletion
                if not creature_penetration:
                    target_creature = map_check_for_creatures(tile_x, tile_y)
                    if target_creature and target_creature is not PLAYER:
                        del list_of_tiles[i+1:]

        else:
            list_of_tiles = [(map_tile_x, map_tile_y)]

        # Get events
        event_list = pygame.event.get()
        for event in event_list:
            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

            # mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:    # left-click is 1, right is 3, scroll up is 4 and down is 5

                # return the last map tile address within the valid list of tiles
                if event.button == 1:

                    if (map_tile_x, map_tile_y) == list_of_tiles[-1]:
                        return map_tile_x, map_tile_y

                    # or maybe tell player that they must click on a tile that is within the range, etc.
                    else:
                        return list_of_tiles[-1]

        # Draw game
        # clear the surface (filling it with some color, wipe the color out)
        SURFACE_MAIN.fill(constants.COLOR_BLACK)
        SURFACE_MAP.fill(constants.COLOR_BLACK)

        CAMERA.update_pos()

        # draw the map
        draw_map(GAME.current_map)

        # draw the character
        for obj in GAME.current_objects:
            obj.draw()

        # draw area of affect with the correct radius
        if radius:
            area_of_effect = map_find_radius(list_of_tiles[-1], radius)
            target_tile = list_of_tiles[-1]

            # prevent tiles to be highlighted twice (as it changes the opaqueness of the highlight)
            for (tile_x, tile_y) in area_of_effect:
                target_creature = map_check_for_creatures(tile_x, tile_y)

                for x, y in list_of_tiles:
                    if (tile_x, tile_y) == (x, y):
                        list_of_tiles.remove((x, y))

                # highlight tile in red if tile contains a monster
                if target_creature:
                    # mark target with an "X"
                    if (tile_x, tile_y) == target_tile:
                        draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED, alpha=200, mark="X")

                    else:
                        draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED, alpha=150)

                # highlight anything else (walls, floor, items) in pale yellow
                else:
                    # mark target with an "X"
                    if (tile_x, tile_y) == target_tile:
                        draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=200, mark="X")
                    else:
                        draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_ORANGE, alpha=100)

        # Draw rectangle at mouse position over game visuals
        for (tile_x, tile_y) in list_of_tiles:

            # mark target with an "X"
            if (tile_x, tile_y) == list_of_tiles[-1] and not radius:
                draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=200, mark="X")

            target_creature = map_check_for_creatures(tile_x, tile_y)

            # highlight tile in red if tile contains a monster
            if target_creature and target_creature is not PLAYER:
                draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_RED)

            # no highlight of tile if tile is PLAYER (setting transparency to max)
            elif target_creature is PLAYER:
                draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=0)

            # highlight anything else (walls, floor, items) in white
            else:
                draw_tile_rect(SURFACE_MAP, (tile_x, tile_y), constants.COLOR_WHITE, alpha=150)

        # next half of draw_game()
        SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

        draw_debug()
        draw_messages()

        pygame.display.flip()  # pygame.display.update() does the same thing if given without any arguments

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)


# ================================================================= #
#                      -----  Generator  -----                      #
#                          --- SECTION ---                          #
# ================================================================= #

# ---> PLAYER
def gen_player(tup_coords):
    global PLAYER

    x, y = tup_coords

    container_com = ComContainer()
    creature_com = ComCreature("Rak", base_atk=3)

    PLAYER = ObjActor(x, y, "Alligator",
                      "A_PLAYER",
                      animation_speed=1,
                      creature=creature_com,
                      container=container_com)

    GAME.current_objects.append(PLAYER)


# ---> ITEMS
def gen_item(tup_coords):
    """Generates a random item at the given coordinates specified by tup_coords.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated item.

    Returns:
         Inserts a randomly generated item object onto the front of the GAME.current_objects list.

    """

    choice_num = tcod.random_get_int(0, 1, 5)

    if choice_num == 1:
        new_item = gen_scroll_lightening(tup_coords)
    elif choice_num == 2:
        new_item = gen_scroll_fireball(tup_coords)
    elif choice_num == 3:
        new_item = gen_scroll_confusion(tup_coords)
    elif choice_num == 4:
        new_item = gen_weapon_sword(tup_coords)
    elif choice_num == 5:
        new_item = gen_armour_shield(tup_coords)

    GAME.current_objects.insert(0, new_item)


def gen_scroll_lightening(tup_coords):

    x, y = tup_coords

    damage = tcod.random_get_int(0, 3, 5)
    max_r = tcod.random_get_int(0, 7, 8)

    item_com = ComItem(use_function=cast_lightening, value=(damage, max_r))

    lightening_scroll_obj = ObjActor(x, y, "Lightening Scroll",
                                     "S_SCROLL_1",
                                     item=item_com)

    return lightening_scroll_obj


def gen_scroll_fireball(tup_coords):
    x, y = tup_coords

    damage = tcod.random_get_int(0, 2, 4)
    max_r = tcod.random_get_int(0, 7, 8)
    radius = 1

    item_com = ComItem(use_function=cast_fireball, value=(damage, max_r, radius))

    fireball_scroll_obj = ObjActor(x, y, "Fireball Scroll",
                                   "S_SCROLL_2",
                                   item=item_com)

    return fireball_scroll_obj


def gen_scroll_confusion(tup_coords):
    x, y = tup_coords

    effect_len = tcod.random_get_int(0, 5, 7)

    item_com = ComItem(use_function=cast_confusion, value=effect_len)

    confusion_scroll_obj = ObjActor(x, y, "Confusion Scroll",
                                    "S_SCROLL_3",
                                    item=item_com)

    return confusion_scroll_obj


def gen_weapon_sword(tup_coords):
    x, y = tup_coords

    bonus = tcod.random_get_int(0, 1, 2)

    equipment_com = ComEquipment(attack_bonus=bonus, slot="Right Hand")

    sword_obj = ObjActor(x, y, "Small Sword",
                         "S_32_SWORD",
                         equipment=equipment_com)

    return sword_obj


def gen_armour_shield(tup_coords):
    x, y = tup_coords

    bonus = tcod.random_get_int(0, 1, 2)

    equipment_com = ComEquipment(defence_bonus=bonus, slot="Left Hand")

    shield_obj = ObjActor(x, y, "Small Shield",
                          "S_32_SHIELD",
                          equipment=equipment_com)

    return shield_obj


# ---> SPECIAL ITEMS

def gen_stairs(tup_coords, up=True):
    """ Generates a set of stairs going up or down a level/map.

    Args:
        tup_coords (tuple): The map tile coordinates the stairs will be placed.
        up (bool): Specifies if the stairs will lead up or down. Default is set to True, which means stairs going up.

    Returns:
        None

    """

    x, y = tup_coords

    if up:
        stairs_com = ComStairs()
        stairs_obj = ObjActor(x, y, "Upwards stairs",
                                    "S_STAIRS_UP",
                                    stairs=stairs_com)
    else:
        stairs_com = ComStairs(upwards=False)
        stairs_obj = ObjActor(x, y, "Upwards stairs",
                                    "S_STAIRS_DOWN",
                                    stairs=stairs_com)

    GAME.current_objects.insert(0, stairs_obj)


# ---> CREATURES
def gen_enemy(tup_coords):
    """Generates a random enemy at the given coordinates specified by tup_coords.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated enemy creature.

    Returns:
         Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    """

    choice_num = tcod.random_get_int(0, 1, 100)

    if choice_num <= 20:
        new_enemy = gen_snake_cobra(tup_coords)

    else:
        new_enemy = gen_snake_boa(tup_coords)

    if choice_num <= 100:
        new_healer = gen_healer_slime(tup_coords)
        GAME.current_objects.insert(-1, new_healer)

    GAME.current_objects.insert(-1, new_enemy)


def gen_snake_boa(tup_coords):
    x, y = tup_coords

    base_attack = tcod.random_get_int(0, 1, 3)
    max_health = tcod.random_get_int(0, 7, 10)
    creature_name = tcod.namegen_generate("Fantasy male")

    creature_com = ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death_snake_monster)  # base attack is 2
    item_com = ComItem()
    ai_com = AiChase()

    snake_boa_obj = ObjActor(x, y, "Giant Boa",
                             "A_GIANT_BOA",
                             animation_speed=1,
                             creature=creature_com,
                             ai=ai_com,
                             item=item_com)
    return snake_boa_obj


def gen_snake_cobra(tup_coords):
    x, y = tup_coords

    base_attack = tcod.random_get_int(0, 4, 6)
    max_health = tcod.random_get_int(0, 15, 18)
    creature_name = tcod.namegen_generate("Fantasy female")

    creature_com = ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death_snake_monster)    # default base atk is 2
    item_com = ComItem()
    ai_com = AiChase()

    snake_cobra_obj = ObjActor(x, y, "Dark Cobra",
                               "A_COBRA",
                               animation_speed=1,
                               creature=creature_com,
                               ai=ai_com,
                               item=item_com)
    return snake_cobra_obj


def gen_healer_slime(tup_coords):
    x, y = tup_coords

    base_attack = 0
    max_health = 5
    creature_name = tcod.namegen_generate("Fantasy male")

    creature_com = ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death_healer_monster)

    item_com = ComItem(use_function=cast_heal, value=2)
    ai_com = AiFlee()

    healer_zom_obj = ObjActor(x, y, "Healer Slime",
                              "A_HEALER_SLIME",
                              animation_speed=1,
                              creature=creature_com,
                              ai=ai_com,
                              item=item_com)
    return healer_zom_obj


# ================================================================= #
#                         -----  Game  -----                        #
#                          --- SECTION ---                          #
# ================================================================= #


def game_main_loop():
    """Main game loop.

    Draws the game, takes care of any keyboard or mouse events from the player, keeps track of time/turns, and
    quits the game when requested.

    """
    game_quit = False

    # player action definition
    player_action = "no-action"

    while not game_quit:

        # handle player input
        player_action = game_handle_keys()

        map_calculate_fov()

        # quit the game
        if player_action == "QUIT":
            game_exit()

        if player_action != "no-action":     # this is how TURN-BASED is implemented for this game
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)


def game_initialize():
    """Initializes the main game window and other game assets.

    Initializes pygame, the main surface (game window), ObjGame, clock (time tracker), StructAssets, and PLAYER.
    Globalizes important variable constants.

    """

    global SURFACE_MAIN, CLOCK, FOV_CALCULATE, ASSETS, SURFACE_MAP, CAMERA

    # initialize pygame
    pygame.init()
    pygame.key.set_repeat(180, 90)     # (delay, interval) in milliseconds for movement when holding down keys

    # Parse name generation files
    tcod.namegen_parse("data/namegen/jice_fantasy.cfg")

    # displays the pygame window
    SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))  # pygame.RESIZABLE

    # surface of entire map
    SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                  constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    CAMERA = ObjCamera()

    ASSETS = StructAssets()

    CLOCK = pygame.time.Clock()

    FOV_CALCULATE = True


def game_handle_keys():

    global FOV_CALCULATE
    # get player input
    events_list = pygame.event.get()  # list of all events so far (like keys pressed and mouse clicks)
    pressed_key_list = pygame.key.get_pressed()    # list of booleans for whether a key is pressed or not

    # shift pressed
    shift_pressed = (pressed_key_list[pygame.K_RSHIFT] or pressed_key_list[pygame.K_LSHIFT])

    # process input
    for event in events_list:
        # exit game and close entire window when user clicks on the exit (x) button in the top left corner
        if event.type == pygame.QUIT:
            return "QUIT"

        # keyboard events
        if event.type == pygame.KEYDOWN:

            # 'up arrow' key: move player one tile up, hold down to continuing moving automatically
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player moved"

            # 'down arrow' key: move player one tile down, hold down to continuing moving automatically
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player moved"

            # 'left arrow' key: move player one tile to the left, hold down to continuing moving automatically
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player moved"

            # 'right arrow' key: move player one tile to the right, hold down to continuing moving automatically
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player moved"

            # 'g' key: pickup item at the player's current position
            if event.key == pygame.K_g:
                objects_at_player = map_object_at_coords(PLAYER.x, PLAYER.y)
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)

            # 'd' key: drop object from inventory
            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

            # 'p' key: pause the game
            if event.key == pygame.K_p:
                menu_pause()

            # 'i' key: open inventory menu
            if event.key == pygame.K_i:
                menu_inventory()

            if shift_pressed and event.key == pygame.K_PERIOD:

                # check if the player is standing on top of a set of stairs
                list_of_obj = map_object_at_coords(PLAYER.x, PLAYER.y)

                for obj in list_of_obj:

                    # check if the object contains a stairs component
                    if obj.stairs:
                        obj.stairs.use()

            # 'l' key: enable tile selection (for lightening spell)
            # if event.key == pygame.K_l:
                # cast_lightening(5)

            # 'f' key: enable tile selection (for fireball spell)
            # if event.key == pygame.K_f:
                # cast_fireball()

            # 'c' key: enable tile selection (for confuse spell)
            # if event.key == pygame.K_c:
                # cast_confusion()

    return "no-action"


def game_message(game_msg, msg_color=constants.COLOR_GREY):
    new_msg_lines = textwrap.wrap(game_msg, constants.MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(GAME.message_history) == constants.NUM_MESSAGES:
            del GAME.message_history[0]

    GAME.message_history.append((game_msg, msg_color))


def game_new():
    global GAME

    GAME = ObjGame()
    gen_player((0, 0))
    map_place_items_creatures(GAME.current_rooms)


def game_exit():

    # save the game
    game_save()

    pygame.quit()
    sys.exit()


def game_save():

    # destroy Surface object (from actor animations)
    for obj in GAME.current_objects:
        obj.animation_del()

    # write GAME and PLAYER objects into compressed binary file
    with gzip.open("data/saves/savegame", "wb") as save_file:
        pickle.dump([GAME, PLAYER], save_file)


def game_load():

    # since re-assigning these globals
    global GAME, PLAYER

    with gzip.open("data/saves/savegame", "rb") as load_file:
        GAME, PLAYER = pickle.load(load_file)

    # reinitialize animations
    for obj in GAME.current_objects:
        obj.animation_init()

    # create FOV_MAP
    map_make_fov(GAME.current_map)


def game_start():
    # generate a new game or load a game if there is a save data available
    try:
        game_load()

    except:
        print("No saved game data or error loading save data")
        game_new()

    game_main_loop()



if __name__ == '__main__':
    menu_main()
