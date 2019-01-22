# Third party imports
import pygame

# Local project imports
from source import constants
from source import globalvars


class ObjCamera:
    """Camera object that updates the view of the map as the player moves around.

    Attributes:
        width (int): The width of the rectangular camera display in pixels
        height (int): The height of the rectangular camera display in pixels
        x (int): The x (pixel) coordinate of the camera rectangle to be aligned to a surface.
        y (int): The y (pixel) coordinate of the camera rectangle to be aligned to a surface.

    """

    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.x, self.y = (0, 0)

    @property
    def rectangle(self):
        """Creates the rectangle area of the camera object and aligns its center coordinates accordingly.

        Returns:
            pos_rect (Rect): A pygame's rectangle object aligned at the center.

        """
        pos_rect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

        pos_rect.center = (self.x, self.y)

        return pos_rect

    @property
    def map_address(self):
        """Converts the camera's center map-pixel coordinates to map-tile coordinates.

        Returns:
            tup_map_tile_coords (tuple): The converted map-tile coordinates of the camera's center position on the map.

        """

        map_x = int(self.x / constants.CELL_WIDTH)
        map_y = int(self.y / constants.CELL_HEIGHT)

        tup_map_tile_coords = (map_x, map_y)

        return tup_map_tile_coords

    def update_pos(self):
        """Updates and sets the position of the x, y coordinates of camera.

        Follows the coordinate (relative to SURFACE_MAP) of the center of the player. Have the option of making the
        camera lag behind a bit, or have to catch up in a smooth motion.

        """

        # add half the pixel dimensions of one cell as PLAYER coordinates are aligned to the cell's upper-left corner
        target_x = (globalvars.PLAYER.x * constants.CELL_WIDTH) + (constants.CELL_WIDTH/2)
        target_y = (globalvars.PLAYER.y * constants.CELL_HEIGHT) + (constants.CELL_HEIGHT/2)

        distance_to_target_x, distance_to_target_y = self. map_dist_to_cam((target_x, target_y))

        camera_speed = 1

        self.x += int(distance_to_target_x * camera_speed)
        self.y += int(distance_to_target_y * camera_speed)

    def map_dist_to_cam(self, tup_coords):
        """Gives x and y distance from specified map-coordinate to camera's center map-coordinate.

        Calculates the x and y coordinate difference between a specified coordinate on the map and the center
        map-coordinate of the camera. Every value is expressed in pixels.

        Args:
            tup_coords (tuple): Pixel coordinates relative to the map, or SURFACE_MAP.

        Returns:
            tup_diff_coord (tuple): Pixel coordinates relative to the map of the calculated x and y difference.

        """

        map_x, map_y = tup_coords

        distance_diff_x = map_x - self.x
        distance_diff_y = map_y - self.y

        tup_diff_coord = (distance_diff_x, distance_diff_y)

        return tup_diff_coord

    def window_dist_to_cam(self, tup_coords):
        """Gives x and y distance from specified window-coordinate to camera's center window-coordinate.

        Calculates the x and y coordinate difference between a specified coordinate on the window and the center
        window-coordinate of the camera. Every value is expressed in pixels.

        Args:
            tup_coords (tuple): Pixel coordinates relative to the window, or SURFACE_MAIN.

        Returns:
            tup_diff_coord (tuple): Pixel coordinates relative to the window of the calculated x and y difference.

        """

        window_x, window_y = tup_coords

        distance_diff_x = window_x - (self.width / 2)
        distance_diff_y = window_y - (self.height / 2)

        tup_diff_coord = (distance_diff_x, distance_diff_y)

        return tup_diff_coord

    def window_to_map(self, tup_coords):
        target_x, target_y = tup_coords

        # convert window coordinates to distance from camera
        cam_wind_dx, cam_wind_dy = self.window_dist_to_cam((target_x, target_y))

        # distance from camera to map coordinate
        map_pix_x = self.x + cam_wind_dx
        map_pix_y = self.y + cam_wind_dy

        # pixel map coordinates converted from window pixel coordinates
        tup_map_coords = (map_pix_x, map_pix_y)

        return tup_map_coords