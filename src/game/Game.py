from typing import Literal, TypeAlias
from . import GameField
from ..objects import GameObject, ObjFabric
from ..game_types import GameMode

class Game:
    def __init__(self, field_size : tuple[int, int] = (10, 10), mode : GameMode = "CONSOLE"):
        self.objects : list[GameObject] = []
        self.field = GameField(*field_size)
        self._mode = mode
    
    @property
    def mode(self) -> GameMode:
        return self._mode
    @mode.setter
    def mode(self, mode : GameMode) -> None:
        self._mode = mode

    def collect_render_objs(self) -> list[GameObject]:
        on_filed_objs = []
        for obj in self.objects:
            # если хоть кусочек hitbox попадает на поле - берём
            if obj.on_field():
                on_filed_objs += [obj]
        return on_filed_objs

    def render(self, /, **kwargs) -> None:
        objs = self.collect_render_objs()
        for obj in objs:
            obj.render(mode=self._mode, **kwargs)

    def add_object(self, obj : GameObject) -> None:
        self.objects.append(obj)

    def fast_map_config(self, file_name : str) -> None:
        str_map : list[str]
        with open(file_name, "r") as file:
            str_map = list(map(lambda line : line.strip('\n'), file.readlines()))
        print(str_map)
        assert all(len(line) == len(str_map[0]) for line in str_map), RuntimeError("lens of lines in map config are not the same")

        width, height = len(str_map[0]), len(str_map)
        self.field = GameField(width, height)

        for i, line in enumerate(str_map):
            for j, symbol in enumerate(line):
                if symbol != ' ':
                    obj = ObjFabric.create_from_symbol(symbol)
                    obj.position = {'x' : j, 'y' : i}
                    self.objects.append(obj)
                    self.field.set_obj_on_field(obj)
                    