from source import constants, map, game
from source.menu import tileselect
from source.components import ai


def cast_heal(target, value):
    """Heals the `target` creature for `value` amount.

    Notifies the PLAYER that health is already full if currently at max hp.

    Parameters
    ----------
    target : ObjActor obj
        The actor object with a creature component that will be healed.
    value : int
        The amount of hp the `target` creature will gain.

    Returns
    -------
    bool
        True if the heal was successful, False otherwise.

    """
    if target.creature.current_hp < target.creature.maxHp:
        target.creature.heal(value)
        return True
    else:
        full_hp_msg = f"{target.creature.name_instance} is already at full health!"
        game.game_message(full_hp_msg, constants.COLOR_BLUE)
        return False


def cast_lightening(caster, dmg_and_range):
    """Casts a spell that damages all targets in a line of tiles within a certain range of the `caster`.

    Notifies the PLAYER that health is already full if currently at max hp.

    Parameters
    ----------
    caster : ObjActor obj
        The actor object using or casting this spell.
    dmg_and_range : tuple
        Contains (damage amount, max range) int values.

    Returns
    -------
    bool
        True if the spell was successful, False otherwise.

    """
    caster_location = (caster.x, caster.y)
    damage, max_r = dmg_and_range
    damaged_something = False
    selected_tile_address = tileselect.menu_tile_select(coords_origin=caster_location, max_range=max_r,
                                                        wall_penetration=False, base_color=constants.COLOR_YELLOW)

    # continue with casting of spell only if caster did not cancel the spell (by using esc from menu_tile_select)
    if selected_tile_address:
        list_of_tiles_affected = map.map_find_line(caster_location, selected_tile_address)

        # damage all creatures in the line of sight of the spell
        for i, (x, y) in enumerate(list_of_tiles_affected):
            target_creature = map.map_check_for_creatures(x, y)

            if target_creature and i != 0:
                target_creature.creature.take_damage(damage)
                damaged_something = True

            if target_creature and len(list_of_tiles_affected) == 1:
                game.game_message("Watch out! Aim away from yourself please.", constants.COLOR_WHITE)
                return False

        game.game_message(f"{caster.creature.name_instance} casts lightening", constants.COLOR_WHITE)
        if not damaged_something:
            game.game_message("Nothing was hit, what a waste.", constants.COLOR_WHITE)

        return True
    else:
        return False


def cast_fireball(caster, dmg_range_radius):
    """Casts a spell that damages all targets in a radius of tiles within a certain range of the `caster`.

    Parameters
    ----------
    caster : ObjActor obj
        The actor object using or casting this spell.
    dmg_range_radius : tuple
        Contains (damage amount, max range, max radius) int values.

    Returns
    -------
    bool
        True if the spell was successful, False otherwise.

    """
    damage, spell_range, spell_radius = dmg_range_radius
    caster_location = (caster.x, caster.y)
    damaged_something = False
    selected_tile_address = tileselect.menu_tile_select(coords_origin=caster_location,
                                                        max_range=spell_range,
                                                        radius=spell_radius,
                                                        wall_penetration=False,
                                                        creature_penetration=False)
    if selected_tile_address:
        game.game_message(f"{caster.creature.name_instance} casts fireball", constants.COLOR_WHITE)

        list_of_tiles_to_damage = map.map_find_radius(selected_tile_address, spell_radius)

        # damage all creatures in the aoe sphere
        for (x, y) in list_of_tiles_to_damage:
            target_creature = map.map_check_for_creatures(x, y)
            if target_creature:
                target_creature.creature.take_damage(damage)
                damaged_something = True

        if not damaged_something:
            game.game_message("Nothing was hit, what a waste.", constants.COLOR_WHITE)

        return True
    else:
        return False


def cast_confusion(caster, effect_length):
    """Casts a spell that confuses the selected target and forces them to move in uncontrollable, random directions.

    Parameters
    ----------
    caster : ObjActor obj
        The actor object using or casting this spell.
    effect_length : int
        The number of turns the spell lasts.

    Returns
    -------
    bool
        True if the spell was successful, False otherwise.

    """
    selected_tile_address = tileselect.menu_tile_select(wall_penetration=False,
                                                        single_tile=True,
                                                        target_color=constants.COLOR_GREEN)
    if selected_tile_address:

        target_tile_x, target_tile_y = selected_tile_address

        target_creature = map.map_check_for_creatures(target_tile_x, target_tile_y)

        if target_creature:
            game.game_message(f"{caster.creature.name_instance} casts confusion on {target_creature.display_name}",
                              constants.COLOR_WHITE)
            normal_ai = target_creature.ai

            target_creature.ai = ai.AiConfuse(original_ai=normal_ai, num_turns=effect_length)
            target_creature.ai.owner = target_creature

            game.game_message(f"{target_creature.display_name} is confused for {effect_length} turns!",
                              constants.COLOR_GREEN)

        return True
    else:
        return False
