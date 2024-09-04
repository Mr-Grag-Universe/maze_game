from typing import Literal, TypeAlias
from pydantic import BaseModel, Field, validate_call
from . import GameField
from ..objects import GameObject, GameObjectIntelligent, ObjFabric
from ..game_types import GameEvent, GameMode
import pygame

class Game:
    objects : dict[str, GameObject]
    intelligent_objects : dict[str, GameObjectIntelligent]
    obj_under_controll : dict[str, GameObject]
    field : GameField
    _mode : GameMode

    @validate_call
    def __init__(self, field_size : tuple[int, int] = (10, 10), mode : GameMode = "CONSOLE") -> None:
        self.objects : dict[str, GameObject] = {}
        self.intelligent_objects : dict[str, GameObjectIntelligent] = {}
        self.obj_under_controll : dict[str, GameObject] = {}
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

                    if symbol == 'h':
                        self.obj_under_controll[str(id(obj))] = obj

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

    def _process_events(self, events : list[GameEvent]) -> None:
        for event in events:
            if not self._process_event(event):
                print("cannot run this commond successfully")
            else:
                print("success!")

    def process_events(self) -> bool:
        # возвращает, был ли сигнал для завершения работы
        game_events = []

        # выслушиваем наши сущности с интелектом
        asks = self.ask_intelligent()
        print(f'{asks=}')
        game_events += asks

        if self.mode == "PYGAME":
            # получаем пачку поступивших событий
            events = pygame.event.get()
            event_types = set(map(lambda x : x.type, events))
            
            if pygame.QUIT in event_types:
                return True
            
            # движения персонажа
            MOVE_KEYS_HORIZONTAL = {pygame.K_RIGHT, pygame.K_LEFT}
            MOVE_KEYS_VERTICAL = {pygame.K_UP, pygame.K_DOWN}
            MOVE_KEYS = MOVE_KEYS_HORIZONTAL.union(MOVE_KEYS_VERTICAL)
            if pygame.KEYDOWN in event_types:
                key_events = list(filter(lambda x : x.type == pygame.KEYDOWN, events))
                event_keys = list(map(lambda x : x.key, key_events))
                move_keys = list(filter(lambda x : x in MOVE_KEYS, event_keys))
                move_keys_horizontal = list(filter(lambda x : x in MOVE_KEYS_HORIZONTAL, move_keys))
                move_keys_vertical = list(filter(lambda x : x in MOVE_KEYS_VERTICAL, move_keys))

                move_dir_horizontal = None
                move_dir_vertical = None
                if len(move_keys_horizontal):
                    move_dir_horizontal = "RIGHT" if move_keys_horizontal[-1] == pygame.K_RIGHT else "LEFT"
                if len(move_keys_vertical):
                    move_dir_vertical = "UP" if move_keys_vertical[-1] == pygame.K_UP else "DOWN"
                
                if move_dir_horizontal is not None or move_dir_vertical is not None:
                    if move_dir_vertical is None:
                        # двигаемся только по горизонтали
                        game_events += [GameEvent("MOVE", direction=move_dir_horizontal, id=obj_id, speed=1.0) for obj_id in self.obj_under_controll]
                    elif move_dir_horizontal is None:
                        # двигаемся только по вертикали
                        game_events += [GameEvent("MOVE", direction=move_dir_vertical, id=obj_id, speed=1.0) for obj_id in self.obj_under_controll]
                    else:
                        # двигаемся по диагонали
                        pass
        else:
            # TODO : обработчик событий для консольного варианта
            pass

        self._process_events(game_events)
        return False