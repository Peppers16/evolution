import random

# global variables
energy_p_flora = 50


class Board:
    def __init__(self, size=100, start_flora=0):
        self.board = [[None] * size for i in range(size)]
        self.size = size
        # counts
        self.flora_count = 0
        self.creature_count = 0
        # sets and lists for tracking locations and creatures
        self.free_squares = set()
        for i in range(size):
            for j in range(size):
                self.free_squares.add((i, j))
        self.creature_list = []
        self.spawn_flora(start_flora)

    def spawn_flora(self, n_flora):
        """n_flora will be added to the board randomly, subject to free squares being available"""
        for i in range(n_flora):
            if len(self.free_squares):  # if set is non-empty
                x, y = random.choice(tuple(self.free_squares))
                self.board[x][y] = 'F'
                self.flora_count += 1
                self.free_squares.remove((x, y))

    def remove_flora(self, x, y):
        """remove a single flora from the board, and free up the space"""
        if self.board[x][y] != 'F':
            raise Exception("Attempted to remove flora from location where no flora was present")
        self.board[x][y] = None
        self.flora_count -= 1
        self.free_squares.add((x, y))


class Creature:
    def __init__(self, ecosystem, x, y, move_cost):
        self.energy = 100
        self.move_cost = move_cost
        self.ecosystem = ecosystem
        # initial location
        self.location = (x, y)
        self.ecosystem.board[x][y] = self
        self.ecosystem.free_squares.remove((x, y))
        self.ecosystem.creature_count += 1
        self.ecosystem.creature_list.append(self)

    def is_alive(self):
        return self.energy > 0

    def eat_flora(self, x, y):
        if self.ecosystem.board[x][y] != 'F':
            raise Exception(f"Location ({x},{y}) does not contain Flora")
        self.ecosystem.remove_flora(x, y)
        self.energy = min(self.energy + energy_p_flora, 100)

    def move(self, x, y):
        if (x, y) not in self.ecosystem.free_squares:
            raise Exception(f"Location ({x},{y}) is not available")
        else:
            oldx, oldy = self.location
            self.location = (x, y)
            self.ecosystem.board[oldx][oldy] = None
            self.ecosystem.board[x][y] = self
            self.ecosystem.free_squares.add((oldx, oldy))
            self.ecosystem.free_squares.remove((x, y))
            self.energy -= self.move_cost
