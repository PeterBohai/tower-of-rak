import tcod

from src import constants, globalvars, game


class AiConfuse:
    """Ai component class that makes a creature actor walk in random directions.

    Attributes
    ----------
    original_ai : ai obj
        The ai component object that the actor originally had before being set to this one.
    num_turns : int
        Number of turns before the affected creature's ai is reset to `original_ai`.
    hurt_kin : bool
        True if the creature is allowed to hurt other creatures while confused. Default is True.

    """

    def __init__(self, original_ai, num_turns):
        self.original_ai = original_ai
        self.num_turns = num_turns
        self.hurt_kin = True

    def take_turn(self):
        """Performs one move action towards a random adjacent tile.

        Resets ai component to `original_ai` after `num_turns` reaches 0.

        Returns
        -------
        None
        """
        if self.num_turns > 0:
            self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        else:
            self.owner.ai = self.original_ai
            game.game_message(f"{self.owner.display_name} has broken out of its confusion!",
                              constants.COLOR_YELLOW)


class AiChase:
    """Ai component class that chases the PLAYER and attacks when adjacent to the PLAYER.

    Attributes
    ----------
    hurt_kin : bool
        True if the creature is allowed to hurt other creatures when chasing. Default is False.
    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action towards the PLAYER's current location.

        Creature only takes a turn if it is in the PLAYER's fov or 6 tiles and less away from the
        PLAYER. When the creature is adjacent to the PLAYER, attack. Creatures are prevented from
        hurting other creatures when moving towards PLAYER
        (implemented in the move() method of ComCreature).
        """
        mob = self.owner
        distance = mob.distance_to(globalvars.PLAYER)

        if tcod.map_is_in_fov(globalvars.FOV_MAP, mob.x, mob.y) or distance <= 6:
            if distance >= 2:
                mob.creature.move_towards(globalvars.PLAYER)
            else:
                mob.creature.attack(globalvars.PLAYER)


class AiFlee:
    """Ai component class that is non-aggressive and moves away from the PLAYER.

    Attributes
    ----------
    hurt_kin : bool
        True if the creature is allowed to hurt other creatures when fleeing. Default is False.
    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action away from the PLAYER's current location.

        Creature takes a turn when it is in the PLAYER's fov and 2 tiles or less from the PLAYER.
        """
        mob = self.owner
        distance = mob.distance_to(globalvars.PLAYER)

        if tcod.map_is_in_fov(globalvars.FOV_MAP, mob.x, mob.y) and distance <= 2:
            mob.creature.move_away(globalvars.PLAYER)
