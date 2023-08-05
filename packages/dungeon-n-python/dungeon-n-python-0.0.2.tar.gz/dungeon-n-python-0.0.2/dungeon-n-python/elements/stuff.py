"""File defining the stuff class."""
from .element import Element


class Stuff(Element):
    """Class defining the stuff object."""

    def __init__(self, name, description):
        """Initialize the object."""
        super().__init__(name)
        self.description = description

    def do_action(self, stdscr, offset_x, offset_y):
        """Make the action of the stuff happen."""
        stdscr.addstr(offset_y, offset_x, self.description)
        return True

    def use(self):
        """Use the stuff."""
        raise NotImplementedError
