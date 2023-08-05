"""File defining the base element class."""


class Element(object):
    """Class defining the base element."""

    def __init__(self, name):
        """Initialize the object."""
        self.name = name
        self.solved = False

    def do_action(self, stdscr, offsetX, offsetY):
        """Make the action of the base element happen."""
        raise NotImplementedError

    def draw(self, stdscr, offsetX, offsetY):
        """Draw the representation of the element."""
        stdscr.addstr(offsetY, offsetX, "\o/")

    def __str__(self):
        """Return the string version of the object."""
        return self.name
