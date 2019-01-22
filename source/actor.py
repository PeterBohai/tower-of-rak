# Standard library imports
import math

# Third party imports
import tcod

# Local project imports
from source import constants, globalvars
from source.components import itemcom


class ObjActor:
    """An actor object class that essentially represents every entity in the game.

    This is an object that can be anything that appears in the game and is differentiated mainly through the components
    that make up and control the object.
    Note that this rouge-like game mainly uses the composition/component system over inheritance.

    Attributes:
        x (arg, int): Tile map address of the actor object on the x-axis.
        y (arg, int): Tile map address of the actor object on the y-axis.
        name_object (arg, str): Name of the object type, "scroll" or "snake" for example.
        animation (list): List of images for the object's display (can be a list of one image).
                          Created in the ObjAssets class and usually denoted as "A_..." or "S_...".
        animation_speed (arg, float): Time in seconds it takes to loop through the object animation.
                                      Default value is initialized as 0.5

    Components:
        creature: Created from the ComCreature class. Has health, and can move and fight.
        ai: Created from classes that have the prefix "Ai" like AiChase. Gives actor object specific rules to follow.
        container: Created from the ComContainer class. Gives actor object ability to have an inventory.
        item: Created from the ComItem class. Gives actor objects the ability to be picked up and be potentially usable.

    """

    def __init__(self, x, y,
                 name_object,
                 animation_key,
                 animation_speed=0.5,
                 status=None,
                 creature=None,
                 ai=None,
                 container=None,
                 item=None,
                 equipment=None,
                 stairs=None,
                 portal=None):   # None is implicitly False

        self.x = x  # map address (not pixel address)
        self.y = y  # map address (not pixel address)
        self.name_object = name_object  # name of object, might change to object_name or name_object_type
        self.animation_key = animation_key
        self.animation = globalvars.ASSETS.animation_dict[animation_key]
        self.animation_speed = animation_speed/1.0   # in seconds (always converted to a float, even if its an int)
        self.status = status

        # animation flicker speed (over the course of # of secs)
        self.flicker_speed = self.animation_speed/len(self.animation)   # amount of display time for each img
        self.flicker_timer = 0.0
        self.sprite_image = 0

        self.creature = creature
        if creature:
            self.creature.owner = self   # component system implementation

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:    # if it has a container component, then...
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            # automatically give item component to equipment actor object
            self.item = itemcom.ComItem()
            self.item.owner = self

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

        self.portal = portal
        if self.portal:
            self.portal.owner = self

    @property
    def display_name(self):
        """Combines creature names and their object (type) name. Adds the "[E]" indicator for equipped items.

        Returns:
            name_to_display (str): The full name of a creature or the equip status of an equipment item.

        """

        if self.creature:
            name_to_display = "{} the {}".format(self.creature.name_instance, self.name_object)
            return name_to_display

        if self.item:
            if self.equipment and self.equipment.equipped is True:
                name_to_display = "{} [E]".format(self.name_object)
                return name_to_display
            else:
                name_to_display = self.name_object
                return name_to_display

    def draw(self):
        """Draws the actor object to the screen.

        Draws the actor object to the map screen if it appears within the PLAYER's fov. If the object as multiple sprite
        images in its animation list, it keeps track of the timing of the animations and triggers a transition to
        display the next image in the list. This will give off an "idle" animation look, where creatures usually bob up
        and down.

        """

        is_visible = tcod.map_is_in_fov(globalvars.FOV_MAP, self.x, self.y)
        if is_visible:
            if len(self.animation) == 1:
                # pixel address
                globalvars.SURFACE_MAP.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

            elif len(self.animation) > 1:
                if globalvars.CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1/globalvars.CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0
                    else:
                        self.sprite_image += 1

            # fixes rare occurrence when self.sprite_image is 1 when len(self.animation) changed from 2 to 1 already,
            # which caused index out of bounds error
            if len(self.animation) == 1:
                self.sprite_image = 0

            globalvars.SURFACE_MAP.blit(self.animation[self.sprite_image],
                              (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def distance_to(self, other):
        """Calculates the relative distance of this actor object to another.

        Args:
            other (ObjActor): Another actor object.

        Returns:
            shortest_distance_to_other (float): The straight distance to the "other" actor object.

        """

        dx = other.x - self.x
        dy = other.y - self.y

        # shortest distance to another actor object in tile number measurements
        shortest_distance_to_other = math.sqrt(dx ** 2 + dy ** 2)

        return shortest_distance_to_other

    def move_towards(self, other):
        """Moves this actor object closer towards another object.

            Used in the AiChase to chase after a specified actor object.
            Uses the move() method in the ComCreature component class.

        Args:
            other (ObjActor): Target actor object to move towards

        """

        dx = other.x - self.x
        dy = other.y - self.y

        # shortest distance to another actor object in tile number measurements
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        self.creature.move(dx, dy)

    def move_away(self, other):
        """Moves this actor object away from another object.

            Used in the AiFlee to get away from a specified actor object.
            Uses the move() method in the ComCreature component class.

        Args:
            other (ObjActor): Target actor object to move towards

        """

        dx = self.x - other.x
        dy = self.y - other.y

        # shortest distance to another actor object in tile number measurements
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        self.creature.move(dx, dy)

    def animation_del(self):
        """ Get rid of any animation assets.

        For the purpose of avoiding pygame.Surface objects dump, which can't be pickled.

        Returns:
            None

        """

        self.animation = None

    def animation_init(self):
        """ Sets animation back to referencing animations from ASSETS (and not None after animation_del)

        Returns:
            None
        """

        self.animation = globalvars.ASSETS.animation_dict[self.animation_key]