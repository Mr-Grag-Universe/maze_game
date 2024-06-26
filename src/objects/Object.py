from pydantic import BaseModel
from typing import Literal

from ..physics import HitBox
from ..types import Position, GameMode

class GameObject:
    def __init__(self, position : tuple[int, int] | Position = (0, 0)):
        hitbox =    '''
                    *
                    '''
        self.hitbox = HitBox(hitbox)
        self.passability = True
        self.cells = []
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

    def subscribe(self, cell):
        self.cells.append(cell)
    
    def unsubscribe(self, cell):
        self.cells.remove(cell)
    
    def unsubscribe_all(self):
        for cell in self.cells:
            self.unsubscribe(cell)

    def move(self, field, coords : tuple[int, int], rel=True):
        self.unsubscribe_all()
        new_position = Position(coords[0], coords[1])
        if rel:
            new_position += self._position

        self.cells = field.get_hitbox_cells(new_position, self.hitbox.mask())
        self._position = new_position
        for cell in self.cells:
            cell.add_obj(self)

    def on_field(self) -> bool:
        return len(self.cells) != 0

    def render(self, mode : GameMode = "CONSOLE", frame=None):
        raise NotImplementedError("You cannot render GameObject class!")