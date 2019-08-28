from src import globalvars, actor
from src.components import itemcom, structure


def gen_stairs(coord, up=True):
    """Generates a set of stairs going up or down a floor,

    Parameters
    ----------
    coord : tuple
        The map-grid coordinate to place the stairs.
    up : bool
        True if the stairs lead up, False if the stairs lead down.

    Returns
    -------
    None

    """
    if up:
        stairs_com = structure.ComStairs()
        stairs_obj = actor.ObjActor(*coord, "Upwards stairs", "S_STAIRS_UP", stairs=stairs_com)
    else:
        stairs_com = structure.ComStairs(upwards=False)
        stairs_obj = actor.ObjActor(*coord, "Downwards stairs", "S_STAIRS_DOWN", stairs=stairs_com)

    globalvars.GAME.current_objects.insert(0, stairs_obj)


def gen_magic_rock(coord):
    """Generates the magic stone relic that triggers then end portals to open.

    Parameters
    ----------
    coord : tuple
        The map-grid coordinate to place the relic.

    Returns
    -------
    None

    """
    item_com = itemcom.ComItem()
    rock_obj = actor.ObjActor(*coord, "MAGIC ROCK", "S_MAGIC_ROCK", item=item_com)

    globalvars.GAME.current_objects.insert(0, rock_obj)


def gen_portal(coord):
    """Generates the portal that leads to winning the game.

    Parameters
    ----------
    coord : tuple
        The map-grid coordinate to place the portal.

    Returns
    -------
    None

    """
    portal_com = structure.ComPortal()
    portal_obj = actor.ObjActor(*coord, "Portal", "S_PORTAL_CLOSED", portal=portal_com)

    globalvars.GAME.current_objects.insert(0, portal_obj)
