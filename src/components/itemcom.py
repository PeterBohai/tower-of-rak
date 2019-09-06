from src import constants, globalvars, game


class ComItem:
    """Item component class that gives actor objects item-like properties and functionality like pick up and use.

    Attributes
    ----------
    item_desc : str
        A description of the item.
    weight : int, optional
        The weight value in wu (weight units) of the item.
    item_type : str, optional
        Type of item (gold, consumable, magic, equipment, etc.)
    use_function : function, optional
        Function that's executed when item is used.
    value : int, optional
        Value of the item if it holds one (gold, exp etc.).
    container : ComContainer
        The specific container object the item resides in. Initialized to None.

    """
    def __init__(self, item_desc, weight=0,
                 item_type=None,
                 use_function=None,
                 value=0):

        self.item_desc = item_desc
        self.weight = weight
        self.item_type = item_type
        self.use_function = use_function
        self.value = value
        self.container = None
        self.hover_sound_played = False

    def pick_up(self, actor):
        """Picks up the item and either places it into the `actor`'s inventory, or directly used upon picking up.

        Parameters
        ----------
        actor : ObjActor
            The actor object (usually PLAYER) that will hold the item after pick up.

        Returns
        -------
        None

        """
        if self.item_type == "gold":
            globalvars.ASSETS.sfx_coin_pickup.play()
            actor.gold += self.value

            self.owner.animation_del()
            globalvars.GAME.current_objects.remove(self.owner)

            game.game_message(f"Gained {self.value} gold.", constants.COLOR_YELLOW)
            game.game_message(f"Player now has {actor.gold} gold total.", constants.COLOR_WHITE)
            return

        elif self.item_type == "Red Soul":
            globalvars.ASSETS.sfx_soul_consume.play()
            actor.exp_total += self.value

            self.owner.animation_del()
            globalvars.GAME.current_objects.remove(self.owner)
            return

        if actor.container:
            if self.item_type == "Pure Soul":
                globalvars.ASSETS.sfx_pure_soul_consume.play()
                actor.container.inventory.append(self.owner)
                self.container = actor.container
                self.use()
                globalvars.GAME.current_objects.remove(self.owner)
                return

            if actor.container.weight + self.weight > actor.container.max_weight:
                game.game_message("Not enough room to pick up", constants.COLOR_WHITE)

            else:
                game.game_message(f"Picked up [{self.owner.display_name}]")
                actor.container.inventory.append(self.owner)

                self.owner.animation_del()
                globalvars.GAME.current_objects.remove(self.owner)

                self.container = actor.container

    def drop(self, new_x, new_y):
        """Drops this item object onto the ground specified by the (`new_x`,`new_y`) map-grid coordinates.

        Parameters
        ----------
        new_x : int
            The map-grid x-coord to drop the item (usually PLAYER's current position).
        new_y : int
            The map-grid y-coord to drop the item (usually PLAYER's current position).

        Returns
        -------
        None

        """

        # inserting underneath any creature or PLAYER but above any objects already on that tile
        insert_position = 0
        for i, obj in enumerate(reversed(globalvars.GAME.current_objects)):
            if obj.item and obj.x == new_x and obj.y == new_y:
                insert_position = i
                break

        globalvars.GAME.current_objects.insert(insert_position, self.owner)

        self.owner.animation_init()

        if self.owner in self.container.inventory:
            self.container.inventory.remove(self.owner)
        elif self.owner in self.container.equipped_inventory:
            self.container.equipped_inventory.remove(self.owner)

        self.owner.x, self.owner.y = new_x, new_y
        game.game_message(f"Dropped [{self.owner.display_name}]")

    def use(self):
        """Uses the item to produce an effect and removes it from the inventory.

        Passes in the caster (the creature/actor using the item) and any value associated to the use_function.

        Returns
        -------
        None

        """
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:
            used = self.use_function(self.container.owner, self.value)
            if used:
                self.container.inventory.remove(self.owner)
            elif self.item_type == "Pure Soul":
                self.container.inventory.remove(self.owner)


class ComEquipment:
    """Equipment component class that gives item objects extra combat bonuses and statuses.

    Attributes
    ----------
    attack_bonus : int
        Value of additional damage a wielder will gain when equipped.
    defence_bonus : int
        Value of additional defence a wielder will gain when equipped.
    slot : str
        The slot that the equipment will occupy (Right, Left, Body, Legs, Feet, Head).
    equipped : bool
        True if the item is equipped.

    """
    def __init__(self, attack_bonus=0, defence_bonus=0, slot=None):

        self.attack_bonus = attack_bonus
        self.defence_bonus = defence_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):
        """Toggles the equipment on and off.

        Returns
        -------
        None

        """
        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        """Equips the item and sets the equipped attribute to True.

        Checks the slot of the equipment to see if that particular slot is already occupied.
        If the slot is empty, set equipped attribute to true.

        Returns
        -------
        None

        """
        all_equipped_items = self.owner.item.container.equipped_inventory

        if len(all_equipped_items) > 0:
            for equipped_item in all_equipped_items:
                if equipped_item.equipment.slot == self.slot:
                    game.game_message(f"There is already an item in the {self.slot} slot!", constants.COLOR_WHITE)
                    self.equipped = False
                    return

        self.equipped = True
        game.game_message(f"Equipped [{self.owner.object_name}] in the {self.slot} slot")

    def unequip(self):
        """Unequips the item and sets the equipped attribute to False.

        Returns
        -------
        None

        """
        self.equipped = False
        game.game_message(f"Unequipped [{self.owner.display_name}]")
