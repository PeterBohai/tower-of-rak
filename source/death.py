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
from source.generators import itemgen


def death_player(player):
    """Death function for when PLAYER dies.

    Parameters
    ----------
    player : ObjActor obj
        The PLAYER object that executes this death function.

    Returns
    -------
    None

    """
    player.status = "STATUS_DEAD"
    center_coords = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    # button variables
    button_width = 96
    button_height = 32
    quit_button_x = constants.CAMERA_WIDTH/2
    quit_button_y = constants.CAMERA_HEIGHT * 3/4

    quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Quit", (quit_button_x, quit_button_y),
                                (button_width, button_height))

    # create a legacy file and delete any game save files
    file_name = "legacy_{}_{}.txt".format(player.creature.name_instance,
                                          datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))
    with open("data/saves/{}".format(file_name), 'a+') as legacy_file:
        legacy_file.write("************* {}'s LEGACY FILE ************* \n\n".format(player.creature.name_instance))
        for (message, color) in globalvars.GAME.message_history:
            legacy_file.write(message + '\n')

        legacy_file.write("Deleted any previous game save files\n")

    save_to_rm = "data/saves/savegame"
    try:
        os.remove(save_to_rm)
    except OSError:
        print("No prior save file to delete")

    # deinitialize pygame Surface objects (animation sprites)
    for obj in globalvars.GAME.current_objects:
        obj.animation_del()

    # popup menu displaying a "You Died!" message and a quit to main menu button
    death_popup = True
    while death_popup:
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


def death_enemy(mob):
    """Death function for unfriendly mobs.

    The dead mob leaves a slow bobbing red soul behind that gives experience points when consumed/picked up and has a
    chance to drop coins or items.

    Parameters
    ----------
    mob : ObjActor obj
        The mob object that executes this death function (an actor object with a creature component).

    Returns
    -------
    None

    """

    death_msg = f"{mob.display_name} is dead!"
    game.game_message(death_msg, constants.COLOR_WHITE)

    mob.animation_key = "A_DEATH_RED"
    mob.object_name = "Red Soul"
    mob.animation_speed = 1.5

    coin_drop = itemgen.gen_coins((mob.x, mob.y), 10)
    globalvars.GAME.current_objects.insert(0, coin_drop)

    mob.creature = None
    mob.ai = None


def death_friendly(mob):
    """Death function for friendly mobs.

    The dead mob leaves a slow bobbing blue soul behind that gives heals for a certain amount when consumed/picked up.

    Parameters
    ----------
    mob : ObjActor obj
        The mob object that executes this death function (an actor object with a creature component).

    Returns
    -------
    None

    """

    death_msg = f"{mob.display_name} is dead and dropped a healing element!"
    game.game_message(death_msg, constants.COLOR_GREEN)

    mob.animation_key = "A_DEATH_BLUE"
    mob.object_name = "Pure Soul"
    mob.animation_speed = 1.6

    mob.creature = None
    mob.ai = None

