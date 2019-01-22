# Third party imports
import tcod

# Local project imports
from source import globalvars, actor, death, magic
from source.components import creature, ai, itemcom

def gen_enemy(tup_coords):
    """Generates a random enemy at the given coordinates specified by tup_coords.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated enemy creature.

    Returns:
         Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    """

    choice_num = tcod.random_get_int(0, 1, 100)

    if choice_num <= 15:
        new_enemy = gen_snake_cobra(tup_coords)

    else:
        new_enemy = gen_snake_boa(tup_coords)

    if choice_num <= 100:
        new_healer = gen_healer_slime(tup_coords)
        globalvars.GAME.current_objects.insert(-1, new_healer)

    globalvars.GAME.current_objects.insert(-1, new_enemy)


def gen_snake_boa(tup_coords):
    x, y = tup_coords

    base_attack = tcod.random_get_int(0, 1, 2)
    max_health = tcod.random_get_int(0, 7, 10)
    creature_name = tcod.namegen_generate("Fantasy male")

    creature_com = creature.ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death.death_snake_monster)  # base attack is 2
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()

    snake_boa_obj = actor.ObjActor(x, y, "Giant Boa",
                             "A_GIANT_BOA",
                             animation_speed=1,
                             creature=creature_com,
                             ai=ai_com,
                             item=item_com)
    return snake_boa_obj


def gen_snake_cobra(tup_coords):
    x, y = tup_coords

    base_attack = tcod.random_get_int(0, 2, 3)
    max_health = tcod.random_get_int(0, 15, 18)
    creature_name = tcod.namegen_generate("Fantasy female")

    creature_com = creature.ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death.death_snake_monster)    # default base atk is 2
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()

    snake_cobra_obj = actor.ObjActor(x, y, "Dark Cobra",
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

    creature_com = creature.ComCreature(creature_name,
                               base_atk=base_attack,
                               max_hp=max_health,
                               death_function=death.death_healer_monster)

    item_com = itemcom.ComItem(use_function=magic.cast_heal, value=2)
    ai_com = ai.AiFlee()

    healer_zom_obj = actor.ObjActor(x, y, "Healer Slime",
                              "A_HEALER_SLIME",
                              animation_speed=1,
                              creature=creature_com,
                              ai=ai_com,
                              item=item_com)
    return healer_zom_obj