
class ComContainer:
    """Container component gives actor objects an inventory that can hold item objects.

    Attributes:
        inventory (arg, list): Optional argument that initializes a list of ObjActor with the item component. Default
                               list is empty.
        max_volume (arg, float): Optional argument that specifies the maximum volume of the container. Default value is
                                 initialized to 10.0.

    """

    def __init__(self, volume=10.0, inventory=[]):
        self.inventory = inventory
        self.max_volume = volume    # further usage of this in the future for more strategic and robust inventory system


    # Get volume within container
    @property
    def volume(self):
        """Gets the current total volume of the container.

        Returns:
            total_volume (float): The total volume that the current items in the inventory sum up to.

        """

        total_volume = 0.0

        return total_volume

    @property
    def equipped_items(self):
        """Gives a list of all equipped items on the character.

        Returns:
             list_of_equipped_items (list): list of all equipment items in the inventory that have their equipped
             attribute set to True.

        """

        list_of_equipped_items = [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped is True]

        return list_of_equipped_items

