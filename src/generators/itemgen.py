import tcod
import numpy

from src import globalvars
from src import actor
from src import magic
from src.components import itemcom


def gen_item(floor_num, tup_coords):
    """Generates a random item at the given coordinates specified by tup_coords.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated item.

    Returns:
         Inserts a randomly generated item object onto the front of the GAME.current_objects list.

    """
    item_dict = {
        #  chance between species  |    the species
        1: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_bronze(tup_coords), gen_defence_shield_wooden(tup_coords))),

        2: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_bronze(tup_coords), gen_defence_shield_wooden(tup_coords))),

        3: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_iron(tup_coords), gen_defence_shield_bronze(tup_coords))),

        4: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_iron(tup_coords), gen_defence_shield_iron(tup_coords))),

        5: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords), gen_defence_shield_steel(tup_coords))),

        6: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords),
             gen_defence_shield_steel(tup_coords))),

        7: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords),
             gen_defence_shield_steel(tup_coords))),

        8: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords),
             gen_defence_shield_steel(tup_coords))),

        9: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
             gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords),
             gen_defence_shield_steel(tup_coords))),

        10: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
             (gen_none_item(), gen_scroll_lightening(tup_coords), gen_scroll_fireball(tup_coords),
              gen_scroll_confusion(tup_coords), gen_weapon_sword_steel(tup_coords),
              gen_defence_shield_steel(tup_coords))),

    }

    # choose one of the mobs according to their spawn probability
    new_item = numpy.random.choice(item_dict[floor_num][1], p=item_dict[floor_num][0])

    if new_item:
        globalvars.GAME.current_objects.insert(0, new_item)


def gen_none_item():
    """Acts as an option for not generating any items.

    Returns:
        None
    """
    return None


# DAMAGE ITEMS


def gen_scroll_lightening(tup_coords):

    x, y = tup_coords

    damage = tcod.random_get_int(0, 3, 5)
    max_r = tcod.random_get_int(0, 7, 8)

    item_com = itemcom.ComItem(use_function=magic.cast_lightening, value=(damage, max_r))

    lightening_scroll_obj = actor.ObjActor(x, y, "Lightening Scroll",
                                           "S_SCROLL_YELLOW",
                                           item=item_com)

    return lightening_scroll_obj


def gen_scroll_fireball(tup_coords):
    x, y = tup_coords

    damage = tcod.random_get_int(0, 2, 4)
    max_r = tcod.random_get_int(0, 7, 8)
    radius = 1

    item_com = itemcom.ComItem(use_function=magic.cast_fireball, value=(damage, max_r, radius))

    fireball_scroll_obj = actor.ObjActor(x, y, "Fireball Scroll",
                                         "S_SCROLL_RED",
                                         item=item_com)

    return fireball_scroll_obj


def gen_scroll_confusion(tup_coords):
    x, y = tup_coords

    effect_len = tcod.random_get_int(0, 5, 7)

    item_com = itemcom.ComItem(use_function=magic.cast_confusion, value=effect_len)

    confusion_scroll_obj = actor.ObjActor(x, y, "Confusion Scroll",
                                          "S_SCROLL_MULTI",
                                          item=item_com)

    return confusion_scroll_obj


# WEAPON ITEMS


def gen_weapon_sword_bronze(tup_coords):
    x, y = tup_coords

    bonus = 1

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")
    sword_obj = actor.ObjActor(x, y, "Bronze Sword",
                               "S_SWORD_BRONZE",
                               equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_iron(tup_coords):
    x, y = tup_coords

    bonus = 2

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")
    sword_obj = actor.ObjActor(x, y, "Iron Sword",
                               "S_SWORD_IRON",
                               equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_steel(tup_coords):
    x, y = tup_coords

    bonus = 3

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")
    sword_obj = actor.ObjActor(x, y, "Steel Sword",
                               "S_SWORD_STEEL",
                               equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_black(tup_coords):
    x, y = tup_coords

    bonus = 5

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")
    sword_obj = actor.ObjActor(x, y, "Black Sword",
                               "S_SWORD_BLACK",
                               equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_rune(tup_coords):
    x, y = tup_coords

    bonus = 7

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")
    sword_obj = actor.ObjActor(x, y, "Rune Sword",
                               "S_SWORD_RUNE",
                               equipment=equipment_com)

    return sword_obj


# DEFENCE ITEMS


def gen_defence_shield_wooden(tup_coords):
    x, y = tup_coords

    bonus = 1

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Wooden Shield",
                                "S_SHIELD_WOODEN",
                                equipment=equipment_com)

    return shield_obj


def gen_defence_shield_bronze(tup_coords):
    x, y = tup_coords

    bonus = 2

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Bronze Shield",
                                "S_SHIELD_BRONZE",
                                equipment=equipment_com)

    return shield_obj


def gen_defence_shield_iron(tup_coords):
    x, y = tup_coords

    bonus = 3

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Iron Shield",
                                "S_SHIELD_IRON",
                                equipment=equipment_com)

    return shield_obj


def gen_defence_shield_steel(tup_coords):
    x, y = tup_coords

    bonus = 4

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Steel Shield",
                                "S_SHIELD_STEEL",
                                equipment=equipment_com)

    return shield_obj


def gen_defence_shield_black(tup_coords):
    x, y = tup_coords

    bonus = 6

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Black Shield",
                                "S_SHIELD_BLACK",
                                equipment=equipment_com)

    return shield_obj


def gen_defence_shield_rune(tup_coords):
    x, y = tup_coords

    bonus = 8

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")
    shield_obj = actor.ObjActor(x, y, "Rune Shield",
                                "S_SHIELD_RUNE",
                                equipment=equipment_com)

    return shield_obj


def gen_coins(tup_coords, amount):
    x, y = tup_coords

    item_com = itemcom.ComItem(type_item="gold", value=amount)
    obj = actor.ObjActor(x, y, "Gold", "S_GOLD", item=item_com)

    return obj
