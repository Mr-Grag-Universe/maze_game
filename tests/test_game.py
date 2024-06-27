import pytest
from src.game import Game

@pytest.mark.parametrize( ["width", "height", "mode"], [
    (1, 1, "CONSOLE"),
    (10, 10, "CONSOLE"),
    (1, 1, "PYGAME"),
    (10, 10, "PYGAME"),
])
def test_game_initialization(width, height, mode):
    Game((width, height), mode)

@pytest.mark.parametrize( ["width", "height", "mode"], [
    (1, 0, "CONSOLE"),
    (10, -10, "CONSOLE"),
    (1, -1, "PYGAME"),
    (10, 10, "P"),
])
def test_game_wrong_initialization(width, height, mode):
    with pytest.raises(Exception) as exc:
        Game((width, height), mode)