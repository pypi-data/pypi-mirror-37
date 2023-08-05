"""File defining the player class."""
from .element import Element


class Player(Element):
    """Class defining the player object."""

    def __init__(self, name):
        """Initialize the player object."""
        super().__init__(name)
        self.inv = {}
        self.life = 10

    def move(self, where):
        """Make the player moves."""
        pass

    def attack(self):
        """Make the player attacks."""
        pass

    def use(self, what):
        """Make the player use."""
        pass

    def inventory(self):
        """Print the elements of the player inventory."""
        for elem in self.inv:
            print(elem)
