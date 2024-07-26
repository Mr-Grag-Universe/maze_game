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