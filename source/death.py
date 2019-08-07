
# standard library imports
import datetime
import os

# Third party imports
import pygame

# Local project imports
from source import constants
from source import gui
from source import globalvars
from source import text
from source import game
from source import magic
from source.generators import itemgen
from source.components import itemcom



# ================================================================= #
#                   -----  Death Functions -----                    #
#                          --- SECTION ---                          #
# ================================================================= #

def death_player(player):
    """Death_function for the player.

    Display a death message and kick player out of game and into the main menu.

    Args:
        player (ObjActor): The PLAYER object that executes this death function when it dies.

    """

    player.status = "STATUS_DEAD"

    center_coords = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    # button variables
    button_width = 96
    button_height = 32
    quit_button_x = constants.CAMERA_WIDTH/2
    quit_button_y = constants.CAMERA_HEIGHT * 3/4

    quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Quit",
                                (quit_button_x, quit_button_y),
                                (button_width, button_height))

    # make a legacy file
    file_name = "legacy_{}_{}.txt".format(player.creature.name_instance,
                                          datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))

    with open("data/saves/{}".format(file_name), 'a+') as legacy_file:
        legacy_file.write("************* {}'s LEGACY FILE ************* \n\n".format(player.creature.name_instance))
        for (message, color) in globalvars.GAME.message_history:
            legacy_file.write(message + '\n')

        legacy_file.write("Deleted any game save files\n")

    # delete save game file
    save_to_rm = "data/saves/savegame"
    try:
        os.remove(save_to_rm)
    except OSError as e:
        print("Error: {} - {}".format(e.filename, e.strerror))

    # For exiting out of the game
    death_popup = True
    while death_popup:

        # get player input
        events_list = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        player_events = (events_list, mouse_pos)

        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    death_popup = False

        if quit_button.update(player_events):
            death_popup = False

        globalvars.SURFACE_MAIN.fill(constants.COLOR_GAME_BG)
        text.draw_text(globalvars.SURFACE_MAIN, "You Died!", constants.FONT_PLAYER_DEATH,
                       center_coords,
                       constants.COLOR_RED,
                       center=True)

        quit_button.draw()

        pygame.display.update()


def death_snake_monster(monster):
    """Death_function for dead snake creatures.

    Creature stops moving, loses its creature component and its idle animation becomes a still piece of snake flesh.

    Args:
        monster (ObjActor): The actor creature object that will execute this death function when it dies.

    """

    death_msg = "{} is dead!".format(monster.display_name)
    # death_msg = monster.creature.name_instance + " is dead!"
    game.game_message(death_msg, constants.COLOR_WHITE)

    monster.animation_key = "S_FLESH_SNAKE"
    monster.animation = globalvars.ASSETS.animation_dict[monster.animation_key]

    monster.creature = None
    monster.ai = None


def death_healer_monster(monster):
    """Death_function for dead healing creatures.

    Creature stops moving, loses its creature component and its idle animation becomes a still piece of healing item.

    Args:
        monster (ObjActor): The actor creature object that will execute this death function when it dies.

    """

    death_msg = "{} is dead and dropped a healing element!".format(monster.display_name)
    game.game_message(death_msg, constants.COLOR_GREEN)

    monster.animation_key = "S_WATER_CUP"
    monster.animation = globalvars.ASSETS.animation_dict[monster.animation_key]
    monster.name_object = "Water Cup"

    monster.creature = None
    monster.ai = None


def death_enemy(mob):

    death_msg = f"{mob.display_name} is dead and dropped a healing element!"
    game.game_message(death_msg, constants.COLOR_GREEN)

    mob.set_animation_key("S_WATER_CUP")
    mob.name_object = "Red Soul"

    coin_drop = itemgen.gen_coins((mob.x, mob.y), 10)
    globalvars.GAME.current_objects.insert(0, coin_drop)

    mob.creature = None
    mob.ai = None

