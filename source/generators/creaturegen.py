# Third party imports
import tcod, random, numpy

# Local project imports
from source import globalvars, actor, death, magic
from source.components import creature, ai, itemcom


def gen_enemy(room_range_x, room_range_y, floor_num):
    """Generates random enemies in random positions in a room.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated enemy creature.

    Returns:
         Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    """

    mob_dict = {
        #  chance between species  |    the species  | max num of enemies per room
        1: ((0.1, 0.9),
            (gen_snake_cobra(room_range_x, room_range_y), gen_snake_boa(room_range_x, room_range_y)),
            4),

        2: ((1, 9),
            (gen_snake_cobra(room_range_x, room_range_y), gen_snake_boa(room_range_x, room_range_y)),
            1),

        3: ((1, 9),
            (gen_snake_cobra(room_range_x, room_range_y), gen_snake_boa(room_range_x, room_range_y)),
            1),

    }

    new_enemy = numpy.random.choice(mob_dict[floor_num][1], p=mob_dict[floor_num][0])

    globalvars.GAME.current_objects.insert(-1, new_enemy)


def gen_friendly_mob(room_range_x, room_range_y, floor_num):

    choice_num = random.randint(1, 100)

    if choice_num <= 80:
        new_healer = gen_healer_slime(room_range_x, room_range_y)
        globalvars.GAME.current_objects.insert(-1, new_healer)


def gen_snake_boa(room_range_x, room_range_y):
    x, y = (random.randint(*room_range_x), random.randint(*room_range_y))

    base_attack = tcod.random_get_int(0, 1, 2)
    max_health = tcod.random_get_int(0, 12, 14)
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


def gen_snake_cobra(room_range_x, room_range_y):
    x, y = (random.randint(*room_range_x), random.randint(*room_range_y))

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


def gen_healer_slime(room_range_x, room_range_y):
    x, y = (random.randint(*room_range_x), random.randint(*room_range_y))

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