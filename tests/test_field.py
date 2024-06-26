import pytest
import logging
import decorator
from src.game import GameField as Field
from src.types import Position

def disable_logging(func):
    def wrapper(func, *args, **kwargs):
        logging.disable(logging.CRITICAL)
        res = func(*args, **kwargs)
        logging.disable(logging.NOTSET)
        return res
    return decorator.decorator(wrapper, func)

@pytest.mark.parametrize( ["width", "height"], [
    (1, 3),
    (3, 4),
    (20, 50)
])
def test_field_initialization(width, height):
    field = Field(width, height)
    assert field.width == width
    assert field.height == height

@pytest.mark.parametrize( ["width", "height"], [
    (1, -1),
    (3, -4),
    (-20, -50),
    (0, 1),
    (20, 0),
    (0, 0)
])
def test_field_wrong_initialization(width, height):
    with pytest.raises(Exception) as exc:
        field = Field(width, height)

# @disable_logging
@pytest.mark.parametrize( ["width"], [
    (1,),
    (7,)
])
def test_field_width_change(width):
    field = Field(5, 5)
    field.width = width
    assert field.width == width

# @disable_logging
@pytest.mark.parametrize( ["height"], [
    (1,),
    (7,)
])
def test_field_height_change(height):
    field = Field(5, 5)
    field.height = height
    assert field.height == height

# @disable_logging
def test_field_get_size():
    field = Field(5, 5)
    assert field.get_size() == (5, 5)

def test_field_mask_cells():
    field = Field(5, 5)
    cells = field.get_hitbox_cells(Position(0, 0), [[0, 1, 0], [1, 0, 1]])
    assert len(cells) == 3


if __name__ == "__main__":
    pytest.main()

