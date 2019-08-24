import pygame

from source import constants, globalvars


class ObjCamera:
    """Camera object that updates the view of the map as the player moves around.

    Attributes
    ----------
    width : int
        The width of the rectangular camera display in pixels (typically same as the game window dimensions).
    height : int
        The height of the rectangular camera display in pixels (typically same as the game window dimensions).
    x : int
        The x-coordinate in pixels of where the camera will be aligned to relative to the map.
    y : int
        The y-coordinate in pixels of where the camera will be aligned to relative to the map.

    """

    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.x, self.y = (0, 0)

    @property
    def rectangle(self):
        """pygame.Rect obj: The rectangle area of the camera object aligned at its center coordinates."""
        pos_rect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        pos_rect.center = (self.x, self.y)

        return pos_rect

    @property
    def map_address(self):
        """tuple: The map-grid coordinates (not pixels) of where the camera object's center is currently at."""

        map_x = int(self.x / constants.CELL_WIDTH)
        map_y = int(self.y / constants.CELL_HEIGHT)

        return map_x, map_y

    def update_pos(self):
        """Updates the x, y coordinates of camera as the PLAYER moves.

        Returns
        -------
        None

        """
        camera_speed = 1

        # add half the dimensions of one cell as PLAYER coordinates are aligned to the cell's upper-left corner
        target_x = (globalvars.PLAYER.x * constants.CELL_WIDTH) + (constants.CELL_WIDTH/2)
        target_y = (globalvars.PLAYER.y * constants.CELL_HEIGHT) + (constants.CELL_HEIGHT/2)
        distance_to_target_x, distance_to_target_y = self.map_dist_to_cam((target_x, target_y))

        self.x += int(distance_to_target_x * camera_speed)
        self.y += int(distance_to_target_y * camera_speed)

    def map_dist_to_cam(self, map_pixel_coord):
        """Calculates the distance between the camera and the specified `coords`

        Parameters
        ----------
        map_pixel_coord : tuple
            The (x, y) pixel coordinates relative to the map for the camera object to compare to.

        Returns
        -------
        tuple
            The (x, y) pixel coordinate difference between the camera and `coords` relative to the map.

        """
        map_x, map_y = map_pixel_coord

        distance_diff_x = map_x - self.x
        distance_diff_y = map_y - self.y

        return distance_diff_x, distance_diff_y

    def window_dist_to_cam(self, window_coord):
        """Calculates the distance the camera's center (in terms of the window) from the specified window `coords`.

        Parameters
        ----------
        window_coord : tuple
            The (x, y) pixel coordinates relative to the window for the camera object to compare to.

        Returns
        -------
        tuple
            The (x, y) pixel coordinate difference between the camera and `coords` relative to the window.

        """
        window_x, window_y = window_coord

        distance_diff_x = window_x - (self.width / 2)
        distance_diff_y = window_y - (self.height / 2)

        return distance_diff_x, distance_diff_y

    def window_to_map(self, window_coord):
        """Calculates the map-grid coordinates of the given window-pixel `coords`.

        Parameters
        ----------
        window_coord : tuple
            The (x, y) pixel window coordinate to be converted into map-grid coordinates.

        Returns
        -------
        tuple
            The map-grid coordinate equivalent of the given `window_coords`

        """
        target_x, target_y = window_coord

        # convert window coordinates to distance from camera
        cam_wind_dx, cam_wind_dy = self.window_dist_to_cam((target_x, target_y))

        # distance from camera to map coordinate
        map_pix_x = self.x + cam_wind_dx
        map_pix_y = self.y + cam_wind_dy

        map_grid_x = int(map_pix_x / constants.CELL_WIDTH)
        map_grid_y = int(map_pix_y / constants.CELL_HEIGHT)

        return map_grid_x, map_grid_y
