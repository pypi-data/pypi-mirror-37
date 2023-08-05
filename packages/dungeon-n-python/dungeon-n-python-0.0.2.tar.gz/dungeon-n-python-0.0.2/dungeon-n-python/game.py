"""
    Game
"""
import curses
import readline
from maze import Maze
from elements import Player
import json

def clear_screen():
        print("\033[2J")
        print("\033[1;1H")

def has_wall(block):
    pass

class Game:

    def get_data(self, filename):
        with open("assets/" + filename) as f:
            data = json.load(f)
        return data

    def __init__(self, x, y):
        self.player = Player("Player 1")
        self.playing = True
        self.monster_data = self.get_data("monster.json")
        self.event_data = self.get_data("event.json")
        self.maze = Maze(x, y, self.event_data, self.monster_data)

    def print_block(self, block, x, y, stdscr, offsetX, offsetY):
        """Print a block in the labyrinth."""
        if (y == 0 or has_wall(block) == 0):
            stdscr.addstr((y * 4) + offsetY, (x * 6) + offsetX, '━━━━━━')
        else:
            stdscr.addstr((y * 4) + offsetY, (x * 6) + offsetX, '──────')
        if (x == 0 or has_wall(block == 3)):
            stdscr.addstr((y * 4) + offsetY, offsetX, '┏' if y == 0 else '┠')
            stdscr.addstr((y * 4) + 1 + offsetY, offsetX, '┃')
            stdscr.addstr((y * 4) + 2 + offsetY, offsetX, '┃')
            stdscr.addstr((y * 4) + 3 + offsetY, offsetX, '┃')
        else:
            stdscr.addstr((y * 4) + offsetY, (x * 6) + offsetX, '┯' if y == 0 else '┼')
            stdscr.addstr((y * 4) + 1 + offsetY, (x * 6) + offsetX, '│')
            stdscr.addstr((y * 4) + 2 + offsetY, (x * 6) + offsetX, '│')
            stdscr.addstr((y * 4) + 3 + offsetY, (x * 6) + offsetX, '│')
        if (y == self.maze.y - 1 or has_wall(block) == 2):
            stdscr.addstr(((y + 1) * 4) + offsetY, (x * 6) + offsetX, '┗━━━━━' if x == 0 else '┷━━━━━')
        if (x == self.maze.x - 1 or has_wall(block) == 1):
            stdscr.addstr((y * 4) + offsetY, ((x + 1) * 6) + offsetX, '┓' if y == 0 else '┨')
            stdscr.addstr((y * 4) + 1 + offsetY, ((x + 1) * 6) + offsetX, '┃')
            stdscr.addstr((y * 4) + 2 + offsetY, ((x + 1) * 6) + offsetX, '┃')
            stdscr.addstr((y * 4) + 3 + offsetY, ((x + 1) * 6) + offsetX, '┃')
        if (x == self.maze.x - 1 and y == self.maze.y - 1):
            stdscr.addstr(((y + 1) * 4) + offsetY, ((x + 1) * 6) + offsetX, '┛')
        if (self.maze.pos[0] == x and self.maze.pos[1] == y):
            stdscr.addstr(((y) * 4) + 2 + offsetY, ((x) * 6) + 3 + offsetX, 'X', curses.color_pair(1))
        

    def print_maze(self, stdscr):
        for row, y in zip(self.maze.blocks, range(self.maze.y)):
            for block, x in zip(row, range(self.maze.y)):
                self.print_block(block, x, y, stdscr, 0, 0)


    def play(self, stdscr):
        stdscr.clear()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        while self.playing:
            stdscr.clear()
            self.print_maze(stdscr)
            stdscr.refresh()
            if (self.maze.blocks[self.maze.pos[0]][self.maze.pos[1]].solved):
                c = stdscr.getch()
                if c == curses.KEY_LEFT:
                    self.maze.pos[0] -= 1
                elif c == curses.KEY_RIGHT:
                    self.maze.pos[0] += 1
                elif c == curses.KEY_UP:
                    self.maze.pos[1] -= 1
                elif c == curses.KEY_DOWN:
                    self.maze.pos[1] += 1
                elif c == ord("e"):
                    return
            else:
                curses.echo()
                stdscr.clear()
                stdscr.refresh()
                self.maze.blocks[self.maze.pos[0]][self.maze.pos[1]].do_action(stdscr, 0, 0)
                curses.noecho()
