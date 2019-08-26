from src import globalvars, actor
from src.components import itemcom, structure


def gen_stairs(tup_coords, up=True):
    """ Generates a set of stairs going up or down a level/map.

    Args:
        tup_coords (tuple): The map tile coordinates the stairs will be placed.
        up (bool): Specifies if the stairs will lead up or down. Default is set to True, which means stairs going up.

    Returns:
        None

    """

    x, y = tup_coords

    if up:
        stairs_com = structure.ComStairs()
        stairs_obj = actor.ObjActor(x, y, "Upwards stairs",
                                    "S_STAIRS_UP",
                                    stairs=stairs_com)
    else:
        stairs_com = structure.ComStairs(upwards=False)
        stairs_obj = actor.ObjActor(x, y, "Upwards stairs",
                                    "S_STAIRS_DOWN",
                                    stairs=stairs_com)

    globalvars.GAME.current_objects.insert(0, stairs_obj)


def gen_magic_rock(tup_coords):
    x, y = tup_coords

    item_com = itemcom.ComItem()
    rock_obj = actor.ObjActor(x, y, "MAGIC ROCK",
                              "S_MAGIC_ROCK",
                              item=item_com)

    globalvars.GAME.current_objects.insert(0, rock_obj)


def gen_portal(tup_coords):

    x, y = tup_coords

    portal_com = structure.ComPortal()
    portal_obj = actor.ObjActor(x, y, "Portal",
                                "S_PORTAL_CLOSED",
                                portal=portal_com)

    globalvars.GAME.current_objects.insert(0, portal_obj)
