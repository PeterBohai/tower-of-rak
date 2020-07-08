from src import globalvars, map


def use_stairs():
    """Checks to see if PLAYER is on a set of stairs/portal and invokes the respective actions.

    Returns
    -------
    str
        Either the status "Just Changed Floors" or None.
    """
    objs_at_player = map.objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)

    for obj in objs_at_player:
        # check if the object contains a stairs component
        if obj.stairs:
            obj.stairs.use()
            globalvars.FLOOR_CHANGED = True
            return "Just Changed Floors"

        if obj.portal:
            obj.portal.use()

    globalvars.FLOOR_CHANGED = False


def move_one_tile(direction):
    """Sets the dx, dy according to the `direction` and passes them to the PLayer's move method.

    Parameters
    ----------
    direction : str
        The direction that the PLAYER wants to go.

    Returns
    -------
    None
    """
    if direction == "up":
        dx, dy = 0, -1
    elif direction == "down":
        dx, dy = 0, 1
    elif direction == "left":
        dx, dy = -1, 0
    elif direction == "right":
        dx, dy = 1, 0
    globalvars.PLAYER.creature.move(dx, dy)
    globalvars.FOV_CALCULATE = True


def grab_item():
    """Invokes the pick_up method for the PLAYER and ensures the topmost object is taken.

    Returns
    -------
    None

    """
    objs_at_player = map.objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)

    # only pick up the top most object that is an item
    for obj in reversed(objs_at_player):
        if obj.item:
            obj.item.pick_up(globalvars.PLAYER)
            break


def drop_item():
    """Invokes the drop method for the PLAYER and ensures the item is dropped appropriately.

    Returns
    -------
    None

    """
    if len(globalvars.PLAYER.container.inventory) > 0:
        globalvars.PLAYER.container.inventory[-1].item.drop(globalvars.PLAYER.x,
                                                            globalvars.PLAYER.y)

