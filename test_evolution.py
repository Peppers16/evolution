from evolution import *
import pytest


def test_are_adjacent():
    assert are_adjacent((1, 1), (1, 2))
    assert are_adjacent((1, 1), (2, 1))
    assert are_adjacent((1, 1), (2, 2))
    assert are_adjacent((1, 1), (2, 0))
    assert are_adjacent((1, 1), (0, 0))
    assert not are_adjacent((1, 1), (3, 1))
    assert not are_adjacent((1, 1), (1, 3))
    assert not are_adjacent((1, 1), (1, 1.5))


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


def test_is_inbounds():
    t_board = Board(3, start_flora=0)
    assert t_board.is_inbounds(2, 2)
    assert not t_board.is_inbounds(3, 2)
    assert not t_board.is_inbounds(-1, 2)
    assert not t_board.is_inbounds(-1.2, 2.4)


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
    with pytest.raises(Exception):  # out of bounds
        t_creature.move(3, 1)
    with pytest.raises(Exception):  # more than a square away
        t_creature.move(0, 1)


def test_eat_flora():
    t_board = Board(3, start_flora=8)
    x, y = t_board.free_squares[0]
    t_creature = Creature(t_board, x, y, move_cost=2)
    t_creature.energy = 80
    t_creature.eat_flora(1, 1)
    assert t_board.flora_count == 7
    assert t_board.board[1][1] == t_creature
    assert 80 < t_creature.energy <= 100
    assert t_creature.location == (1, 1)


