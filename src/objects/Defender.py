from typing import TypeVar
from . import GameObject
from ..game_types import Position, GameEvent, GameMode
from ..graphics import Asset, Frame
from ..physics import HitBox

Game = TypeVar("Game")

class Defender(GameObject):
    def __init__(self, position: tuple[int, int] | Position | dict = {'x' : 0, 'y' : 0}):
        super().__init__(position)
        self.hitbox = HitBox('*')
        self.asset = Asset("&", "Defender")
        
        self.passability = False
        self.intelligent = True

    def render(self, mode : GameMode = "CONSOLE", frame : Frame = None):
        frame.render(self.asset, self.position, mode)

    def ask(self, game : Game) -> list[GameEvent] | None:
        return [GameEvent("MOVE", direction="DOWN", id=str(id(self)), speed=1.0)]