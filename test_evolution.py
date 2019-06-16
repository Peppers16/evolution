from evolution import *


def test_board():
    t_board = create_board(3)
    assert t_board == \
           [[None, None, None]
            , [None, None, None]
            , [None, None, None]]

    t_board[1][1] = 'X'

    assert t_board == \
           [[None, None, None]
            , [None, 'X', None]
            , [None, None, None]]


def test_creature():
    t_creature = Creature()
    assert t_creature.energy == 100
    assert t_creature.is_alive()

