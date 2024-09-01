from typing import TypeVar
from . import GameObject
from ..game_types import Position, GameMode, GameEvent
from ..graphics import Asset, Frame
from ..physics import HitBox
from ..strategy.Brain import Brain, SimpleNNBrain

Game = TypeVar("Game")

class Attacker(GameObject):
    def __init__(self, position: tuple[int, int] | Position = {'x' : 0, 'y' : 0}):
        super().__init__(position)
        self.hitbox = HitBox('@')
        self.asset = Asset("@", "Attacker")
        self._brain : Brain = None

        self.passability = False
        self.intelligent = True

    def set_brain(self, brain) -> None:
        self._brain = brain
        print("brain setting: ", brain)

    def render(self, mode : GameMode = "CONSOLE", frame : Frame = None):
        frame.render(self.asset, self.position, mode)
        
    def ask(self, game : Game) -> list[GameEvent] | None:
        direction = self._brain.chose_move_direction(self, game)
        if direction is None:
            return []
        return [GameEvent("MOVE", direction=direction, id=str(id(self)), speed=1.0)]