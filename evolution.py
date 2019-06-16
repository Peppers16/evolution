def create_board(size=100):
    """This board will represent the ecosystem as a square matrix"""
    board = [[None] * size for i in range(size)]
    return board


class Creature:
    def __init__(self):
        self.energy = 100

    def is_alive(self):
        return True
