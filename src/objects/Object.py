from pydantic import BaseModel
from typing import Literal, TypeVar

from ..physics import HitBox
from ..game_types import Position, GameMode

Game = TypeVar("Game")
GameEvent = TypeVar("GameEvent")

class GameObject:
    def __init__(self, position : tuple[int, int] | Position = (0, 0)):
        hitbox =    '''
                    *
                    '''
        self.hitbox = HitBox(hitbox)
        self.passability = True
        self.intelligent = False
        self.cells : dict = {}
        self.game = None
        if isinstance(position, tuple):
            self._position = Position(position[0], position[1])
        else:
            self._position = position

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, pos : Position | tuple[int, int] | dict):
        if isinstance(pos, tuple):
            self._position = Position(**{"x" : pos[0], "y" : pos[1]})
        if isinstance(pos, dict):
            self._position = Position(**pos)
        else:
            self._position = pos

    def cell_subscribe(self, cell):
        self.cells[id(cell)] = cell
    
    def cell_unsubscribe(self, cell):
        self.cells.pop(id(cell))
    
    def cell_unsubscribe_all(self):
        for cell in self.cells.values():
            self.cell_unsubscribe(cell)

    def game_subscribe(self, game : Game):
        self.game = game
    
    def game_unsubscribe(self):
        self.game = None

    def move(self, field, coords : tuple[int, int], rel=True):
        new_position = Position(coords[0], coords[1])
        if rel:
            new_position += self._position

        print("getting hitbox cells")
        cells = field.get_hitbox_cells(new_position, self.hitbox.mask())
        for cell in cells:
            if not cell.passable():
                raise RuntimeError("cannot set this object on such place. it's not passable!")
        self.cell_unsubscribe_all()
        for cell in cells:
            self.cell_subscribe(cell)
        self._position = new_position
        print("adding objs")
        for cell in self.cells.values():
            cell.add_obj(self)

    def on_field(self) -> bool:
        return len(self.cells) != 0

    def render(self, mode : GameMode = "CONSOLE", frame=None):
        raise NotImplementedError("You cannot render GameObject class!")

class GameObjectIntelligent(GameObject):
    def ask(self, game : Game) -> list[GameEvent] | None:
        raise NotImplementedError("ask func must be implemented for intelligent object")