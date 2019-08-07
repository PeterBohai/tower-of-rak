# Third party imports
import tcod

# Local project imports
from source import globalvars, actor, magic
from source.components import itemcom


def gen_item(tup_coords):
    """Generates a random item at the given coordinates specified by tup_coords.

    Args:
        tup_coords (tuple): The map tile coordinates to place the generated item.

    Returns:
         Inserts a randomly generated item object onto the front of the GAME.current_objects list.

    """

    choice_num = tcod.random_get_int(0, 1, 5)

    if choice_num == 1:
        new_item = gen_scroll_lightening(tup_coords)
    elif choice_num == 2:
        new_item = gen_scroll_fireball(tup_coords)
    elif choice_num == 3:
        new_item = gen_scroll_confusion(tup_coords)
    elif choice_num == 4:
        new_item = gen_weapon_sword(tup_coords)
    else:
        new_item = gen_armour_shield(tup_coords)

    # new_item = gen_scroll_lightening(tup_coords)
    globalvars.GAME.current_objects.insert(0, new_item)


def gen_scroll_lightening(tup_coords):

    x, y = tup_coords

    damage = tcod.random_get_int(0, 3, 5)
    max_r = tcod.random_get_int(0, 7, 8)

    item_com = itemcom.ComItem(use_function=magic.cast_lightening, value=(damage, max_r))

    lightening_scroll_obj = actor.ObjActor(x, y, "Lightening Scroll",
                                     "S_SCROLL_1",
                                     item=item_com)

    return lightening_scroll_obj


def gen_scroll_fireball(tup_coords):
    x, y = tup_coords

    damage = tcod.random_get_int(0, 2, 4)
    max_r = tcod.random_get_int(0, 7, 8)
    radius = 1

    item_com = itemcom.ComItem(use_function=magic.cast_fireball, value=(damage, max_r, radius))

    fireball_scroll_obj = actor.ObjActor(x, y, "Fireball Scroll",
                                         "S_SCROLL_2",
                                         item=item_com)

    return fireball_scroll_obj


def gen_scroll_confusion(tup_coords):
    x, y = tup_coords

    effect_len = tcod.random_get_int(0, 5, 7)

    item_com = itemcom.ComItem(use_function=magic.cast_confusion, value=effect_len)

    confusion_scroll_obj = actor.ObjActor(x, y, "Confusion Scroll",
                                          "S_SCROLL_3",
                                          item=item_com)

    return confusion_scroll_obj


def gen_weapon_sword(tup_coords):
    x, y = tup_coords

    bonus = tcod.random_get_int(0, 1, 2)

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="Right Hand")

    sword_obj = actor.ObjActor(x, y, "Small Sword",
                               "S_32_SWORD",
                               equipment=equipment_com)

    return sword_obj


def gen_armour_shield(tup_coords):
    x, y = tup_coords

    bonus = tcod.random_get_int(0, 1, 2)

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="Left Hand")

    shield_obj = actor.ObjActor(x, y, "Small Shield",
                                "S_32_SHIELD",
                                equipment=equipment_com)

    return shield_obj


def gen_coins(tup_coords, amount):
    x, y = tup_coords

    item_com = itemcom.ComItem(type_item="gold", value=amount)

    obj = actor.ObjActor(x, y, "Gold", "S_GOLD", item=item_com)

    return obj
