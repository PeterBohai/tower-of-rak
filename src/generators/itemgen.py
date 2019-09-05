import tcod
import numpy

from src import globalvars
from src import actor
from src import magic
from src.components import itemcom


def gen_item(floor_num, coord):
    """Generates a random item at the given coordinates specified by coord.

    Inserts a randomly generated item object onto the front of the GAME.current_objects list.

    Parameters
    ----------
    floor_num : int
        The current floor number that the room is on.
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    None

    """
    item_dict = {
        #  chance between items  |    the different items
        1: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_bronze(coord), gen_defence_shield_wooden(coord))),

        2: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_bronze(coord), gen_defence_shield_wooden(coord))),

        3: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_iron(coord), gen_defence_shield_bronze(coord))),

        4: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_iron(coord), gen_defence_shield_iron(coord))),

        5: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_steel(coord), gen_defence_shield_steel(coord))),

        6: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_steel(coord),
             gen_defence_shield_steel(coord))),

        7: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_steel(coord),
             gen_defence_shield_steel(coord))),

        8: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_steel(coord),
             gen_defence_shield_steel(coord))),

        9: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
            (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
             gen_scroll_confusion(coord), gen_weapon_sword_steel(coord),
             gen_defence_shield_steel(coord))),

        10: ((0.15, 0.25, 0.25, 0.15, 0.1, 0.1),
             (gen_none_item(), gen_scroll_lightening(coord), gen_scroll_fireball(coord),
              gen_scroll_confusion(coord), gen_weapon_sword_steel(coord),
              gen_defence_shield_steel(coord))),
    }

    # choose one of the items according to their spawn probability
    new_item = numpy.random.choice(item_dict[floor_num][1], p=item_dict[floor_num][0])

    if new_item:
        globalvars.GAME.current_objects.insert(0, new_item)


def gen_none_item():
    """Acts as an option for not generating any items.

    Returns
    -------
    None

    """
    return None


# DAMAGE ITEMS
def gen_scroll_lightening(coord):
    """Generates a Lightening Scroll item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Lightening Scroll.

    """
    x, y = coord

    damage = tcod.random_get_int(0, 3, 5)
    max_r = tcod.random_get_int(0, 7, 8)
    description = "Casts a lightening spell at enemies."

    item_com = itemcom.ComItem(description, use_function=magic.cast_lightening, value=(damage, max_r))
    lightening_scroll_obj = actor.ObjActor(x, y, "Lightening Scroll", "S_SCROLL_YELLOW", item=item_com)

    return lightening_scroll_obj


def gen_scroll_fireball(coord):
    """Generates a Fireball Scroll item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Fireball Scroll.

    """
    x, y = coord

    damage = tcod.random_get_int(0, 2, 4)
    max_r = tcod.random_get_int(0, 7, 8)
    radius = 1
    description = "Casts a fireball spell at enemies."

    item_com = itemcom.ComItem(description, use_function=magic.cast_fireball, value=(damage, max_r, radius))
    fireball_scroll_obj = actor.ObjActor(x, y, "Fireball Scroll", "S_SCROLL_RED", item=item_com)

    return fireball_scroll_obj


def gen_scroll_confusion(coord):
    """Generates a Confusion Scroll item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Confusion Scroll.

    """
    x, y = coord

    effect_len = tcod.random_get_int(0, 5, 7)
    description = "Casts a confusion spell at enemies...or yourself, but why."

    item_com = itemcom.ComItem(description, use_function=magic.cast_confusion, value=effect_len)
    confusion_scroll_obj = actor.ObjActor(x, y, "Confusion Scroll", "S_SCROLL_MULTI", item=item_com)

    return confusion_scroll_obj


# WEAPON ITEMS
def gen_weapon_sword_bronze(coord):
    """Generates a Bronze Sword item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Bronze Sword.

    """
    x, y = coord

    bonus = 1
    description = "A relatively weak sword made of bronze but still as sharp as a knife so watch your fingers."

    item_com = itemcom.ComItem(description)
    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="weapon")
    sword_obj = actor.ObjActor(x, y, "Bronze Sword", "S_SWORD_BRONZE", item=item_com, equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_iron(coord):
    """Generates an Iron Sword item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of an Iron Sword.

    """
    x, y = coord

    bonus = 2
    description = "A sturdy sword made of iron that can definitely cut your fingers, so watch out."

    item_com = itemcom.ComItem(description)
    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="weapon")
    sword_obj = actor.ObjActor(x, y, "Iron Sword", "S_SWORD_IRON", item=item_com, equipment=equipment_com)
    return sword_obj


def gen_weapon_sword_steel(coord):
    """Generates a Steel Sword item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Steel Sword.

    """
    x, y = coord

    bonus = 3
    description = "A shiny sword made of steel that can easily cut through most things, including your fingers!"

    item_com = itemcom.ComItem(description)
    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="weapon")
    sword_obj = actor.ObjActor(x, y, "Steel Sword", "S_SWORD_STEEL", item=item_com, equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_black(coord):
    """Generates a Black Sword item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Black Sword.

    """
    x, y = coord

    bonus = 5

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="weapon")
    sword_obj = actor.ObjActor(x, y, "Black Sword", "S_SWORD_BLACK", equipment=equipment_com)

    return sword_obj


def gen_weapon_sword_rune(coord):
    """Generates a Rune Sword item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Rune Sword.

    """
    x, y = coord

    bonus = 7

    equipment_com = itemcom.ComEquipment(attack_bonus=bonus, slot="weapon")
    sword_obj = actor.ObjActor(x, y, "Rune Sword", "S_SWORD_RUNE", equipment=equipment_com)

    return sword_obj


# DEFENCE ITEMS
def gen_defence_shield_wooden(coord):
    """Generates a Wooden Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Wooden Shield.

    """
    x, y = coord

    bonus = 1
    description = "The goddamn weakest shield one can pick up. But hey, it's better than " \
                  "blocking with your scrawny elbows right?"

    item_com = itemcom.ComItem(description)
    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Wooden Shield", "S_SHIELD_WOODEN", item=item_com, equipment=equipment_com)

    return shield_obj


def gen_defence_shield_bronze(coord):
    """Generates a Bronze Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Bronze Shield.

    """
    x, y = coord

    bonus = 2
    description = "A slightly better shield than the wooden one but not much better."

    item_com = itemcom.ComItem(description)
    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Bronze Shield", "S_SHIELD_BRONZE", item=item_com, equipment=equipment_com)

    return shield_obj


def gen_defence_shield_iron(coord):
    """Generates a Iron Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Iron Shield.

    """
    x, y = coord

    bonus = 3

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Iron Shield", "S_SHIELD_IRON", equipment=equipment_com)

    return shield_obj


def gen_defence_shield_steel(coord):
    """Generates a Steel Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Steel Shield.

    """
    x, y = coord

    bonus = 4

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Steel Shield", "S_SHIELD_STEEL", equipment=equipment_com)

    return shield_obj


def gen_defence_shield_black(coord):
    """Generates a Black Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Black Shield.

    """
    x, y = coord

    bonus = 6

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Black Shield", "S_SHIELD_BLACK", equipment=equipment_com)

    return shield_obj


def gen_defence_shield_rune(coord):
    """Generates a Rune Shield item on a random tile in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties and abilities of a Rune Shield.

    """
    x, y = coord

    bonus = 8

    equipment_com = itemcom.ComEquipment(defence_bonus=bonus, slot="shield")
    shield_obj = actor.ObjActor(x, y, "Rune Shield", "S_SHIELD_RUNE", equipment=equipment_com)

    return shield_obj


def gen_coins(coord, amount):
    """Generates `amount` of coins in the room specified by `coord`

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the generated item.
    amount : int
        Value of the coins.

    Returns
    -------
    ObjActor
        An actor object with an item component having all the properties of gold coins.

    """
    x, y = coord

    item_com = itemcom.ComItem("Gold coins that can be spent.", item_type="gold", value=amount)
    obj = actor.ObjActor(x, y, "Gold", "S_GOLD", item=item_com)

    return obj
