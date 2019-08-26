import gzip
import pickle
import sys
import textwrap

import pygame

from src import constants, globalvars, map, draw, actions, hud
from src.menu import pause, inventory, options
from src.generators import playergen


class ObjGame:
    """A game object class that keeps track of game progress.

    Stores and tracks all game information including maps, objects, and a record of game messages.

     Attributes
    ----------
    current_objects : list
        List of objects on the current map (excluding inventory objects).
    message_history : list
        List of messages that have been displayed on the game screen.
    maps_next : list of tuples
        List of map data for encountered maps, where maps are saved to before transitioning to a lower floor.
    maps_prev : list of tuples
        List of map data for encountered maps, where maps are saved to before transitioning to a higher floor.
    current_map : list (nested)
        The map that is currently loaded and displayed (contains floor and wall tile info).
    current_rooms : list
        List of all valid ObjRoom objects on the current map.
    cur_floor : int
        The current floor number the PLAYER is on.
    max_floor_reached : int
        The max floor number the PLAYER has reached.
    floor_transition_alpha : int
        The alpha value [0, 255], that is used to fade out the floor title text when entering a new floor.
    from_main_menu : bool
        Tracks if the PLAYER has just started a game from the main menu.

    """
    def __init__(self):
        self.current_objects = []
        self.message_history = []
        self.maps_next = []
        self.maps_prev = []
        self.current_map, self.current_rooms = map.map_create()
        self.cur_floor = 1
        self.max_floor_reached = 1
        self.floor_transition_alpha = 0
        self.from_main_menu = True

    def map_transition_next(self):
        """Transitions the PLAYER to a higher floor map when using stairs that go upwards.

        Creates a new map if there are no maps in maps_next queue. Otherwise, load the last map in maps_next.

        Returns
        -------
        None

        """

        globalvars.FOV_CALCULATE = True
        for obj in self.current_objects:
            obj.animation_del()

        # save data of current map (before creating new map) on to maps_prev list
        save_data = (globalvars.PLAYER.x, globalvars.PLAYER.y,
                     self.current_map, self.current_rooms, self.current_objects)
        self.maps_prev.append(save_data)

        if self.max_floor_reached == self.cur_floor:
            self.max_floor_reached += 1

        self.cur_floor += 1

        # if the current floor has no explored floors above it
        if len(self.maps_next) == 0:

            # erase all items from previous map except the PLAYER
            self.current_objects = [globalvars.PLAYER]
            globalvars.PLAYER.animation_init()

            self.current_map, self.current_rooms = map.map_create()
            map.map_place_items_creatures(self.current_rooms)

        # if there are floors above the current floor
        else:

            (globalvars.PLAYER.x, globalvars.PLAYER.y,
             self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.create_fov_map(self.current_map)

            globalvars.FOV_CALCULATE = True

            del self.maps_next[-1]

        game_message("{} moved up a floor!".format(globalvars.PLAYER.creature.name_instance), constants.COLOR_BLUE)

    def map_transition_prev(self):
        """Transitions the PLAYER to a lower floor map when using stairs that go downwards.

        Loads the last map in maps_prev, saving data of current map before doing so.

        Returns
        -------
        None

        """
        if len(self.maps_prev) != 0:
            for obj in self.current_objects:
                obj.animation_del()

            save_data = (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects)
            self.maps_next.append(save_data)

            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_prev[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.create_fov_map(self.current_map)

            globalvars.FOV_CALCULATE = True

            del self.maps_prev[-1]

        game_message("{} moved down a floor!".format(globalvars.PLAYER.creature.name_instance), constants.COLOR_BLUE)
        self.cur_floor -= 1


def game_main_loop():
    """Main game loop.

    Draws the game, takes care of any keyboard or mouse events from the player, keeps track of time/turns, and
    quits the game when requested.

    Returns
    -------
    None

    """
    pygame.mixer.music.load(globalvars.ASSETS.ingame_music)
    pygame.mixer.music.play(-1)
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # set flags and counters
    globalvars.GAME_QUIT = False
    globalvars.FLOOR_CHANGED = False

    while not globalvars.GAME_QUIT:

        draw.draw_game()

        player_action = game_handle_keys()
        if player_action == "QUIT":
            game_exit()

        for objActor in globalvars.GAME.current_objects:
            if objActor.is_visible and objActor.creature is not None:

                if objActor.creature.was_hit and objActor is not globalvars.PLAYER:
                    objActor.creature.internal_timer = pygame.time.get_ticks()
                    objActor.creature.dmg_alpha = 255
                    objActor.creature.health_bar_alpha = 255

                elif objActor.creature.was_hit and objActor is globalvars.PLAYER:
                    objActor.creature.dmg_alpha = 255

                if objActor.creature.dmg_alpha > 0:
                    objActor.creature.draw_damage_taken()

        # makes sure that damage taken ui gets applied to player as well (since creature takes turn in next for loop)
        globalvars.PLAYER.creature.was_hit = False

        # display floor title for a few seconds when floor changes and when game first starts
        if (globalvars.FLOOR_CHANGED and player_action == "Just Changed Floors") or globalvars.GAME.from_main_menu:
            globalvars.GAME.floor_transition_alpha = 255
            if globalvars.GAME.from_main_menu:
                globalvars.FLOOR_CHANGED = False

        if globalvars.GAME.floor_transition_alpha > 0:
            hud.draw_floor_title()

        map.update_fov()

        # creatures takes their turn
        for obj in globalvars.GAME.current_objects:
            if obj.ai is not None:
                if player_action != "no-action":
                    obj.ai.take_turn()

            if obj.is_visible and obj.creature is not None and obj is not globalvars.PLAYER:
                obj.creature.was_hit = False

            if obj.portal is not None:
                obj.portal.update()

        if globalvars.PLAYER.status == "STATUS_DEAD" or globalvars.PLAYER.status == "STATUS_WIN":
            globalvars.GAME_QUIT = True

        globalvars.GAME.from_main_menu = False
        pygame.display.flip()
        globalvars.CLOCK.tick(constants.GAME_FPS)


def game_handle_keys():
    """Handles player keyboard and mouse inputs and executes them accordingly.

    Returns
    -------
    str
        Status information indicating the action the PLAYER took.

    """

    # get player input
    events_list = pygame.event.get()
    pressed_key_list = pygame.key.get_pressed()

    # load in keybindings from preferences (note this is not a copy of the keybindings dict, just a reference/alias)
    keys = globalvars.PREFERENCES.keybindings

    shift_pressed = (pressed_key_list[pygame.K_RSHIFT] or pressed_key_list[pygame.K_LSHIFT])

    # process input
    for event in events_list:
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
                    globalvars.PLAYER.animation_key = "A_PLAYER_LEFT"
                    actions.move_one_tile("left")
                    return "player moved"

                elif len(keys["left"]) == 3 and \
                        (keys["left"][2] == pygame.K_LSHIFT or keys["left"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        globalvars.PLAYER.animation_key = "A_PLAYER_LEFT"
                        actions.move_one_tile("left")
                        return "player moved"

            # 'right arrow' key: move player one tile to the right, hold down to continuing moving automatically
            if event.key == keys["right"][1]:
                if len(keys["right"]) == 2:
                    globalvars.PLAYER.animation_key = "A_PLAYER_RIGHT"
                    actions.move_one_tile("right")
                    return "player moved"

                elif len(keys["right"]) == 3 and \
                        (keys["right"][2] == pygame.K_LSHIFT or keys["right"][2] == pygame.K_RSHIFT):
                    if shift_pressed:
                        globalvars.PLAYER.animation_key = "A_PLAYER_RIGHT"
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


def game_message(text, color=constants.COLOR_GREY):
    """Adds a game message to the list of messages.

    Separates lines of text that is longer than the specified msg width (constants.MSG_MAX_CHARS) into different
    message pieces to be appended to the list of messages separately.

    Parameters
    ----------
    text : str
        The game message content.
    color : tuple
        The color the message text will be displayed in.

    Returns
    -------
    None

    """
    new_msg_lines = textwrap.wrap(text, constants.MSG_MAX_CHARS)

    for line in new_msg_lines:

        # if the buffer is full, remove the first line to make room for the new one
        if len(globalvars.GAME.message_history) == constants.NUM_MESSAGES:
            del globalvars.GAME.message_history[0]

        globalvars.GAME.message_history.append((line, color))


def game_new():
    """Starts a new game starting from Floor 1.

    Initializes the player, GAME object, all other actors for the first floor as well as the FOV_CALCULATE.

    Returns
    -------
    None

    """

    globalvars.GAME = ObjGame()

    # position doesn't matter as it will be set when every actor is placed with map_place_items_creatures
    playergen.gen_player((0, 0))
    map.map_place_items_creatures(globalvars.GAME.current_rooms)
    globalvars.FOV_CALCULATE = True


def game_exit():
    """Saves current game before exiting the game.

    Returns
    -------
    None

    """
    pygame.mixer.fadeout(10)
    game_save()
    pygame.quit()
    sys.exit()


def game_save(in_game=False):
    """Saves the game into a compressed binary file. Reinitialize animations if saving in-game from options menu.

    Returns
    -------
    None

    """
    with gzip.open("data/saves/savegame", "wb") as save_file:
        try:
            # destroy Surface objects so pickle can save the data
            for obj in globalvars.GAME.current_objects:
                obj.animation_del()

            pickle.dump([globalvars.GAME, globalvars.PLAYER], save_file)
        except TypeError:
            print("TypeError, couldn't save game")

    if in_game:
        # reinitialize animations
        for obj in globalvars.GAME.current_objects:
            obj.animation_init()


def game_load():
    """Load previous game from save file.

    Returns
    -------
    None

    """

    with gzip.open("data/saves/savegame", "rb") as load_file:
        globalvars.GAME, globalvars.PLAYER = pickle.load(load_file)

    # reinitialize animations
    for obj in globalvars.GAME.current_objects:
        obj.animation_init()

    globalvars.GAME.from_main_menu = True

    map.create_fov_map(globalvars.GAME.current_map)
    globalvars.FOV_CALCULATE = True


def preferences_save():
    """Saves games settings.

    Returns
    -------
    None

    """

    with gzip.open("data/saves/settings", "wb") as save_file:
        pickle.dump(globalvars.PREFERENCES, save_file)


def preferences_load():
    """Loads previous game settings.

    Returns
    -------
    None

    """

    with gzip.open("data/saves/settings", "rb") as load_file:
        globalvars.PREFERENCES = pickle.load(load_file)


def game_start(new=True):
    """Loads a saved game or generate a new game if there is a no save data

    Returns
    -------
    None

    """
    if new:
        game_new()
    else:
        try:
            game_load()

        except FileNotFoundError:
            # TODO indicate that a new game was initiated instead (pop up notice)
            game_new()

    game_main_loop()
