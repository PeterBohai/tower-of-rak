# Standard library imports
import gzip
import pickle
import sys
import textwrap

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, map, draw, text, actions
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
        self.cur_floor = 1
        self.max_floor_reached = 1
        self.floor_transition_alpha = 0
        self.from_main_menu = True      # to make sure that the floor number
                                        # (title-style not the corner one) displays when game starts

    def map_transition_next(self):
        """Creates a new map if there are no maps in maps_next queue. Otherwise, load the last map in maps_next.

        """

        globalvars.FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_del()

        # save data of current map (before creating new map) on to maps_prev list
        save_data = (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
        self.maps_prev.append(save_data)

        if self.max_floor_reached == self.cur_floor:
            self.max_floor_reached += 1

        self.cur_floor += 1

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
        self.cur_floor -= 1

def game_main_loop():
    """Main game loop.

    Draws the game, takes care of any keyboard or mouse events from the player, keeps track of time/turns, and
    quits the game when requested.

    """
    globalvars.GAME_QUIT = False
    globalvars.FLOOR_CHANGED = False

    # player action definition
    player_action = "no-action"

    # play in-game music
    pygame.mixer.music.load(globalvars.ASSETS.ingame_music)
    pygame.mixer.music.play(-1)

    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # for fading creature damage taken text setup
    while not globalvars.GAME_QUIT:

        draw.draw_game()

        # handle player input
        player_action = game_handle_keys()

        for objActor in globalvars.GAME.current_objects:
            if objActor.is_visible and objActor.creature:

                if objActor.creature.was_hit:
                    objActor.creature.dmg_alpha = 255

                if objActor.creature.dmg_alpha > 0:
                    objActor.creature.draw_damage_taken()

        # makes sure that damage taken ui gets applied to player as well (since creature takes turn in next for loop)
        globalvars.PLAYER.creature.was_hit = False

        # display floor number (title) in the middle for a few seconds when floor changes and when game first starts
        if (globalvars.FLOOR_CHANGED and player_action == "Just Changed Floors") or globalvars.GAME.from_main_menu:
            globalvars.GAME.floor_transition_alpha = 255
            if globalvars.GAME.from_main_menu:
                globalvars.FLOOR_CHANGED = False

        if globalvars.GAME.floor_transition_alpha > 0:
            draw.draw_floor_num_title()

        map.map_calculate_fov()

        # quit the game
        if player_action == "QUIT":
            pygame.mixer.fadeout(10)
            game_exit()

        # creatures takes their turn
        for obj in globalvars.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action":
                    obj.ai.take_turn()

            if obj.is_visible and obj.creature and obj is not globalvars.PLAYER:
                obj.creature.was_hit = False

            if obj.portal:
                obj.portal.update()

        if globalvars.PLAYER.status == "STATUS_DEAD" or globalvars.PLAYER.status == "STATUS_WIN":
            globalvars.GAME_QUIT = True

        globalvars.GAME.from_main_menu = False
        # update the display
        pygame.display.flip()

        # tick the CLOCK
        globalvars.CLOCK.tick(constants.GAME_FPS)


def game_handle_keys():

    # get player input
    events_list = pygame.event.get()  # list of all events so far (like keys pressed and mouse clicks)
    pressed_key_list = pygame.key.get_pressed()    # list of booleans for whether a key is pressed or not

    # load in keybindings from preferences (note this is not a copy of the keybindings dict, just a reference/alias)
    keys = globalvars.PREFERENCES.keybindings

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
            if event.key == keys["up"][1]:
                if len(keys["up"]) == 2:
                    actions.move_one_tile("up")
                    return "player moved"

                elif len(keys["up"]) == 3 and \
                        (keys["up"][2] == pygame.K_LSHIFT or keys["up"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.move_one_tile("up")
                        return "player moved"

            # 'down arrow' key: move player one tile down, hold down to continuing moving automatically
            if event.key == keys["down"][1]:
                if len(keys["down"]) == 2:
                    actions.move_one_tile("down")
                    return "player moved"

                elif len(keys["down"]) == 3 and \
                        (keys["down"][2] == pygame.K_LSHIFT or keys["down"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.move_one_tile("down")
                        return "player moved"

            # 'left arrow' key: move player one tile to the left, hold down to continuing moving automatically
            if event.key == keys["left"][1]:
                if len(keys["left"]) == 2:
                    actions.move_one_tile("left")
                    return "player moved"

                elif len(keys["left"]) == 3 and \
                        (keys["left"][2] == pygame.K_LSHIFT or keys["left"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.move_one_tile("left")
                        return "player moved"

            # 'right arrow' key: move player one tile to the right, hold down to continuing moving automatically
            if event.key == keys["right"][1]:
                if len(keys["right"]) == 2:
                    actions.move_one_tile("right")
                    return "player moved"

                elif len(keys["right"]) == 3 and \
                        (keys["right"][2] == pygame.K_LSHIFT or keys["right"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.move_one_tile("right")
                        return "player moved"

            # 'space bar' key: stay in place but advance turn by 1
            if event.key == keys["stay"][1]:
                if len(keys["stay"]) == 2:
                    return "player moved"

                elif len(keys["stay"]) == 3 and \
                        (keys["stay"][2] == pygame.K_LSHIFT or keys["stay"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        return "player moved"

            # 'g' key: pickup item at the player's current position
            if event.key == keys["grab"][1]:
                if len(keys["grab"]) == 2:
                    actions.grab_item()

                elif len(keys["grab"]) == 3 and \
                        (keys["grab"][2] == pygame.K_LSHIFT or keys["grab"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.grab_item()

            # 'd' key: drop object from inventory
            if event.key == keys["drop"][1]:
                if len(keys["drop"]) == 2:
                    actions.drop_item()

                elif len(keys["drop"]) == 3 and \
                        (keys["drop"][2] == pygame.K_LSHIFT or keys["drop"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.drop_item()

            # 'p' key: pause the game
            if event.key == keys["pause"][1]:
                if len(keys["pause"]) == 2:
                    pause.menu_pause()

                elif len(keys["pause"]) == 3 and \
                        (keys["pause"][2] == pygame.K_LSHIFT or keys["pause"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        pause.menu_pause()

            # 'i' key: open inventory menu
            if event.key == keys["inventory"][1]:
                if len(keys["inventory"]) == 2:
                    inventory.menu_inventory()

                elif len(keys["inventory"]) == 3 and \
                        (keys["inventory"][2] == pygame.K_LSHIFT or keys["inventory"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        inventory.menu_inventory()

            # '>' key: use stairs or portal
            if event.key == keys["next"][1]:
                # for when user sets use stairs to only one key
                if len(keys["next"]) == 2:
                    actions.use_stairs()

                # default is ">" which is a shift and a period (2 keys)
                elif len(keys["next"]) == 3 and \
                        (keys["next"][2] == pygame.K_LSHIFT or keys["next"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        actions.use_stairs()
                return "Just Changed Floors"

            # access in-game options menu or exit from a popup/menu
            if event.key == keys["back"][1]:
                if len(keys["back"]) == 2:
                    previous_display = globalvars.PREFERENCES.display_window

                    options.menu_main_options(ingame_menu_options=True)
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

                    # Change display after exiting options menu (only if there was a change)
                    if previous_display != globalvars.PREFERENCES.display_window and \
                            globalvars.PREFERENCES.display_window == "fullscreen":
                        globalvars.SURFACE_MAIN = pygame.display.set_mode(
                            (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT),
                            flags=pygame.FULLSCREEN)

                    elif previous_display != globalvars.PREFERENCES.display_window:
                        globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH,
                                                                           constants.CAMERA_HEIGHT))

                elif len(keys["back"]) == 3 and \
                        (keys["back"][2] == pygame.K_LSHIFT or keys["back"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        options.menu_main_options(ingame_menu_options=True)
                        pygame.mouse.set_cursor(*pygame.cursors.tri_left)


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
    globalvars.GAME.from_main_menu = True
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
        game_new()

    game_main_loop()
