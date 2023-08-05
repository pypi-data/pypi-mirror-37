"""
    Generate a lab
"""

from random import *
import random
import elements

class Maze:
    """
        The maze is the map of the game composed of blocs containing one Entity
    """
    
    def random_elem(self):
        type_elem = randrange(0, len(self.datas))
        if (self.datas[type_elem] is None):
            return None
        data = self.datas[type_elem]["data"]
        if self.datas[type_elem]["type"] == "monster":
            monster = data[randrange(0, len(data))]
            question = monster["askings"][randrange(0, len(monster["askings"]))]
            try:
                asciii = monstre["ascii"]
            except:
                asciii = "\O_O/"
            return elements.Monster(
                    monster["name"],
                    question["ask"],
                    question["ok"],
                    question["ko"],
                    question["good"],
                    monster["intro"],
                    asciii
            )
        elif self.datas[type_elem]["type"] == "event":
            event = data[randrange(0, len(data))]
            return elements.Event(event["event"], event["func"])
        else:
            return elements.Stuff()

    def generate(self, x, y):
        """
            Generate the maze
        """
        self.blocks = []
        for i in range(y):
            self.blocks.append([])
            for j in range(x):
                self.blocks[i].append(self.random_elem())
        self.blocks[self.pos[0]][self.pos[1]] = elements.Event("Welcome to D&P Dungeon and Python. {Insert Tutorial}", "self.solved == True")

    def __init__(self, x, y, events, monsters):
        self.x = x
        self.y = y
        self.pos = [random.randrange(0, x), random.randrange(0, y)]
        self.datas = [monsters, events]
        self.generate(x, y)

    def move(self, x, y):
        """
            Move inside the blocs
        """
        self.pos[0] += x
        self.pos[1] += y
        try:
            new = self.maze[self.pos[0]][self.pos[1]]
        except IndexError:
            new = None
        finally:
            if new == None:
                print("It's a wall you stay in this room !")
            else:
                self.actual_bloc = new
                

