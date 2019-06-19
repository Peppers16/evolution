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
    t_creature = Creature()
    assert t_creature.energy == 100
    assert t_creature.is_alive()

