from . import GameObject
from ..game_types import Position, GameMode
from ..graphics import Asset, Frame
from ..physics import HitBox

class Wall(GameObject):
    def __init__(self, position: tuple[int, int] | Position = {'x' : 0, 'y' : 0}):
        super().__init__(position)
        self.hitbox = HitBox('#')
        self.asset = Asset("#", "Wall")

    def render(self, mode : GameMode = "CONSOLE", frame : Frame = None):
        frame.render(self.asset, self.position, mode)