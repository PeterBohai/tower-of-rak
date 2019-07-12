# Standard library imports
import random

# Third party imports
import pygame


# Local project imports
from source import constants, globalvars, game, map


class ComCreature:
    """Creature component gives actor objects health and fighting properties.

    Creatures have health, can damage other objects by attacking them and possibly die.

    Attributes:
        name_instance (arg, str): Name of the individual creature. Randomly generated using namegen methods in tcod
                                  library. See gen_enemy() function under Generation for details.
        max_hp (arg, int): Max hit points of the creature. Default value initialized as 10.
        base_atk (arg, int): Base attack power of the creature. Default value initialized as 2.
        base_def (arg, int): Base defence of the creature. Default value initialized as 0.
        death_function (arg, function): Function to be executed when current_hp is 0 or below.
        current_hp (int): Current health of the creature.

    """

    def __init__(self, name_instance,
                 max_hp=10,
                 base_atk=2,
                 base_def=0,
                 death_function=None):

        self.name_instance = name_instance
        self.maxHp = max_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.current_hp = max_hp
        self.death_function = death_function

    def move(self, dx, dy):
        """Moves the creature object on the map.

        Args:
            dx (int): Distance in tile map coordinates to move object along the x-axis.
            dy (int): Distance in tile map coordinates to move object along the y-axis.

        """

        # boolean to check if a tile is a wall
        tile_is_wall = (globalvars.GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path is True)

        target = map.map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            # player or a confused creature (not normal ai)can hurt anyone
            if self.owner is globalvars.PLAYER or self.owner.ai.hurt_kin is True:
                self.attack(target)

            # creatures can only harm the player and not their kin
            elif self.owner is not globalvars.PLAYER and target is globalvars.PLAYER:
                self.attack(globalvars.PLAYER)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):
        """Attacks another "target" ObjActor object.

        Uses the take_damage() method in this ComCreature class to implement harming of target. Will display a game
        message indicating how much damage the creature did to the target. The damage dealt to the target is influenced
        by the power and defence properties.

        Args:
            target (ObjActor): Target actor object (that also contains a creature component)to be attacked and harmed.

        Returns:

        """

        damage_dealt = self.power - target.creature.defence
        if damage_dealt <= 0:
            damage_dealt = 0

        # naming convention for attack message
        # (PLAYER will only display nickname, creatures display nickname and creature type)
        if target is globalvars.PLAYER:
            victim_name = target.creature.name_instance
        else:
            victim_name = target.display_name

        if self.owner is globalvars.PLAYER:
            attacker_name = self.name_instance
        else:
            attacker_name = self.owner.display_name

        if damage_dealt > 0 and self.owner is globalvars.PLAYER:
            pygame.mixer.Sound.play(random.choice(globalvars.ASSETS.sfx_hit_punch_list))

        # attack message
        attack_msg = "{} attacks {} for {} damage!".format(attacker_name, victim_name, damage_dealt)
        game.game_message(attack_msg, constants.COLOR_WHITE)

        # target creature takes damage
        target.creature.take_damage(damage_dealt)

    def take_damage(self, damage):
        """Applies damage amount to current_hp.

        Decreases current_hp of self and displays a game message indicating how much health remains. The name displayed
        is different for PLAYER and other creatures. Runs death_function specified in the initialization of the creature
        object when health falls to 0 or below.

        Args:
            damage (int): Amount of damage to be taken away from current_hp of self.

        """

        self.current_hp -= damage

        if self.owner is not globalvars.PLAYER:
            msg_color = constants.COLOR_ORANGE

            if self.current_hp < 0:
                damage_taken = "{}'s health is 0/{}".format(self.owner.display_name, self.maxHp)
            else:
                damage_taken = "{}'s health is {}/{}".format(self.owner.display_name, self.current_hp, self.maxHp)

        elif self.owner is globalvars.PLAYER:
            msg_color = constants.COLOR_RED

            if self.current_hp < 0:
                damage_taken = "{}'s health is 0/{}".format(self.name_instance, self.maxHp)
            else:
                damage_taken = "{}'s health is {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

        game.game_message(damage_taken, msg_color)

        if self.current_hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def get_health_percentage(self):
        return self.current_hp / self.maxHp

    def heal(self, amount):
        """Applies health to creature's current_hp.

        Increases current_hp of self and displays a game message indicating the amount healed and another game message
        indicating the current health of the creature. Makes sure that the current_hp of creature does not go past its
        maximum health.

        Args:
            amount (int): Amount of health to be regained.

        """

        hp_before_heal = self.current_hp
        self.current_hp += amount

        if self.current_hp <= self.maxHp:
            healed_amt_msg = "{} healed for {}".format(self.name_instance, amount)
            curr_hp_msg = "{}'s health is now {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

            game.game_message(healed_amt_msg, constants.COLOR_GREEN)
            game.game_message(curr_hp_msg, constants.COLOR_WHITE)

        # when healing gave creature more hp than max hp
        elif self.current_hp > self.maxHp:
            actual_healed_amt = self.maxHp - hp_before_heal
            self.current_hp = self.maxHp

            healed_amt_msg = "{} healed for {}".format(self.name_instance, actual_healed_amt)
            curr_hp_msg = "{}'s health is now {}/{}".format(self.name_instance, self.current_hp, self.maxHp)

            game.game_message(healed_amt_msg, constants.COLOR_GREEN)
            game.game_message(curr_hp_msg, constants.COLOR_WHITE)

    @property
    def power(self):
        """A property that calculates and returns the current total power of the creature.

        Adds base_atk and all attack bonuses currently available to the creature (equipped items, etc.) to its
        total power.

        Returns:
            total_power (int): The current total power of the creature (including base and bonuses)

        """
        total_power = self.base_atk

        if self.owner.container:
            equipment_power_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_items]

            for power_bonus in equipment_power_bonuses:
                total_power += power_bonus

        return total_power

    @property
    def defence(self):
        """A property that calculates and returns the current total defence of the creature.

        Adds base_def and all defence bonuses currently available to the creature (equipped items, etc.) to its
        total defence.

        Returns:
            total_defence (int): The current total defence of the creature (including base and bonuses)

        """
        total_defence = self.base_def

        if self.owner.container:
            equipment_defence_bonuses = [obj.equipment.defence_bonus for obj in self.owner.container.equipped_items]

            for def_bonus in equipment_defence_bonuses:
                total_defence += def_bonus

        return total_defence
