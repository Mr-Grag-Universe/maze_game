import pytest
from src.game import GameField
from src.objects import GameObject

def test_obj_init():
    obj = GameObject()


@pytest.mark.parametrize(["width", "height", "pos", "coords", "rel"], [
    [10, 10, (1, 1), (1, 1), False],
    [10, 10, (8, 8), (5, 5), False],
    [10, 10, (1, 1), (-5, -5), False],
    [10, 10, (7, 7), (-5, -5), False],
    [10, 10, (1, 1), (1, 1), True],
    [10, 10, (8, 8), (5, 5), True],
    [10, 10, (1, 1), (-5, -5), True],
    [10, 10, (7, 7), (-5, -5), True],
])
def test_obj_move(width, height, pos, coords, rel):
    field = GameField(width, height)
    obj = GameObject(position=pos)
    obj.move(field, coords, rel)
    assert  (obj.position == coords and not rel) ^ (obj.position == (coords[0]+pos[0], coords[1]+pos[1]) and rel), RuntimeError("wrong move")

def test_obj_hitbox():
    pass