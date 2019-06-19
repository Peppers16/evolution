from evolution import *


def test_board():
    t_board = Board(3, start_flora=0)
    assert t_board.board == \
           [[None, None, None]
            , [None, None, None]
            , [None, None, None]]
    assert t_board.flora_count == 0
    assert len(t_board.free_squares) == 9
    assert t_board.size == 3


def test_spawn_flora():
    t_board = Board(3, start_flora=0)
    assert t_board.flora_count == 0
    assert len(t_board.free_squares) == 9

    t_board.spawn_flora(3)

    assert t_board.flora_count == 3
    assert len(t_board.free_squares) == 6

    print(t_board.board)


def test_remove_flora():
    test_board = Board(6, start_flora=36)
    assert len(test_board.free_squares) == 0
    assert test_board.flora_count == 36
    assert test_board.board[1][2] == 'F'
    test_board.remove_flora(1, 2)
    assert len(test_board.free_squares) == 1
    assert test_board.flora_count == 35
    assert test_board.board[1][2] is None


def test_creature():
    t_board = Board(3, start_flora=0)
    t_creature = Creature(ecosystem=t_board, x=1, y=1, move_cost=None)
    assert t_creature.energy == 100
    assert t_creature.is_alive()
    assert t_creature.ecosystem == t_board
    assert t_creature in t_board.creature_list
    assert t_board.creature_count == 1
    assert t_board.board[1][1] == t_creature
    assert (1, 1) not in t_board.free_squares

def test_eat_flora():
    t_board = Board(3, start_flora=9)
    t_creature = Creature(t_board, move_cost=None)
    t_creature.energy = 80
    t_creature.eat_flora(2, 1)
    assert t_board.flora_count == 8
    assert t_board.board[2][1] != 'F'
    assert 80 < t_creature.energy <= 100


def test_move():
    t_board = Board(3, start_flora=0)
    t_creature = Creature(ecosystem=t_board, x=1, y=1, move_cost=2)
    t_creature.move(2, 1)
    assert t_board.board[1][1] is None
    assert t_board.board[2][1] == t_creature
    assert t_creature.location == (2, 1)
    assert t_creature.energy == 98
    assert (1, 1) in t_board.free_squares
    assert (2, 1) not in t_board.free_squares

    # should we also test that the location is valid, and adjacent to the creature?