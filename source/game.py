# Standard library imports
import gzip
import pickle
import sys
import textwrap

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, map, draw, text
from source.menu import pause, inventory, options
from source.generators import playergen



# ================================================================= #
#                         -----  Game  -----                        #
# ================================================================= #

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
        self.current_map, self.current_rooms = map.map_create()

    def map_transition_next(self):
        """Creates a new map if there are no maps in maps_next queue. Otherwise, load the last map in maps_next.

        """

        globalvars.FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_del()

        # save data of current map (before creating new map) on to maps_prev list
        save_data = (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
        self.maps_prev.append(save_data)

        # if the current floor is the top floor so far
        if len(self.maps_next) == 0:

            # erase all items from previous map except the globalvars.PLAYER
            self.current_objects = [globalvars.PLAYER]
            globalvars.PLAYER.animation_init()

            self.current_map, self.current_rooms = map.map_create()
            map.map_place_items_creatures(self.current_rooms)

        # if there are floors above the current floor
        else:

            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.map_make_fov(self.current_map)

            globalvars.FOV_CALCULATE = True

            del self.maps_next[-1]

        game_message("{} moved up a floor!".format(globalvars.PLAYER.creature.name_instance), constants.COLOR_BLUE)

    def map_transition_prev(self):
        """Loads the last map in maps_prev, saving data of current map before doing so.

        """

        if len(self.maps_prev) != 0:
            for obj in self.current_objects:
                obj.animation_del()

            save_data = (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
            self.maps_next.append(save_data)

            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_prev[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.map_make_fov(self.current_map)

            globalvars.FOV_CALCULATE = True

            del self.maps_prev[-1]

        game_message("{} moved down a floor!".format(globalvars.PLAYER.creature.name_instance), constants.COLOR_BLUE)


def game_main_loop():
    """Main game loop.

    Draws the game, takes care of any keyboard or mouse events from the player, keeps track of time/turns, and
    quits the game when requested.

    """
    globalvars.GAME_QUIT = False
    globalvars.FLOOR_CHANGED = False

    # player action definition
    player_action = "no-action"
    display_time = 0
    text_coords = (constants.CAMERA_WIDTH/2, constants.CAMERA_HEIGHT/2 - 40)

    while not globalvars.GAME_QUIT:

        draw.draw_game()

        # handle player input
        player_action = game_handle_keys()

        # display floor number in the middle for a few seconds when floor changes
        if globalvars.FLOOR_CHANGED and player_action == "Just Changed Floors":
            display_time = 180

        elif globalvars.FLOOR_CHANGED:
            floor_num = len(globalvars.GAME.maps_prev) + 1
            text.draw_text(globalvars.SURFACE_MAIN, "Floor - {}".format(floor_num),
                           constants.FONT_BEST,
                           text_coords,
                           constants.COLOR_WHITE,
                           center=True)

        if display_time > 0:
            display_time -= 1
        elif display_time <= 0 and globalvars.FLOOR_CHANGED is True:
            globalvars.FLOOR_CHANGED = False

        map.map_calculate_fov()

        # quit the game
        if player_action == "QUIT":
            game_exit()

            # this is how TURN-BASED is implemented for this game
        for obj in globalvars.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action":
                    obj.ai.take_turn()
            if obj.portal:
                obj.portal.update()

        if globalvars.PLAYER.status == "STATUS_DEAD" or globalvars.PLAYER.status == "STATUS_WIN":
            globalvars.GAME_QUIT = True

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        globalvars.CLOCK.tick(constants.GAME_FPS)


def game_handle_keys():

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
                globalvars.PLAYER.creature.move(0, -1)
                globalvars.FOV_CALCULATE = True
                return "player moved"

            # 'down arrow' key: move player one tile down, hold down to continuing moving automatically
            if event.key == pygame.K_DOWN:
                globalvars.PLAYER.creature.move(0, 1)
                globalvars.FOV_CALCULATE = True
                return "player moved"

            # 'left arrow' key: move player one tile to the left, hold down to continuing moving automatically
            if event.key == pygame.K_LEFT:
                globalvars.PLAYER.creature.move(-1, 0)
                globalvars.FOV_CALCULATE = True
                return "player moved"

            # 'right arrow' key: move player one tile to the right, hold down to continuing moving automatically
            if event.key == pygame.K_RIGHT:
                globalvars.PLAYER.creature.move(1, 0)
                globalvars.FOV_CALCULATE = True
                return "player moved"

            # 'g' key: pickup item at the player's current position
            if event.key == pygame.K_g:
                objects_at_player = map.map_object_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(globalvars.PLAYER)

            # 'd' key: drop object from inventory
            if event.key == pygame.K_d:
                if len(globalvars.PLAYER.container.inventory) > 0:
                    globalvars.PLAYER.container.inventory[-1].item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)

            # 'p' key: pause the game
            if event.key == pygame.K_p:
                pause.menu_pause()

            # 'i' key: open inventory menu
            if event.key == pygame.K_i:
                inventory.menu_inventory()

            # '>' key: use stairs or portal
            if shift_pressed and event.key == pygame.K_PERIOD:

                # check if the player is standing on top of a set of stairs
                list_of_obj = map.map_object_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)

                for obj in list_of_obj:

                    # check if the object contains a stairs component
                    if obj.stairs:
                        obj.stairs.use()
                        FLOOR_CHANGED = True
                        return "Just Changed Floors"

                    if obj.portal:
                        obj.portal.use()

            if event.key == pygame.K_ESCAPE:
                options.menu_main_options(ingame_menu_options=True)

    return "no-action"


def game_message(game_msg, msg_color=constants.COLOR_GREY):
    new_msg_lines = textwrap.wrap(game_msg, constants.MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(globalvars.GAME.message_history) == constants.NUM_MESSAGES:
            del globalvars.GAME.message_history[0]

    globalvars.GAME.message_history.append((game_msg, msg_color))


def game_new():

    globalvars.GAME = ObjGame()
    playergen.gen_player((0, 0))
    map.map_place_items_creatures(globalvars.GAME.current_rooms)
    globalvars.FOV_CALCULATE = True


def game_exit():

    # save the game
    game_save()

    pygame.quit()
    sys.exit()


def game_save():

    # destroy Surface object (from actor animations)
    for obj in globalvars.GAME.current_objects:
        obj.animation_del()

    # write globalvars.GAME and PLAYER objects into compressed binary file
    with gzip.open("data/saves/savegame", "wb") as save_file:
        pickle.dump([globalvars.GAME, globalvars.PLAYER], save_file)


def game_load():

    # since re-assigning these globals

    with gzip.open("data/saves/savegame", "rb") as load_file:
        globalvars.GAME, globalvars.PLAYER = pickle.load(load_file)

    # reinitialize animations
    for obj in globalvars.GAME.current_objects:
        obj.animation_init()

    # create FOV_MAP
    map.map_make_fov(globalvars.GAME.current_map)
    globalvars.FOV_CALCULATE = True


def ingame_save():
    # destroy Surface object (from actor animations)
    for obj in globalvars.GAME.current_objects:
        obj.animation_del()

    # write GAME and PLAYER objects into compressed binary file
    with gzip.open("data/saves/savegame", "wb") as save_file:
        pickle.dump([globalvars.GAME, globalvars.PLAYER], save_file)

    # reinitialize animations
    for obj in globalvars.GAME.current_objects:
        obj.animation_init()


def preferences_save():

    with gzip.open("data/saves/settings", "wb") as save_file:
        pickle.dump(globalvars.PREFERENCES, save_file)


def preferences_load():

    with gzip.open("data/saves/settings", "rb") as load_file:
        globalvars.PREFERENCES = pickle.load(load_file)


def game_start():
    # generate a new game or load a game if there is a save data available
    try:
        game_load()

    except:
        print("No saved game data or error loading save data")
        game_new()

    game_main_loop()