import random

# global variables
energy_p_flora = 50


def are_adjacent(loc1, loc2):
    """takes two coordinates and returns true if they are adjacent, horizontally or diagonally"""
    x1, y1 = loc1
    x2, y2 = loc2
    if x1 == x2 and abs(y1 - y2) == 1:
        return True
    if y1 == y2 and abs(x1 - x2) == 1:
        return True
    return abs(x1 - x2) == 1 and abs(y1 - y2) == 1


class Board:
    def __init__(self, size=100, start_flora=0):
        self.board = [[None] * size for i in range(size)]
        self.size = size
        # counts
        self.flora_count = 0
        self.creature_count = 0
        # lists for tracking locations and creatures
        self.free_squares = []
        for i in range(size):
            for j in range(size):
                self.free_squares.append((i, j))
        self.creature_list = []
        self.spawn_flora(start_flora)

    def spawn_flora(self, n_flora):
        """n_flora will be added to the board randomly, subject to free squares being available"""
        for i in range(n_flora):
            if len(self.free_squares):  # if set is non-empty
                x, y = random.choice(self.free_squares)
                self.board[x][y] = 'F'
                self.flora_count += 1
                self.free_squares.remove((x, y))

    def remove_flora(self, x, y):
        """remove a single flora from the board, and free up the space"""
        if self.board[x][y] != 'F':
            raise Exception("Attempted to remove flora from location where no flora was present")
        self.board[x][y] = None
        self.flora_count -= 1
        self.free_squares.append((x, y))

    def is_inbounds(self, x, y):
        return x in range(self.size) and y in range(self.size)

    def is_available(self, x, y):
        return (x, y) in self.free_squares


class Creature:
    def __init__(self, ecosystem, x, y, move_cost):
        self.energy = 100
        self.move_cost = move_cost
        self.ecosystem = ecosystem
        # initial location
        if not self.ecosystem.is_available(x, y):
            raise Exception(f"Location ({x},{y}) is not available")
        self.location = (x, y)
        self.ecosystem.board[x][y] = self
        self.ecosystem.free_squares.remove((x, y))
        self.ecosystem.creature_count += 1
        self.ecosystem.creature_list.append(self)

    def is_alive(self):
        return self.energy > 0

    def eat_flora(self, x, y):
        if not are_adjacent(self.location, (x, y)):
            raise Exception(f"Creature in {self.location} not adjacent to flora in {(x, y)}, so cannot eat")
        if self.ecosystem.board[x][y] != 'F':
            raise Exception(f"Location ({x},{y}) does not contain Flora")
        self.ecosystem.remove_flora(x, y)
        self.energy = min(self.energy + energy_p_flora, 100)
        self.move(x, y)

    def move(self, x, y):
        if not self.ecosystem.is_available(x, y):
            raise Exception(f"Location ({x},{y}) is not available")
        if not are_adjacent(self.location, (x, y)):
            raise Exception(f"Current location {self.location} is not adjacent to ({x}, {y})")
        else:
            oldx, oldy = self.location
            self.location = (x, y)
            self.ecosystem.board[oldx][oldy] = None
            self.ecosystem.board[x][y] = self
            self.ecosystem.free_squares.append((oldx, oldy))
            self.ecosystem.free_squares.remove((x, y))
            self.energy -= self.move_cost
