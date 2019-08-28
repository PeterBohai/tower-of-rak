class ComContainer:
    """Container component gives actor objects an inventory that can hold item objects.

    Attributes
    ----------
    inventory : list
        Contains a list of ComItem objects. Default is empty.
    weight : int
        The current total weight in the container.
    max_weight : int
        The maximum weight the container can carry (in wu - weight units).

    """

    def __init__(self, weight=0, max_weight=20, inventory=[]):
        self.inventory = inventory
        self.weight = weight
        self.max_weight = max_weight

    @property
    def equipped_items(self):
        """list: Gives a list of all items that are currently equipped on the character."""
        return [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped is True]

