import random
import math

import pygame
import tcod

from src import constants, globalvars, game, map, text


class ComCreature:
    """Creature component class which give actor objects creature-like properties and functionality.

    These creatures contain health and the ability to move and attack, etc.

    Attributes
    ----------
    personal_name : str
        The ai component object that the actor originally had before being set to this one.
    max_hp : int
        Max health points of the creature. Default is 10.
    base_atk : int
        Base attack points of the creature. Default is 2.
    base_def : int
        Base defence points of the creature. Default is 0.
    current_hp : int
        Current health points of the creature.
    death_function : function
        Function that the creature executes when its `current_hp` reaches 0 or less.
    dmg_received : int
        The amount of damaged received if this creature was attacked.
    was_hit : bool
        True if the creature was hit in the previous turn, regardless of the damage taken (even 0).
    dmg_alpha : int
        Alpha value [0, 255] of the fading damage number display on top of the creature when hit.
    health_bar_alpha : int
        Alpha value [0, 255] of the small health bar display on top of the creature when being hit.
    internal_timer : int
        The number of ticks (total since pygame init) at the moment this creature was hit.

    """

    def __init__(self, personal_name,
                 max_hp=10,
                 base_atk=2,
                 base_def=0,
                 death_function=None):

        self.personal_name = personal_name
        self.max_hp = max_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.current_hp = max_hp
        self.death_function = death_function
        self.dmg_received = None
        self.was_hit = False
        self.dmg_alpha = 0
        self.health_bar_alpha = 0
        self.internal_timer = 0

    @property
    def power(self):
        """int: Calculates and returns the current total power of the creature.

        Takes into account the creature's attack points (base attack + bonuses) and any equipment/item/spell
        bonuses.

        """
        additional_random = 0

        if 1 <= self.base_atk <= 12:
            additional_random = tcod.random_get_int(0, 0, 1)
        elif 13 <= self.base_atk <= 24:
            additional_random = tcod.random_get_int(0, 0, 2)
        elif 25 <= self.base_atk <= 40:
            additional_random = tcod.random_get_int(0, 0, 3)
        elif self.base_atk > 40:
            additional_random = tcod.random_get_int(0, 0, 5)

        total_power = self.attack_points + additional_random

        return total_power

    @property
    def defence(self):
        """int: Calculates and returns the current total defence of the creature.

        Takes into account the base defence of the creature as well as any equipment/item/spell bonuses.

        """
        total_defence = self.base_def

        if self.owner.container:
            equipment_def_bonuses = [obj.equipment.defence_bonus for obj in self.owner.container.equipped_inventory]

            for def_bonus in equipment_def_bonuses:
                total_defence += def_bonus

        return total_defence

    @property
    def hp_percent(self):
        """float: Returns the percentage of total health the creature still currently has."""
        return self.current_hp / self.max_hp

    @property
    def attack_points(self):
        """int: Calculates and returns the raw attack points of the PLAYER (base stat plus weapon bonuses)"""
        raw_damage = self.base_atk
        if self.owner.container:
            equipment_power_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_inventory]

            for power_bonus in equipment_power_bonuses:
                raw_damage += power_bonus

        return raw_damage

    def level_up(self):
        self.owner.level += 1
        self.base_def += 1
        self.base_atk += 1
        game.game_message(
            f"Player is now level {self.owner.level}, def is now {self.base_def}, and atk is {self.base_atk}",
            constants.COLOR_YELLOW)
        if self.owner.level == constants.PLAYER_MAX_LV:
            game.game_message("Player is now at max level! NICE!", constants.COLOR_RED)

    def move(self, dx, dy):
        """Moves the creature object one tile on the map, stopping at walls and attacking when appropriate.

        Parameters
        ----------
        dx : int
            The distance/direction to move the object along the x-axis relative to the map grid. Usually [-1, 1].
        dy : int
            The distance/direction to move the object along the y-axis relative to the map grid. Usually [-1, 1].

        Returns
        -------
        None

        """
        self.was_hit = False
        tile_is_wall = globalvars.GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path

        creature_there = map.creature_at_coords(self.owner.x + dx, self.owner.y + dy, exclude=self.owner)

        if creature_there is not None:
            if self.owner is globalvars.PLAYER or self.owner.ai.hurt_kin is True:
                self.attack(creature_there)

            # creatures can only harm the PLAYER
            elif self.owner is not globalvars.PLAYER and creature_there is globalvars.PLAYER:
                self.attack(globalvars.PLAYER)

        # move the creature in the specified direction if not a wall there
        if not tile_is_wall and creature_there is None:
            self.owner.x += dx
            self.owner.y += dy

            for objActor in globalvars.GAME.current_objects:
                if objActor.is_visible and objActor.creature:
                    objActor.creature.was_hit = False

    def move_towards(self, target):
        """Moves this creature one tile closer towards `target`.

        Parameters
        ----------
        target : ObjActor
            The target object to move towards.

        Returns
        -------
        None

        """
        dx = target.x - self.owner.x
        dy = target.y - self.owner.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        # check for wall in the direction it was supposed to move
        if map.wall_at_coords(globalvars.GAME.current_map, self.owner.x + dx, self.owner.y + dy):

            # move towards target in the x-direction if blocked in the y-direction
            if dx == 0:
                if target.x > self.owner.x:
                    dx = 1
                else:
                    dx = -1
                dy = 0

            #  move towards target in the y-direction if blocked in the x-direction
            elif dy == 0:
                if target.y > self.owner.y:
                    dy = 1
                else:
                    dy = -1
                dx = 0

        self.move(dx, dy)

    def move_away(self, target):
        """Moves this creature away from `target`.

        Parameters
        ----------
        target : ObjActor
            The target object to move away from.

        Returns
        -------
        None

        """
        dx = self.owner.x - target.x
        dy = self.owner.y - target.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        rand_int = tcod.random_get_int(0, 0, 100)
        percent_chance = 6

        # have a small chance of not always moving strictly away in the opposite direction of Player
        if rand_int < percent_chance:

            # move towards direction that is not blocked by walls 2 tiles or closer away
            if dx == 0:
                if map.wall_at_coords(globalvars.GAME.current_map, self.owner.x + 1, self.owner.y) or \
                      map.wall_at_coords(globalvars.GAME.current_map, self.owner.x + 2, self.owner.y):
                    dx = -1
                elif map.wall_at_coords(globalvars.GAME.current_map, self.owner.x - 1, self.owner.y) or \
                        map.wall_at_coords(globalvars.GAME.current_map, self.owner.x - 2, self.owner.y):
                    dx = 1
                else:
                    dx = random.choice((-1, 1))

                dy = 0
            elif dy == 0:
                if map.wall_at_coords(globalvars.GAME.current_map, self.owner.x, self.owner.y + 1) or \
                      map.wall_at_coords(globalvars.GAME.current_map, self.owner.x, self.owner.y + 2):
                    dy = -1
                elif map.wall_at_coords(globalvars.GAME.current_map, self.owner.x, self.owner.y - 1) or \
                        map.wall_at_coords(globalvars.GAME.current_map, self.owner.x, self.owner.y - 2):
                    dy = 1
                else:
                    dy = random.choice((-1, 1))

                dx = 0

        # check for wall in the direction it was supposed to move
        if map.wall_at_coords(globalvars.GAME.current_map, self.owner.x + dx, self.owner.y + dy):

            # move randomly to either left or right if blocked in the y-direction
            if dx == 0:
                dx = random.choice((-1, 1))
                dy = 0
            # move randomly to either up or down if blocked in the x-direction
            elif dy == 0:
                dy = random.choice((-1, 1))
                dx = 0

        # has a small chance to stay still for a turn
        rand_stay_chance = tcod.random_get_int(0, 1, 100)
        if rand_stay_chance < 6:
            dx, dy = (0, 0)

        self.move(dx, dy)

    def attack(self, target):
        """Attacks the `target` object.

        Amount of damage dealt depends on this creature's power property value as well as the defence property of the
        `target` creature.

        Parameters
        ----------
        target : ObjActor
            The target object to attack and take health points away from.

        Returns
        -------
        None

        """
        dmg_dealt = max(self.power - target.creature.defence, 0)

        victim_name = target.display_name
        attacker_name = self.owner.display_name

        if self.owner is globalvars.PLAYER:
            pygame.mixer.Sound.play(random.choice(globalvars.ASSETS.sfx_hit_punch_list))

        game.game_message(f"{attacker_name} attacks {victim_name} for {dmg_dealt} damage!", constants.COLOR_WHITE)

        target.creature.take_damage(dmg_dealt)

    def take_damage(self, damage):
        """Applies `damage` value to this creature's current health and executes its death function if health <= 0.

        Parameters
        ----------
        damage : int
            Amount of damage to be taken away from current_hp.

        Returns
        -------
        None

        """
        self.was_hit = True
        self.dmg_received = damage
        self.current_hp = max(self.current_hp - damage, 0)

        if self.owner is globalvars.PLAYER:
            msg_color = constants.COLOR_RED
        else:
            msg_color = constants.COLOR_ORANGE

        damage_taken = f"{self.owner.display_name}'s health is {self.current_hp}/{self.max_hp}"
        game.game_message(damage_taken, msg_color)

        if self.current_hp <= 0 and self.death_function is not None:
            self.death_function(self.owner)

    def heal(self, amount):
        """Adds  `amount` of health to creature's current health value.

        Parameters
        ----------
        amount : int
            Amount of health points to add to this creature's current_hp.

        Returns
        -------
        None

        """
        hp_before_heal = self.current_hp
        self.current_hp += amount

        if self.current_hp > self.max_hp:
            actual_healed_amt = self.max_hp - hp_before_heal
            self.current_hp = self.max_hp
        else:
            actual_healed_amt = amount

        healed_amt_msg = f"{self.owner.display_name} healed for {actual_healed_amt}"
        curr_hp_msg = f"{self.owner.display_name}'s health is now {self.current_hp}/{self.max_hp}"

        game.game_message(healed_amt_msg, constants.COLOR_GREEN)
        game.game_message(curr_hp_msg, constants.COLOR_WHITE)

    def draw_health(self):
        """Draws a small health bar indicator on top or below creature when taking damage.

        Indicator will fade away after a few seconds of the creature not being damaged.

        Returns
        -------
        None

        """
        bar_width = 38
        bar_height = 8
        surface = globalvars.SURFACE_MAP

        if self.hp_percent > 0.6:
            color = constants.COLOR_GRASS_GREEN
        elif self.hp_percent > 0.3:
            color = constants.COLOR_HP_YELLOW
        else:
            color = constants.COLOR_RED

        healthy_width = self.hp_percent * bar_width

        current_time = pygame.time.get_ticks()

        # draw health bar only if taken damage
        if self.current_hp < self.max_hp or self.dmg_received is not None:

            # start fading after 3 secs
            if current_time - self.internal_timer >= 3000:
                self.health_bar_alpha = max(self.health_bar_alpha - 3, 0)

            pos_x = self.owner.x * constants.CELL_WIDTH - 4
            pos_y = self.owner.y * constants.CELL_HEIGHT - (bar_height + 3)

            # draw health bar underneath creature if player is attacking from the top side
            if globalvars.PLAYER.x == self.owner.x and globalvars.PLAYER.y == self.owner.y - 1:
                pos_y = self.owner.y * constants.CELL_HEIGHT + (constants.CELL_HEIGHT + 3)

            healthy_surface = pygame.Surface((healthy_width, bar_height))
            healthy_surface.fill(color)

            back_surface = pygame.Surface((bar_width, bar_height))
            back_surface.fill((0, 0, 0, 100))

            alpha_surface = pygame.Surface(back_surface.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, self.health_bar_alpha))

            outline_rect = pygame.Rect(0, 0, bar_width, bar_height)

            back_surface.blit(healthy_surface, (0, 0))
            pygame.draw.rect(back_surface, constants.COLOR_BLACK, outline_rect, 1)
            back_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            surface.blit(back_surface, (pos_x, pos_y))

    def draw_damage_taken(self):
        """Draws a number indicator of the damage taken by this creature.

        Returns
        -------
        None

        """
        is_below = (globalvars.PLAYER.x == self.owner.x and globalvars.PLAYER.y == self.owner.y - 1)

        start_x = self.owner.x * constants.CELL_WIDTH + int(constants.CELL_WIDTH / 2)
        if is_below:
            start_y = self.owner.y * constants.CELL_HEIGHT + (constants.CELL_HEIGHT + int(constants.CELL_WIDTH / 2))
        else:
            start_y = self.owner.y * constants.CELL_HEIGHT

        display_coords = (self.owner.dmg_taken_posx, self.owner.dmg_taken_posy)

        if self.dmg_alpha > 250:
            self.owner.dmg_taken_posx = start_x
            self.owner.dmg_taken_posy = start_y
        else:
            if (start_y - self.owner.dmg_taken_posy) < 32:
                self.owner.dmg_taken_posy -= 1

        if self.current_hp < self.max_hp or self.dmg_received is not None:
            font = constants.FONT_VIGA
            text_color = pygame.Color('red3')
            dmg_text = str(self.dmg_received)

            if self.owner is globalvars.PLAYER:
                text_color = pygame.Color('red3')

            if self.dmg_received == 0:
                text_color = pygame.Color('royalblue3')

            self.dmg_alpha = text.draw_fading_text(globalvars.SURFACE_MAP, dmg_text, font, display_coords,
                                                   text_color, self.dmg_alpha, center=True)

