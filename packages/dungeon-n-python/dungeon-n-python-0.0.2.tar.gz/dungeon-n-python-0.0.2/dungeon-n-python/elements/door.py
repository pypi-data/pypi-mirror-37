"""File defining the door class."""
from .element import Element


class Door(Element):
    """Class defining the door."""

    def __init__(self, name):
        """Initialize the door."""
        super().__init__(name)

    def do_action(self, stdscr, offset_x, offset_y):
        """Make the action of the door happen."""
        stdscr.addstr(offset_y, offset_x, "You ended the game")
        return True
