# Third party imports
import tcod, random, numpy

# Local project imports
from source import globalvars, actor, death, magic
from source.components import creature, ai, itemcom

"""
Note the speed performance of generating random integers varies quite drastically between different methods

import timeit
t1 = timeit.timeit("n=random.randint(0, 2)", setup="import random", number=1000000)
t2 = timeit.timeit("n=random.choice((0, 1, 2))", setup="import random", number=1000000)
t3 = timeit.timeit("n=random.choice(ar)", setup="import random; ar = (0, 1, 2)", number=1000000)
t4 = timeit.timeit("n=random.randrange(0, 3)", setup="import random", number=1000000)
t5 = timeit.timeit("n=tcod.random_get_int(0, 0, 2)", setup="import tcod", number=1000000)
t6 = timeit.timeit("n=numpy.random.randint(0, 3)", setup="import numpy", number=1000000)

[print(f't{i+1}:   {t}') for i, t in enumerate([t1, t2, t3, t4, t5, t6])]
t1:   1.5368656630000714
t2:   0.9390302479999946
t3:   0.9536893929999906
t4:   1.2985620769999286
t5:   0.5123831550000659
t6:   1.7503905009999698

"""


def gen_enemy(room_range_x, room_range_y, floor_num):
    """Generates random enemies in random positions in a room.

    Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    Args:
        room_range_x (tuple): The (min, max) x-coordinates of the current room to be populated.
        room_range_y (tuple): The (min, max) y-coordinates of the current room to be populated.
        floor_num (int): The current floor number that the room is on.

    Returns:
         None
    """
    coord_range = (room_range_x, room_range_y)

    mob_dict = {
        #  chance between species  |    the species  | max num of enemies per room
        1: ((0.95, 0.05),
            (gen_dungo(*coord_range), gen_darksoot(*coord_range)),
            4),

        2: ((0.8, 0.2),
            (gen_dungo(*coord_range), gen_darksoot(*coord_range)),
            4),

        3: ((0.5, 0.3, 0.2),
            (gen_dungo(*coord_range), gen_blazeo(*coord_range), gen_darksoot(*coord_range)),
            4),

        4: ((0.5, 0.3, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range)),
            1),

        5: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        6: ((0.4, 0.2, 0.2, 0.1),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        7: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        8: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        9: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        10: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        11: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),

        12: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range)),
            1),
    }

    # choose one of the mobs according to their spawn probability
    new_enemy = numpy.random.choice(mob_dict[floor_num][1], p=mob_dict[floor_num][0])

    globalvars.GAME.current_objects.insert(-1, new_enemy)


def gen_friendly_mob(room_range_x, room_range_y, floor_num):
    """Generates random friendly creature in a random position in a room.

    Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    Args:
        room_range_x (tuple): The (min, max) x-coordinates of the current room to be populated.
        room_range_y (tuple): The (min, max) y-coordinates of the current room to be populated.
        floor_num (int): The current floor number that the room is on.

    Returns:
         None
    """

    choice_num = tcod.random_get_int(0, 1, 100)

    if choice_num <= 80:
        new_healer = gen_healer_slime(room_range_x, room_range_y)
        globalvars.GAME.current_objects.insert(-1, new_healer)

        # ---------------------------------------- #
        # ------ Specific mob generators --------- #
        # ---------------------------------------- #


def gen_dungo(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Dungo"
    creature_sprite = "A_DUNGO"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 8
    base_attack = 2
    base_defence = 0

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_darksoot(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "DarkSoot"
    creature_sprite = "A_DARKSOOT"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 10
    base_attack = 3
    base_defence = 0

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_blazeo(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Blazeo"
    creature_sprite = "A_BLAZEO"
    personal_name = tcod.namegen_generate("Fantasy female")

    health = 8
    base_attack = 3
    base_defence = 0

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_shelk(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Shelk"
    creature_sprite = "A_SHELK"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 12
    base_attack = 2
    base_defence = 3

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_kelpclopse(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "KelpClopse"
    creature_sprite = "A_KELPCLOPSE"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 12
    base_attack = 4
    base_defence = 1

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem()
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


# ----- FRIENDLY MOBS ----- #

def gen_healer_slime(room_range_x, room_range_y):

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Healer Slime"
    creature_sprite = "A_HEALER_SLIME"
    personal_name = tcod.namegen_generate("Fantasy female")

    base_attack = 0
    base_defence = 0
    health = 5

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_friendly)

    item_com = itemcom.ComItem(use_function=magic.cast_heal, value=2)

    ai_com = ai.AiFlee()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj

