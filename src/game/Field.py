from typing import *
import logging
from pydantic import BaseModel, Field

from . import Cell
from ..objects import GameObject, ObjFabric
from ..types import Position

# логгер модуля
logger = logging.getLogger(__name__)

class GameField:
    def __init__(self, width : int | None = None, height : int | None = None, filename : str | None = None) -> None:
        if width is None and height is None:
            assert filename is not None, RuntimeError("file name and w/h are None!")
            self._config_with_file(filename)

        assert width > 0 and height > 0
        self._width : int = width
        self._height : int = height
        self._cells = [[Cell() for _ in range(width)] for _ in range(height)]

    def _prepare_logger():
        logging.basicConfig(
            filename='Field.log', 
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s"
            )

    def _config_with_file(self, filename : str):
        '''
        упрощённый вариант конфигурации:
        * каждый объект на карте представлен одним символом
        * только определённый набор объектов
        '''
        with open(filename, "r") as config:
            map = config.readlines()
            for i, raw in enumerate(map):
                for j, s in enumerate(raw):
                    cell = Cell()
                    obj = ObjFabric.create_from_symbol(s)
                    obj.move({"x" : j, "y" : i}, rel=False)
                    cell.add_obj(obj)

    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, w : int):
        assert w > 0, RuntimeError("w must be > 0")
        GameField._prepare_logger()
        logger.info(f"field width has been changed from {self._width} to {w}")
        if w < self._width:
            for i in range(self._width):
                self._cells[i] = self._cells[i][:w]
        else:
            for i in range(self._width):
                self._cells[i] = self._cells[i] + [Cell() for _ in range(w - self._width)]
        assert all(w == len(row) for row in self._cells)
        self._width = w
    
    @height.setter
    def height(self, h : int):
        assert h > 0, RuntimeError("h must be > 0")
        GameField._prepare_logger()
        logger.info(f"field height has been changed from {self._height} to {h}")
        if h < self._height:
            self._cells = self._cells[:h]
        else:
            self._cells += [[Cell() for _ in range(self._width)] for _ in range(h - self._height)]
        assert h == len(self._cells)
        self._height = h

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_hitbox_cells(self, position, mask) -> list[Cell]:
        '''
        наложение маски на клетки поля
        возвращает клетки, реально занимаемые объектом, стоящем на координатах position 
        и с хитбоксом формы mask
        '''
        assert len(mask) and max(len(line) for line in mask), RuntimeError("mask size is wrong")
        cells = []
        rows = self._cells[position.y:position.y+len(mask)]
        for cell_line, mask_line in zip(rows, mask):
            for cell, take in zip(cell_line, mask_line):
                if take:
                    cells.append(cell)
        
        return cells
    
    def set_obj_on_field(self, obj : GameObject) -> None:
        cells = self.get_hitbox_cells(obj.position, obj.hitbox.mask())
        for cell in cells:
            cell.add_obj(obj)