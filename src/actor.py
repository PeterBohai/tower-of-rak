import math

import tcod

from src import constants, globalvars, game


class ObjActor:
    """An actor object class that essentially represents every entity in the game.

    This is an object that can be anything that appears in the game (except for walls and floors) and is differentiated
    mainly through the components that make up and control the object.
    Note that this rouge-like game mainly uses the composition/component system over inheritance.

    Attributes
    ----------
    x : int
        The x-coordinate of the object in terms of map tiles (grid not pixels).
    y : int
        The y-coordinate of the object in terms of map tiles (grid not pixels).
    object_name : str
        Name of the object.
    _animation_key :  str
        The actor object's animation key to access its sprite sequence from the animation dictionary in the assets.
    _animation_seq : list
        The sequence of sprites to be cycled through that make up the animation of the object.
    animation_index : int
        The current index of the animation sequence list to be displayed (a single still sprite).
    animation_speed : float, optional
        Time in seconds it takes to loop through one object animation iteration. Larger number means slower animation.
    sprite_time_elapsed : float
        Time in seconds the current sprite has been displayed for.
    _exp_total : int, optional
        Total experience points of the actor object (mainly for creatures).
    gold : int, optional
        Total gold value the actor object currently contains/owns.
    status : str, optional
        The status of the object that help initiate different behaviours for different statuses (eg. STATUS_OPEN)
    _level : int
        Current level of actor (usually PLAYER).
    exp_to_next_total : int
        Number of total exp points needed to reach the next level.
    creature: object, optional
        A component class (ComCreature) that gives the object creature-specific attributes and functionality.
    ai: object, optional
        A component class that gives the object the ability to move and act on their own.
    container: object, optional
        A component class (ComContainer) that gives the object an inventory (hold more than one item).
    item: object, optional
        A component class (ComItem) that gives the object attributes and functionality of items (pick/drop/use).
    equipment: object, optional
        A component class (ComEquipment) that gives the object equipment attributes (wear/bonuses).
    stairs: object, optional
        A structure component class (ComStairs) that gives the object staircase attributes (move up/down floors).
    portal: object, optional
        A structure component class (ComPortal) that gives the object portal attributes (enter/win the game).

    """

    def __init__(self, x, y, object_name,
                 animation_key, animation_speed=0.5,
                 exp_total=0, gold=0,
                 status=None,
                 creature=None,
                 ai=None,
                 container=None,
                 item=None,
                 equipment=None,
                 stairs=None,
                 portal=None):

        self.x = x
        self.y = y
        self.object_name = object_name

        self._animation_key = animation_key
        self._animation_seq = globalvars.ASSETS.animation_dict[self._animation_key]
        self.animation_index = 0
        self.animation_speed = animation_speed
        self.sprite_time_elapsed = 0.0

        self._exp_total = exp_total
        self.gold = gold
        self.status = status
        self._level = 1
        self.exp_to_next_total = exp_chart[self._level]

        # components
        self.creature = creature
        if creature:
            self.creature.owner = self

            # coordinates for the disappearing damage taken float number
            self.dmg_taken_posx = self.x * constants.CELL_WIDTH + int(constants.CELL_WIDTH / 2)
            self.dmg_taken_posy = self.y * constants.CELL_HEIGHT

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

        self.portal = portal
        if self.portal:
            self.portal.owner = self

    @property
    def animation_key(self):
        """str: Gets the animation key that accesses the sprite sequence from the animation dictionary in the assets.

        When the animation key is set, the animation sequence will also be reset accordingly.
        """
        return self._animation_key

    @animation_key.setter
    def animation_key(self, value):
        self._animation_key = value
        self._animation_seq = globalvars.ASSETS.animation_dict[self._animation_key]

    @property
    def time_per_sprite(self):
        """float: Gets the time one still image sprite should be displayed for."""
        return self.animation_speed / len(self._animation_seq)

    @property
    def display_name(self):
        """str: Gets the combined creature names and their object (type) name."""

        if self.creature is not None:
            name_to_display = f"{self.creature.personal_name} the {self.object_name}"

            if self is globalvars.PLAYER:
                name_to_display = self.creature.personal_name

        else:
            name_to_display = self.object_name

        return name_to_display

    @property
    def is_visible(self):
        """bool: Returns True if this object is in the field of view of the PLAYER, False otherwise."""
        return tcod.map_is_in_fov(globalvars.FOV_MAP, self.x, self.y)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level
        self.exp_to_next_total = exp_chart[self._level]

    @property
    def exp_total(self):
        return self._exp_total

    @exp_total.setter
    def exp_total(self, new_exp):
        gained = new_exp - self._exp_total
        if self._level != constants.PLAYER_MAX_LV:
            self._exp_total = new_exp
            game.game_message(f"Gained {gained} experience points.", constants.COLOR_BLUE3)
        else:
            game.game_message(f"Already at max level, no exp was gained", constants.COLOR_RED)

        game.game_message(f"Player has {self._exp_total} experience total.", constants.COLOR_WHITE)
        if self._exp_total >= self.exp_to_next_total:
            self.creature.level_up()

    @property
    def exp(self):
        return self._exp_total - exp_chart[self._level - 1]

    @property
    def exp_to_next(self):
        return self.exp_to_next_total - exp_chart[self._level - 1]

    def draw(self, surface):
        """Draws the actor object to the screen.

        Draws the actor object to the map screen if it appears within the PLAYER's fov. If the object has multiple
        sprites in its animation list, it keeps track of the timing of the animations and triggers a transition to
        display the next image in the list. This will give off an "idle" animation look, where creatures usually bob up
        and down.

        Parameters
        ----------
        surface : pygame Surface obj
            The surface that the button will be drawn on.

        Returns
        -------
        None

        """

        if surface is globalvars.SURFACE_MAP:
            blit_x = self.x * constants.CELL_WIDTH
            blit_y = self.y * constants.CELL_HEIGHT
        else:
            blit_x = self.x
            blit_y = self.y

        if self.is_visible:
            if len(self._animation_seq) == 1:
                self.animation_index = 0

            elif len(self._animation_seq) > 1:
                if globalvars.CLOCK.get_fps() > 0.0:
                    self.sprite_time_elapsed += 1/globalvars.CLOCK.get_fps()

                if self.sprite_time_elapsed >= self.time_per_sprite:
                    self.sprite_time_elapsed = 0.0

                    if self.animation_index >= len(self._animation_seq) - 1:
                        self.animation_index = 0
                    else:
                        self.animation_index += 1

            surface.blit(self._animation_seq[self.animation_index], (blit_x, blit_y))

    def distance_to(self, other):
        """Calculates the relative distance of this object to another (other).

        Parameters
        ----------
        other : ObjActor
            Another actor object.

        Returns
        -------
        float
            The direct (straight diagonal) distance to the other actor object.

        """

        dx = other.x - self.x
        dy = other.y - self.y

        shortest_distance_to_other = math.sqrt(dx ** 2 + dy ** 2)

        return shortest_distance_to_other

    def animation_del(self):
        """Removes all animation assets (pygame.Surface objects).

        For the purpose of being able to save GAME.current_objects with pickle.

        Returns
        -------
        None

        """

        self._animation_seq = None

    def animation_init(self):
        """Sets animation back to referencing animations from ASSETS (and not None after animation_del).

        Returns
        -------
        None

        """

        self._animation_seq = globalvars.ASSETS.animation_dict[self._animation_key]


# Total exp to get to before reaching the next level
exp_chart = {
    0: 0,
    1: 10,
    2: 30,
    3: 70,
    4: 130,
    5: 220,
    6: 355,
    7: 557,
    8: 860,
    9: 1315,
    10: 1998,
    11: 3022,
    12: 4302,
    13: 5902,
    14: 7902,
    15: 10402,
    16: 13527,
    17: 17433,
    18: 22315,
    19: 27807
}