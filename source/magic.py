# Standard library imports
import math

# Third party imports
import pygame
import tcod

# Local project imports
from source import constants, map, game, globalvars
from source.menu import tileselect
from source.components import ai

# ================================================================= #
#                        -----  Magic  -----                        #
# ================================================================= #


def cast_heal(target, value):
    if target.creature.current_hp == target.creature.maxHp:
        full_hp_msg = target.creature.name_instance + " is already at full health!"
        game.game_message(full_hp_msg, constants.COLOR_BLUE)
        return "Already full health!"

    else:
        target.creature.heal(value)
    return None


def cast_lightening(caster, tup_dmg_range):

    # might set this from a parameter in the future if enemies, other creatures other than the PLAYER uses this spell
    caster_location = (caster.x, caster.y)

    damage, max_r = tup_dmg_range

    # prompt player for a target tile
    selected_tile_address = tileselect.menu_tile_select(coords_origin=caster_location,
                                                        max_range=max_r,
                                                        wall_penetration=False,
                                                        base_color=constants.COLOR_YELLOW)

    damaged_something = False

    # continue with casting of spell only if caster did not "cancel" the spell (by escaping from tileselect.menu_tile_select)
    if selected_tile_address:

        # convert tile into a list of coords between a and b
        list_of_tiles_affected = map.map_find_line(caster_location, selected_tile_address)

        game.game_message("{} cast lightening".format(caster.creature.name_instance),
                          constants.COLOR_WHITE)

        # cycle through list and damage everything in that list
        for i, (x, y) in enumerate(list_of_tiles_affected):
            target_creature = map.map_check_for_creatures(x, y)

            if target_creature and i != 0:
                target_creature.creature.take_damage(damage)
                damaged_something = True

            if target_creature and len(list_of_tiles_affected) == 1:
                game.game_message("Aim away from yourself please.".format(caster.creature.name_instance),
                                  constants.COLOR_WHITE)
                return "unused"

        if not damaged_something:
            game.game_message("Nothing was harmed, what a waste.".format(caster.creature.name_instance),
                              constants.COLOR_WHITE)

    else:
        return "unused"


def cast_fireball(caster, tup_dmg_range_radius):

    damage, spell_range, spell_radius = tup_dmg_range_radius

    # caster is the one holding the spell
    caster_location = (caster.x, caster.y)

    # prompt player for a target tile
    selected_tile_address = tileselect.menu_tile_select(coords_origin=caster_location,
                                                        max_range=spell_range,
                                                        radius=spell_radius,
                                                        wall_penetration=False,
                                                        creature_penetration=False)
    # get sequence of tiles
    if selected_tile_address:
        game.game_message("{} casts fireball".format(caster.creature.name_instance),
                          constants.COLOR_WHITE)

        list_of_tiles_to_damage = map.map_find_radius(selected_tile_address, spell_radius)

        # damage all creatures in tiles
        for (x, y) in list_of_tiles_to_damage:
            target_creature = map.map_check_for_creatures(x, y)

            if target_creature:
                target_creature.creature.take_damage(damage)

    else:
        return "unused"


def cast_confusion(caster, effect_length):

    # prompt player for a target tile
    selected_tile_address = tileselect.menu_tile_select(wall_penetration=False,
                                                        single_tile=True,
                                                        target_color=constants.COLOR_GREEN)

    # get target
    if selected_tile_address:

        target_tile_x, target_tile_y = selected_tile_address

        target_creature = map.map_check_for_creatures(target_tile_x, target_tile_y)

        if target_creature:
            game.game_message("{} casts confusion on {}".format(caster.creature.name_instance, target_creature.display_name),
                              constants.COLOR_WHITE)

            normal_ai = target_creature.ai

            target_creature.ai = ai.AiConfuse(original_ai=normal_ai, num_turns=effect_length)
            target_creature.ai.owner = target_creature

            game.game_message("{} is now confused!".format(target_creature.display_name), constants.COLOR_GREEN)

    else:
        return "unused"
