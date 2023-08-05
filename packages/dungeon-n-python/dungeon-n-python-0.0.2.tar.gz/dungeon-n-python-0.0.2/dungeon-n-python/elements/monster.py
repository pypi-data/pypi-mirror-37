"""File defining the minster class."""
from .element import Element


class Monster(Element):
    """Define a monster in the game."""

    def __init__(self, name, ask, ok, ko, waited, intro, asciii):
        """Initialize the monster."""
        super().__init__(name)
        self.intro = intro
        self.ascii = asciii
        self.ask = ask
        self.ok = ok
        self.ko = ko
        self.waited = waited

    def do_action(self, stdscr, offsetX, offsetY):
        """Make the action of the monster happens."""
        stdscr.addstr(offsetY, offsetX, self.ascii)
        stdscr.addstr(offsetY, offsetX, self.intro)
        stdscr.addstr(offsetY, offsetX, self.ask)
        line = None
        while True:
            try:
                stdscr.addstr(offsetY, offsetX, "Enter message: (hit Ctrl-G to send): ")
                editwin = curses.newwin(5,30, 2,1)
                rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
                stdscr.refresh()
                box = Textbox(editwin)
                box.edit()
                line = box.gather()
            except EOFError:
                stdscr.addstr(offsetY, offsetX, "Are you trying to quit ?!")
            else:
                break

        if line == self.waited:
            stdscr.addstr(offsetY, offsetX, self.ok)
            self.solved = True
        else:
            stdscr.addstr(offsetY, offsetX, self.ko)
            self.solved = False

