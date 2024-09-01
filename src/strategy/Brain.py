from typing import Literal
# import tensorflow as tf
import numpy as np
import random

class Brain:
    INPUT_SHAPE = 4
    OUTPUT_SHAPE = 4


class SimpleNNBrain(Brain):
    def __init__(self):
        self.model = None

    def set_weights(self, weights) -> None:
        # self.model = tf.keras.Sequential([
        #     tf.keras.layers.Dense(self.OUTPUT_SHAPE, activation="softmax", input_shape=(self.INPUT_SHAPE,))
        # ])
        # print(self.model.layers[0].get_weights())
        self.model.layers[0].set_weights(weights)

    def chose_move_direction(self, data) -> Literal["UP", "DOWN", "RIGHT", "LEFT"]:
        res = random.choice([0, 1]) # self.model.predict(np.array([data]))
        return ["UP", "DOWN", "RIGHT", "LEFT"][np.argmax(res)]
    

class KeeperBrain(Brain):
    def __init__(self):
        self._mode : Literal["RAGE", "CALM"] = "CALM"
        self._vis_range : int = 5
        self._view_angle : float = np.pi / 4
        self._interesting_types : set[str] = set(["Defender"])
        
        # настраиваемые параметры
        self._max_inertia_time : int = 2
        self._max_one_dir_time : int = 3

        self._dir = np.random.choice(["UP", "DOWN", "RIGHT", "LEFT"])
        self._inertia_time : int = 0
        self._one_dir_time : int = 0

    def set_weights(self, weights) -> None:
        # можно потом продумать установку параметров по отдельности (например через NA значения)
        self._inertia_time, self._dir_time = weights

    def _is_interesting(self, obj):
        return str(type(obj)) in self._interesting_types

    def _see_somebody(self, keeper, game) -> None | int:
        # None если не видит
        # расстояние, если видит
        pos = keeper.position
        x_right, y_down = pos.to_tuple()
        x_left, y_top = x_right, y_down
        # границы включены
        match self._dir:
            case "RIGHT":
                x_left, x_right = x_right, min(x_right+self._vis_range, game.field.width-1)
            case "LEFT":
                x_left = max(x_right-self._vis_range, 0)
            case "UP":
                y_top = max(y_down-self._vis_range, 0)
            case "DOWN":
                y_top, y_down = y_down, min(y_top+self._vis_range, game.field.height-1)
            case _:
                raise RuntimeError(f"there is not <{self._dir}> direction")
        if x_left == x_right:
            cells = game.field._cells[x_left][y_top:y_down+1]
        elif y_top == y_down:
            cells = list(map(lambda row : row[y_top], game.field._cells[x_left:x_right+1]))
        # разворачиваем в порядке удаления от ловца
        if self._dir in ["UP", "LEFT"]:
            cells = cells[::-1]

        for i, cell in enumerate(cells):
            for obj_id, obj in cell.objects.items():
                # можно подумать над коллизиями потом
                if not obj.passability:
                    return None
                if self._is_interesting(obj):
                    return i
        # пропишу явно
        return None
            
    def _chose_dir(self, keeper, game):
        return np.random.choice(["UP", "DOWN", "RIGHT", "LEFT"])

    def chose_move_direction(self, keeper, game) -> Literal["UP", "DOWN", "RIGHT", "LEFT"]:
        # если видим игрока - бежим за ним пока не закончится инерция
        dist = self._see_somebody(keeper, game)
        if dist is not None:
            self._inertia_time = self._max_inertia_time
            return self._dir
        
        # если инерция есть - бежим вперёд
        # TODO : надо добавить вариант, что если упёрся в стену, то меняет маршрут (сразу или нет)
        if self._inertia_time > 0:
            self._inertia_time -= 1
            return self._dir
        
        # если мы никого не видим и нет инерции - смотрим таймер смены направления движения
        if self._one_dir_time >= self._max_one_dir_time:
            self._one_dir_time = 0
            self._dir = self._chose_dir(keeper, game)
            return None
        
        self._one_dir_time += 1
        return self._dir