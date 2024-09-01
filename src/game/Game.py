from typing import Literal, TypeAlias
from pydantic import BaseModel, Field, validate_call
from . import GameField
from ..objects import GameObject, GameObjectIntelligent, ObjFabric
from ..game_types import GameEvent, GameMode

class Game:
    objects : dict[str, GameObject]
    intelligent_objects : dict[str, GameObjectIntelligent]
    field : GameField
    _mode : GameMode

    @validate_call
    def __init__(self, field_size : tuple[int, int] = (10, 10), mode : GameMode = "CONSOLE") -> None:
        self.objects : dict[str, GameObject] = {}
        self.intelligent_objects : dict[str, GameObjectIntelligent] = {}
        self.field = GameField(*field_size)
        self._mode : GameMode = mode
    
    @property
    def mode(self) -> GameMode:
        return self._mode
    @mode.setter
    def mode(self, mode : GameMode) -> None:
        self._mode = mode

    def collect_render_objs(self) -> list[GameObject]:
        on_filed_objs = []
        for obj in self.objects.values():
            # если хоть кусочек hitbox попадает на поле - берём
            if obj.on_field():
                on_filed_objs += [obj]
        return on_filed_objs

    def render(self, /, **kwargs) -> None:
        objs = self.collect_render_objs()
        for obj in objs:
            obj.render(mode=self._mode, **kwargs)

    def add_object(self, obj : GameObject, tag : str | None = None) -> None:
        if tag is None:
            tag = str(id(obj))
        if tag in self.objects:
            raise ValueError("such object already exists in this game")
        self.objects[tag] = obj
        if obj.intelligent:
            self.intelligent_objects[tag] = obj

    @validate_call
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
                    
                    self.objects[str(id(obj))] = obj
                    if obj.intelligent:
                        self.intelligent_objects[str(id(obj))] = obj

                    # print("obj_pos: ", i, j)
                    # print(self.field._cells)
                    self.field.set_obj_on_field(obj)

    @validate_call
    def ask_intelligent(self) -> list[GameEvent]:
        asks = []
        # можно просто проверять наличие метода и флажка, а не хранить массив разумных объектов
        for obj in self.intelligent_objects.values():
            ask : list[GameEvent] | None = obj.ask(self)
            if ask is not None:
                asks.extend(ask)
        
        return asks
    
    def _process_event(self, event : GameEvent) -> bool:
        match event.event:
            case "MOVE":
                obj = self.intelligent_objects[event.kwargs['id']]
                direction = event.kwargs['direction']
                r = [0, 0]
                match direction:
                    case "UP":
                        r = [0, -1]
                    case "DOWN":
                        r = [0, 1]
                    case "RIGHT":
                        r = [1, 0]
                    case "LEFT":
                        r = [-1, 0]
                    case _:
                        raise ValueError(f"cannot move this way: {direction}")
                try:
                    print(f"moving from {obj.position} to {direction} rel")
                    obj.move(self.field, r, rel=True)
                    return True
                except RuntimeError as exc:
                    # raise exc
                    return False
            case _:
                raise ValueError(f"uknown event processing: {event.event}")

    def process_events(self, events : list[GameEvent]) -> None:
        for event in events:
            if not self._process_event(event):
                print("cannot run this commond successfully")
            else:
                print("success!")