"""
Simple labyrinth.

Simple game for labyrinth escaping using
knowledge from first year at Epitech.
"""

from ctrlc import DelayedKeyboardInterrupt
from game import Game
import curses


def main(len_x, len_y):
    """Make some assertions before beggining the game."""

    def game_main(stdscr):
        """Run the game."""
        game = Game(len_x, len_y)
        game.play(stdscr)

    with DelayedKeyboardInterrupt():
        curses.wrapper(game_main)


if __name__ == "__main__":
    main(7, 7)

