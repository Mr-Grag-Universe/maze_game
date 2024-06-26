from . import GameObject
from ..types import Position, GameMode
from ..graphics import Asset, Frame
from ..physics import HitBox

class Attacker(GameObject):
    def __init__(self, position: tuple[int, int] | Position = {'x' : 0, 'y' : 0}):
        super().__init__(position)
        self.hitbox = HitBox('@')
        self.asset = Asset("@", "Attacker")

    def render(self, mode : GameMode = "CONSOLE", frame : Frame = None):
        frame.render(self.asset, self.position, mode)