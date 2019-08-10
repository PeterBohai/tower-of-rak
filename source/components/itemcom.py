
# Local project imports
from source import constants, globalvars, game, map


class ComItem:
    """Item component gives actor objects the property of being picked up and used.

    Attributes:
        weight (arg, float): The weight of the object with precision of one decimal point.
        volume (arg, float): The volume of the object with precision of one decimal point.
        use_function (arg, func): Optional argument that specifies the function to be executed when an item object is
                                  used. These use functions have the form use_function(target/caster, value).
        value (arg, int or tuple): Optional argument that gives the value to be passed into the use_function.

    """

    def __init__(self, weight=0.0,
                 volume=0.0,
                 type_item=None,                         # consumable, magic, gold, equipment
                 use_function=None,
                 value=0):

        self.weight = weight
        self.volume = volume
        self.value = value      # gold amount or exp
        self.type_item = type_item
        self.use_function = use_function
        self.container = None
        # self.owner = self.owner

    def pick_up(self, actor):
        """Picks up the item object and places it into specified actor's container inventory.

        Appends item to actor's inventory (list) in its container component and removes the items from the list of
        current_objects in GAME (ObjGame). Displays appropriate messages indicating whether the item can be picked up.
        This method is linked to the keyboard shortcut key "g".

        Args:
            actor (ObjActor): The actor that is picking up the item (the actor object with a container component
                              that the item will append itself).

        """
        if self.type_item == "gold":
            globalvars.ASSETS.sfx_coin_pickup.play()
            actor.gold += self.value
            self.owner.animation_del()
            globalvars.GAME.current_objects.remove(self.owner)
            game.game_message(f"Gained {self.value} gold.", constants.COLOR_YELLOW)
            game.game_message(f"Player now has {actor.gold} gold total.", constants.COLOR_WHITE)
            return
        elif self.type_item == "Red Soul":
            globalvars.ASSETS.sfx_soul_consume.play()
            actor.exp += self.value
            globalvars.GAME.current_objects.remove(self.owner)
            game.game_message(f"Gained {self.value} experience points.", constants.COLOR_BLUE3)
            game.game_message(f"Player now has {actor.exp} experience total.", constants.COLOR_WHITE)
            return

        if actor.container:
            if self.type_item == "Pure Soul":
                globalvars.ASSETS.sfx_pure_soul_consume.play()
                actor.container.inventory.append(self.owner)
                self.container = actor.container
                self.use()
                globalvars.GAME.current_objects.remove(self.owner)

                return

            if actor.container.volume + self.volume > actor.container.max_volume:
                game.game_message("Not enough room to pick up", constants.COLOR_WHITE)

            else:
                game.game_message("Picking up [{}]".format(self.owner.name_object))
                actor.container.inventory.append(self.owner)

                self.owner.animation_del()

                # remove from global map and list of objects in the game
                globalvars.GAME.current_objects.remove(self.owner)
                self.container = actor.container


    def drop(self, new_x, new_y):
        """Drops the item object onto the ground specified by the coordinate arguments.

        Removes the item object from the actor's inventory that the item is being contained in and places it into the
        GAME's current_object list. Displays a game message indicating which object has been dropped.

        Args:
            new_x (int): The x-coord on the map to drop the item (usually PLAYER's current position).
            new_y (int): The y-coord on the map to drop the item (usually PLAYER's current position).

        Returns:
            A game message that says the item is dropped.

        """

        # inserting underneath any creature or PLAYER but above any objects already on that tile
        insert_position = 0
        for i, obj in enumerate(reversed(globalvars.GAME.current_objects)):
            if obj.item and obj.x == new_x and obj.y == new_y:
                insert_position = i
                break

        globalvars.GAME.current_objects.insert(insert_position, self.owner)

        self.owner.animation_init()

        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game.game_message("Dropped [{}]".format(self.owner.name_object))

    def use(self):
        """Uses the item to produce an effect and removes it from the inventory.

        Passes in the caster (the creature/actor using the item) and the value associated with the use_function.
        Removes the used item from the inventory that it was held in. Prints error message to console if an error
        occurred when executing the use_function.

        """

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:

            # self.owner would be the item itself.
            # However, self.container, which was initialized in the pick_up(actor) method, is related to the actor
            # holding the item.

            result = self.use_function(self.container.owner, self.value)
            if result != "unused":
                self.container.inventory.remove(self.owner)


class ComEquipment:
    """Equipment component gives actor objects item component properties as well as extra combat bonuses and statuses.

    Equipments are a component of actor objects, but also contain the item component (see ObjActor initialization).

    Attributes:
        attack_bonus (arg, int): Optional argument that specifies the attack bonus of the equipment. Default value is
                                 initialized to 0.
        defence_bonus (arg, int): Optional argument that specifies the defence bonus of the equipment. Default value is
                                  initialized to 0.
        slot (arg, str): Indicates the slot that the equipment should occupy
                        (currently only "Right Hand" and "Left Hand").

    """

    def __init__(self, attack_bonus=0, defence_bonus=0, slot=None):   # might need to delete None initialization of slot

        self.attack_bonus = attack_bonus
        self.defence_bonus = defence_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):
        """Toggles and sets equipment's status attribute "equipped".

        """

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        """Equips the item and sets the equipped attribute to True.

        Checks the slot of the equipment to see if that particular slot is already occupied. Display appropriate game
        messages to PLAYER. If the slot is empty, set equipped attribute to true.

        Returns:
            A game message indicating player of equipment status of the object or any problems when attempting to equip.

        """

        # check for equipment in the corresponding slot
        all_equipped_items = self.owner.item.container.equipped_items

        if all_equipped_items:  # do check only if there are equipped items on already, if not, equip as normal
            for equipped_item in all_equipped_items:
                if equipped_item.equipment.slot == self.slot:
                    game.game_message("There is already an item in the {} slot!".format(self.slot), constants.COLOR_WHITE)
                    return

        self.equipped = True
        game.game_message("Equipped [{}] in the {} slot".format(self.owner.name_object, self.slot))

    def unequip(self):
        """Unequips the item and sets the equipped attribute to False.

        Display a game messages to PLAYER indicating the equipment has been unequipped.

        Returns:
            A game message indicating the equipment has been unequipped.

        """
        self.equipped = False

        game.game_message("Unequipped [{}]".format(self.owner.name_object))