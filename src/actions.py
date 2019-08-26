from src import globalvars, map


def use_stairs():
    # check if the player is standing on top of a set of stairs
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
    objs_at_player = map.objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
    # only pick up the top most object that is an item
    for obj in reversed(objs_at_player):
        if obj.item:
            obj.item.pick_up(globalvars.PLAYER)
            break


def drop_item():
    if len(globalvars.PLAYER.container.inventory) > 0:
        globalvars.PLAYER.container.inventory[-1].item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)
