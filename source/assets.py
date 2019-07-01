# Third party imports
import pygame

# Local project imports
from source import constants
from source import globalvars


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
                         'm': 13, 'n': 14, 'o': 15, 'p': 16,
                         'q': 17, 'r': 18, 's': 19, 't': 20,
                         'u': 21, 'v': 22, 'w': 23, 'x': 24,
                         'y': 25, 'z': 26,
                         'a1': 27, 'b1': 28, 'c1': 29,
                         'd1': 30, 'e1': 31, 'f1': 32, 'g1': 33}    # Thus, (A, 0) will get the upper left corner sprite

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


class ObjAssets:
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
        self.rock = ObjSpriteSheet("data/graphics/Items/Rock.png")


        # ---> Objects folder
        self.wall = ObjSpriteSheet("data/graphics/Objects/Wall.png")
        self.floor = ObjSpriteSheet("data/graphics/Objects/Floor.png")
        self.tile = ObjSpriteSheet("data/graphics/Objects/Tile.png")
        self.door = ObjSpriteSheet("data/graphics/Objects/Door.png")

        # ---> Menu folder
        self.menugui = ObjSpriteSheet("data/graphics/menu/menugui.png")


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

        self.S_WALL_00 = self.wall.get_image('i', 44, 16, 16, (32, 32))[0]
        self.S_WALL_01 = self.wall.get_image('i', 44, 16, 16, (32, 32))[0]
        self.S_WALL_02 = self.wall.get_image('i', 43, 16, 16, (32, 32))[0]
        self.S_WALL_03 = self.wall.get_image('h', 45, 16, 16, (32, 32))[0]
        self.S_WALL_04 = self.wall.get_image('h', 44, 16, 16, (32, 32))[0]
        self.S_WALL_05 = self.wall.get_image('h', 44, 16, 16, (32, 32))[0]
        self.S_WALL_06 = self.wall.get_image('h', 43, 16, 16, (32, 32))[0]
        self.S_WALL_07 = self.wall.get_image('k', 44, 16, 16, (32, 32))[0]
        self.S_WALL_08 = self.wall.get_image('i', 43, 16, 16, (32, 32))[0]
        self.S_WALL_09 = self.wall.get_image('j', 45, 16, 16, (32, 32))[0]
        self.S_WALL_10 = self.wall.get_image('i', 43, 16, 16, (32, 32))[0]
        self.S_WALL_11 = self.wall.get_image('l', 45, 16, 16, (32, 32))[0]
        self.S_WALL_12 = self.wall.get_image('j', 43, 16, 16, (32, 32))[0]
        self.S_WALL_13 = self.wall.get_image('m', 44, 16, 16, (32, 32))[0]
        self.S_WALL_14 = self.wall.get_image('l', 43, 16, 16, (32, 32))[0]
        self.S_WALL_15 = self.wall.get_image('l', 44, 16, 16, (32, 32))[0]

        self.S_WALL_EXPLORED_00 = self.wall.get_image('i', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_01 = self.wall.get_image('i', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_02 = self.wall.get_image('i', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_03 = self.wall.get_image('h', (45+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_04 = self.wall.get_image('h', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_05 = self.wall.get_image('h', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_06 = self.wall.get_image('h', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_07 = self.wall.get_image('k', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_08 = self.wall.get_image('i', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_09 = self.wall.get_image('j', (45+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_10 = self.wall.get_image('i', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_11 = self.wall.get_image('l', (45+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_12 = self.wall.get_image('j', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_13 = self.wall.get_image('m', (44+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_14 = self.wall.get_image('l', (43+3), 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_15 = self.wall.get_image('l', (44+3), 16, 16, (32, 32))[0]

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

        self.S_CREDITS_MENU = pygame.image.load("data/graphics/menu/brown_bg.jpg")
        self.S_CREDITS_MENU = pygame.transform.scale(self.S_CREDITS_MENU, (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

        self.S_TOP_L_MENU_LIGHT = self.menugui.get_image('b1', 8, 16, 16, (32, 32))[0]
        self.S_TOP_R_MENU_LIGHT = self.menugui.get_image('e1', 8, 16, 16, (32, 32))[0]
        self.S_TOP_MENU_LIGHT = self.menugui.get_image('c1', 8, 16, 16, (32, 32))[0]
        self.S_BOT_L_MENU_LIGHT = self.menugui.get_image('b1', 10, 16, 16, (32, 32))[0]
        self.S_BOT_R_MENU_LIGHT = self.menugui.get_image('e1', 10, 16, 16, (32, 32))[0]
        self.S_BOT_MENU_LIGHT = self.menugui.get_image('c1', 10, 16, 16, (32, 32))[0]
        self.S_SIDE_L_MENU_LIGHT = self.menugui.get_image('b1', 9, 16, 16, (32, 32))[0]
        self.S_SIDE_R_MENU_LIGHT = self.menugui.get_image('e1', 9, 16, 16, (32, 32))[0]
        self.S_MID_MENU_LIGHT = self.menugui.get_image('c1', 9, 16, 16, (32, 32))[0]

        self.S_TOP_L_MENU_BROWN = self.menugui.get_image('b1', 14, 16, 16, (32, 32))[0]
        self.S_TOP_R_MENU_BROWN = self.menugui.get_image('e1', 14, 16, 16, (32, 32))[0]
        self.S_TOP_MENU_BROWN = self.menugui.get_image('c1', 14, 16, 16, (32, 32))[0]
        self.S_BOT_L_MENU_BROWN = self.menugui.get_image('b1', 16, 16, 16, (32, 32))[0]
        self.S_BOT_R_MENU_BROWN = self.menugui.get_image('e1', 16, 16, 16, (32, 32))[0]
        self.S_BOT_MENU_BROWN = self.menugui.get_image('c1', 16, 16, 16, (32, 32))[0]
        self.S_SIDE_L_MENU_BROWN = self.menugui.get_image('b1', 15, 16, 16, (32, 32))[0]
        self.S_SIDE_R_MENU_BROWN = self.menugui.get_image('e1', 15, 16, 16, (32, 32))[0]
        self.S_MID_MENU_BROWN = self.menugui.get_image('c1', 15, 16, 16, (32, 32))[0]

        self.S_MAGIC_ROCK = self.rock.get_image('b', 1, 16, 16, (32, 32))
        self.A_PORTAL_OPEN = self.door.get_animation('c', 6, 2, 16, 16, (32, 32))
        self.S_PORTAL_CLOSED = self.door.get_image('b', 6, 16, 16, (32, 32))

        # ---> GUI
        self.slider_button_size = (26, 20)
        self.S_SLIDER_BUTTON = pygame.image.load("data/graphics/GUI/buttons/BTN_SLIDER_SM_(1).png")
        self.S_SLIDER_BUTTON = pygame.transform.scale(self.S_SLIDER_BUTTON, self.slider_button_size)

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
            "S_STAIRS_DOWN": self.S_STAIRS_DOWN,
            "S_MAGIC_ROCK": self.S_MAGIC_ROCK,
            "A_PORTAL_OPEN": self.A_PORTAL_OPEN,
            "S_PORTAL_CLOSED": self.S_PORTAL_CLOSED
        }

        self.wall_dict = {
            0: self.S_WALL_00,
            1: self.S_WALL_01,
            2: self.S_WALL_02,
            3: self.S_WALL_03,
            4: self.S_WALL_04,
            5: self.S_WALL_05,
            6: self.S_WALL_06,
            7: self.S_WALL_07,
            8: self.S_WALL_08,
            9: self.S_WALL_09,
            10: self.S_WALL_10,
            11: self.S_WALL_11,
            12: self.S_WALL_12,
            13: self.S_WALL_13,
            14: self.S_WALL_14,
            15: self.S_WALL_15
        }

        self.wall_explored_dict = {
            0: self.S_WALL_EXPLORED_00,
            1: self.S_WALL_EXPLORED_01,
            2: self.S_WALL_EXPLORED_02,
            3: self.S_WALL_EXPLORED_03,
            4: self.S_WALL_EXPLORED_04,
            5: self.S_WALL_EXPLORED_05,
            6: self.S_WALL_EXPLORED_06,
            7: self.S_WALL_EXPLORED_07,
            8: self.S_WALL_EXPLORED_08,
            9: self.S_WALL_EXPLORED_09,
            10: self.S_WALL_EXPLORED_10,
            11: self.S_WALL_EXPLORED_11,
            12: self.S_WALL_EXPLORED_12,
            13: self.S_WALL_EXPLORED_13,
            14: self.S_WALL_EXPLORED_14,
            15: self.S_WALL_EXPLORED_15
        }

        # =============================== AUDIO ================================== #

        #                             ||| Music |||

        self.main_menu_music = "data/audio/music/RPG-Blues_Looping.ogg"

        #                          ||| Sound Effects |||

        # complete sfx list
        self.sfx_list = []

        self.sfx_hit_punch1 = self.sfx_add("data/audio/sfx/hit_punch_1.wav")
        self.sfx_hit_punch2 = self.sfx_add("data/audio/sfx/hit_punch_2.wav")
        self.sfx_hit_punch3 = self.sfx_add("data/audio/sfx/hit_punch_3.wav")
        self.sfx_hit_punch4 = self.sfx_add("data/audio/sfx/hit_punch_4.wav")
        self.sfx_hit_punch5 = self.sfx_add("data/audio/sfx/hit_punch_5.wav")

        # sfx list for hitting creature
        self.sfx_hit_punch_list = [self.sfx_hit_punch1,
                                   self.sfx_hit_punch2,
                                   self.sfx_hit_punch3,
                                   self.sfx_hit_punch4,
                                   self.sfx_hit_punch5]
        # adjust volume
        self.volume_adjust()

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

    def volume_adjust(self):

        for sfx in self.sfx_list:
            sfx.set_volume(globalvars.PREFERENCES.sfx_volume_val)

        pygame.mixer.music.set_volume(globalvars.PREFERENCES.music_volume_val)