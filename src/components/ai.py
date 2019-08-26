import tcod

from src import constants, globalvars, game


class AiConfuse:
    """Ai component class that makes a creature actor walk in random directions.

    Attributes:
        original_ai (arg, Ai class): The ai component the actor had originally before being set to AiConfuse.
        num_turns (arg, int): The number of turns it takes before the affected creature's ai is reset to original_ai.
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to True.

    """

    def __init__(self, original_ai, num_turns):
        self.original_ai = original_ai
        self.num_turns = num_turns
        self.hurt_kin = True

    def take_turn(self):
        """Performs one move action towards a random direction/tile.

        Resets the affected creature's ai to its previous (normal) ai after num_turns have been exhausted to 0.

        Returns:
            Displays a game message when the creature actor has broken free of this AiConfuse.

        """

        if self.num_turns > 0:
            # default (0) random gen
            self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

            self.num_turns -= 1

        # reset creature's ai
        else:
            self.owner.ai = self.original_ai
            game.game_message("{} has broken out of its confusion!".format(self.owner.display_name), constants.COLOR_YELLOW)


class AiChase:
    """Ai component class for enemy creatures that chases the PLAYER and attacks when the it is next to the PLAYER.

    Attributes:
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to False.

    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action towards the PLAYER's current location when the creature is in the PLAYER's fov.

        When the creature is adjacent to the PLAYER, attack. Prevents creatures from hurt other creatures when moving
        towards PLAYER together (implemented in the move() method of ComCreature).

        """

        monster = self.owner

        distance = monster.distance_to(globalvars.PLAYER)

        # when the monster creature is in the field of vision of the player or is 6 radius within the player
        if tcod.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y) or distance <= 6:

            # move towards player
            if distance >= 2:
                monster.creature.move_towards(globalvars.PLAYER)

            else:
                monster.creature.attack(globalvars.PLAYER)


class AiFlee:
    """Ai component class for enemy creatures that chases the PLAYER and attacks when the it is next to the PLAYER.

    Attributes:
        hurt_kin (bool): True if the ai is allowed to make the creature hurt its own kind/type. Default set to False.

    """
    def __init__(self):
        self.hurt_kin = False

    def take_turn(self):
        """Performs one move action towards the PLAYER's current location when the creature is in the PLAYER's fov.

        When the creature is adjacent to the PLAYER, attack. Prevents creatures from hurt other creatures when moving
        towards PLAYER together (implemented in the move() method of ComCreature).

        """

        monster = self.owner

        distance = monster.distance_to(globalvars.PLAYER)

        # when the monster creature is in the field of vision of the player
        if tcod.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y) and distance <= 2:

            # move away from player
            monster.creature.move_away(globalvars.PLAYER)
