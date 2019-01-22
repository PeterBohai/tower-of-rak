# Standard library imports
import os
import datetime

# Third party imports
import pygame

# Local project imports
from source import constants, globalvars, gui, text


class ComStairs:
    """Stairs component that is defaulted to lead the player up to the next floor.

    Attributes:
        upwards (arg, bool): Specifies whether it should take the player up/to the next map. Default set to True.
                             False would mean stairs lead down and to the previous map.

    """

    def __init__(self, upwards=True):
        self.upwards = upwards

    def use(self):
        """Implements map transitioning when called.

        When only upwards attribute is set to True, the player progresses to the next map. Otherwise, the player goes
        to the previous map.

        TODO:  Possibly implement "locking" the player in until a task is done (rendering stairs unusable).

        Returns:
            None

        """

        if self.upwards:
            globalvars.GAME.map_transition_next()

        else:
            globalvars.GAME.map_transition_prev()


class ComPortal:
    def __init__(self):
        self.open_animation = "A_PORTAL_OPEN"
        self.closed_animation = "S_PORTAL_CLOSED"

    def update(self):
        # flag intialization
        found_lamp = False

        portal_is_open = (self.owner.status == "STATUS_OPEN")

        for obj in globalvars.PLAYER.container.inventory:
            if obj.name_object == "MAGIC ROCK":
                found_lamp = True

        # open the portal if player has lamp in their inventory
        if found_lamp and not portal_is_open:
            self.owner.status = "STATUS_OPEN"
            self.owner.animation_key = self.open_animation
            self.owner.animation_init()

        # close the portal if player does not have the lamp (or somehow decided to drop it)
        if not found_lamp and portal_is_open:
            self.owner.status = "STATUS_CLOSED"
            self.owner.animation_key = self.closed_animation
            self.owner.animation_init()

    def use(self):

        if self.owner.status == "STATUS_OPEN":
            globalvars.PLAYER.status = "STATUS_WIN"

            center_coords = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

            # button variables
            button_width = 80
            button_height = 30
            quit_button_x = constants.CAMERA_WIDTH / 2
            quit_button_y = constants.CAMERA_HEIGHT * 3 / 4

            quit_button = gui.GuiButton(globalvars.SURFACE_MAIN, "Quit",
                                        (quit_button_x, quit_button_y),
                                        (button_width, button_height),
                                        color_button_hovered=constants.COLOR_GREY,
                                        color_button_default=constants.COLOR_DARK_GREY,
                                        color_text_hovered=constants.COLOR_WHITE,
                                        color_text_default=constants.COLOR_WHITE)

            # make a legacy file
            file_name = "win_{}_{}.txt".format(globalvars.PLAYER.creature.name_instance,
                                               datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))

            with open("data/saves/{}".format(file_name), 'a+') as win_file:
                file_title = "************* {}'s WIN RECORD ************* \n\n"
                win_file.write(file_title.format(globalvars.PLAYER.creature.name_instance))
                for (message, color) in globalvars.GAME.message_history:
                    win_file.write(message + '\n')

                win_file.write("Deleted any game save files\n")

            # delete save game file
            save_to_rm = "data/saves/savegame"
            try:
                os.remove(save_to_rm)
            except OSError as e:
                print("Error: {} - {}".format(e.filename, e.strerror))

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
