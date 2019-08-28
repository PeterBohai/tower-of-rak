import os
import datetime

import pygame

from src import constants, globalvars, gui, text


class ComStairs:
    """Stairs component class that gives the actor object properties and functionality of stairs.

    Leads PLAYER up a floor (default) or down a floor.

    Attributes
    ----------
    upwards : bool
        True if the user (PLAYER) will go up a floor, False if down a floor.

    """

    def __init__(self, upwards=True):
        self.upwards = upwards

    def use(self):
        """Transitions the PLAYER up or down a floor.

        Returns
        -------
        None

        """
        # TODO:  Possibly implement "locking" the player in until a task is done (rendering stairs unusable).
        if self.upwards:
            globalvars.GAME.map_transition_next()
        else:
            globalvars.GAME.map_transition_prev()


class ComPortal:
    """Portal component class that gives the actor object properties and functionality of a portal.

    Attributes
    ----------
    open_animation : str
        String that corresponds to an animation dictionary key in ASSETS indicating the portal is open.
    closed_animation : str
        String that corresponds to an animation dictionary key in ASSETS indicating the portal is closed.

    """
    def __init__(self):
        self.open_animation = "A_PORTAL_OPEN"
        self.closed_animation = "S_PORTAL_CLOSED"

    def update(self):
        """Updates the status of the portal object as well as its animation depending on if the PLAYER has the relic.

        Returns
        -------
        None

        """
        found_relic = False

        for obj in globalvars.PLAYER.container.inventory:
            if obj.object_name == "MAGIC ROCK":
                found_relic = True

        # open the portal if player has relic in their inventory
        if found_relic and self.owner.status != "STATUS_OPEN":
            self.owner.status = "STATUS_OPEN"
            self.owner.animation_key = self.open_animation
            self.owner.animation_init()

        # close the portal if player does not have the relic (or somehow decided to drop it)
        if not found_relic and self.owner.status == "STATUS_OPEN":
            self.owner.status = "STATUS_CLOSED"
            self.owner.animation_key = self.closed_animation
            self.owner.animation_init()

    def use(self):
        """Enters the portal if its open and upon entering, wins the game!

        Returns
        -------
        None

        """

        if self.owner.status == "STATUS_OPEN":
            globalvars.PLAYER.status = "STATUS_WIN"
            center_coords = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

            # button variables
            button_width = 96
            button_height = 32
            quit_button_x = constants.CAMERA_WIDTH / 2
            quit_button_y = constants.CAMERA_HEIGHT * 3 / 4

            quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Quit",
                                        (quit_button_x, quit_button_y),
                                        (button_width, button_height))

            # make a legacy file
            winner_name = globalvars.PLAYER.creature.personal_name
            win_time = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
            file_name = f"win_{winner_name}_{win_time}.txt"

            with open(f"data/saves/{file_name}", 'a+') as win_file:
                file_title = f"************* {winner_name}'s WIN RECORD ************* \n\n"

                win_file.write(file_title)
                for (message, color) in globalvars.GAME.message_history:
                    win_file.write(message + '\n')

                win_file.write("Deleted any game save files\n")

            # delete save game file if there is one
            save_to_rm = "data/saves/savegame"
            try:
                os.remove(save_to_rm)
            except OSError:
                print("No prior save file to delete")

            # deinitialize pygame Surface objects (animation sprites)
            for obj in globalvars.GAME.current_objects:
                obj.animation_del()

            # For exiting out of the game
            win_popup = True
            while win_popup:

                # get player input
                events_list = pygame.event.get()
                mouse_pos = pygame.mouse.get_pos()
                player_events = (events_list, mouse_pos)

                for event in events_list:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            win_popup = False

                if quit_button.update(player_events):
                    win_popup = False

                globalvars.SURFACE_MAIN.fill(constants.COLOR_WHITE)
                text.draw_text(globalvars.SURFACE_MAIN, "You WON!", constants.FONT_PLAYER_DEATH,
                               center_coords,
                               constants.COLOR_BLUE,
                               center=True)

                quit_button.draw()

                pygame.display.update()
