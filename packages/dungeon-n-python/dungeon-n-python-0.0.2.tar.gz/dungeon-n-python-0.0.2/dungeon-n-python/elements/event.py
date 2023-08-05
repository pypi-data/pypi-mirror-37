"""File defining the Event class."""
from .element import Element


class Event(Element):
    """Class defining the event."""

    def __init__(self, event, func):
        """Initialize the object."""
        super().__init__(event)
        self.description = event
        self.func = func

    def do_action(self, stdscr, offset_x, offset_y):
        """Make the action of the event happen."""
        stdscr.addstr(offset_y, offset_x, self.description)
        eval(self.func)
        self.solved = True
