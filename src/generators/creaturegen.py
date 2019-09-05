import tcod
import numpy

from src import globalvars, actor, death, magic
from src.components import creature, ai, itemcom


def gen_enemy(room_range_x, room_range_y, floor_num):
    """Generates random enemies at random positions in a room.

    Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room to be populated.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room to be populated.
    floor_num : int
        The current floor number that the room is on.

    Returns
    -------
    None

    """
    coord_range = (room_range_x, room_range_y)

    mob_dict = {
        #  chance between species  |    the species
        1: ((0.95, 0.05),
            (gen_dungo(*coord_range), gen_darksoot(*coord_range))),

        2: ((0.8, 0.2),
            (gen_dungo(*coord_range), gen_darksoot(*coord_range))),

        3: ((0.5, 0.3, 0.2),
            (gen_dungo(*coord_range), gen_blazeo(*coord_range), gen_darksoot(*coord_range))),

        4: ((0.5, 0.3, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range))),

        5: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

        6: ((0.4, 0.2, 0.2, 0.1),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

        7: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

        8: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

        9: ((0.4, 0.2, 0.2, 0.2),
            (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

        10: ((0.4, 0.2, 0.2, 0.2),
             (gen_blazeo(*coord_range), gen_darksoot(*coord_range), gen_shelk(*coord_range),
             gen_kelpclopse(*coord_range))),

    }

    # choose one of the mobs according to their spawn probability
    new_enemy = numpy.random.choice(mob_dict[floor_num][1], p=mob_dict[floor_num][0])

    globalvars.GAME.current_objects.insert(-1, new_enemy)


def gen_friendly_mob(room_range_x, room_range_y, floor_num):
    """Generates random friendly creature in a random position in a room.

    Inserts a randomly generated enemy creature object at the end of the GAME.current_objects list.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room to be populated.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room to be populated.
    floor_num : int
        The current floor number that the room is on.

    Returns
    -------
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
    """Generates a Dungo mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a Dungo mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Dungo"
    creature_sprite = "A_DUNGO"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 8
    base_attack = 2
    base_defence = 0
    exp_pts = 4

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem("An evil soul that gives exp when consumed", item_type="Red Soul", value=exp_pts)
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_darksoot(room_range_x, room_range_y):
    """Generates a DarkSoot mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a DarkSoot mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "DarkSoot"
    creature_sprite = "A_DARKSOOT"
    personal_name = tcod.namegen_generate("Fantasy male")
    exp_pts = 6

    health = 10
    base_attack = 3
    base_defence = 0

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem("An evil soul that gives exp when consumed", item_type="Red Soul", value=exp_pts)
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_blazeo(room_range_x, room_range_y):
    """Generates a Blazeo mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a Blazeo mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Blazeo"
    creature_sprite = "A_BLAZEO"
    personal_name = tcod.namegen_generate("Fantasy female")

    health = 8
    base_attack = 3
    base_defence = 0
    exp_pts = 8

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem("An evil soul that gives exp when consumed", item_type="Red Soul", value=exp_pts)
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_shelk(room_range_x, room_range_y):
    """Generates a Shelk mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a Shelk mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "Shelk"
    creature_sprite = "A_SHELK"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 12
    base_attack = 2
    base_defence = 3
    exp_pts = 9

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem("An evil soul that gives exp when consumed", item_type="Red Soul", value=exp_pts)
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


def gen_kelpclopse(room_range_x, room_range_y):
    """Generates a KelpClopse mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a KelpClopse mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "KelpClopse"
    creature_sprite = "A_KELPCLOPSE"
    personal_name = tcod.namegen_generate("Fantasy male")

    health = 12
    base_attack = 4
    base_defence = 1
    exp_pts = 12

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_enemy)
    item_com = itemcom.ComItem("An evil soul that gives exp when consumed", item_type="Red Soul", value=exp_pts)
    ai_com = ai.AiChase()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj


# ----- FRIENDLY MOBS ----- #

def gen_healer_slime(room_range_x, room_range_y):
    """Generates a friendly IceSlime mob on a random tile in the room specified by `room_range_x` and `room_range_y`.

    Parameters
    ----------
    room_range_x : tuple
        The (min, max) x-coordinates of the current room.
    room_range_y : tuple
        The (min, max) y-coordinates of the current room.

    Returns
    -------
    ObjActor
        An actor object with a creature component having all the stats and abilities of a IceSlime mob.

    """

    x, y = (tcod.random_get_int(0, *room_range_x), tcod.random_get_int(0, *room_range_y))

    creature_name = "IceSplime"
    creature_sprite = "A_ICESLIME"
    personal_name = tcod.namegen_generate("Fantasy female")

    base_attack = 0
    base_defence = 0
    health = 5

    creature_com = creature.ComCreature(personal_name, base_atk=base_attack, base_def=base_defence, max_hp=health,
                                        death_function=death.death_friendly)

    item_com = itemcom.ComItem("A pure soul that gives health when consumed",
                               item_type="Pure Soul", use_function=magic.cast_heal, value=2)

    ai_com = ai.AiFlee()
    mob_obj = actor.ObjActor(x, y, creature_name, creature_sprite, animation_speed=1,
                             creature=creature_com, ai=ai_com, item=item_com)
    return mob_obj

