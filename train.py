import time
from src.game import Game
import pygame
from src.graphics import Frame
from src.strategy.Brain import SimpleNNBrain
import numpy as np

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# import tensorflow as tf


INPUT_SHAPE = 4
OUTPUT_SHAPE = 4

def run(weights, mode="CONSOLE"):
    brain = SimpleNNBrain()
    brain.set_weights(weights)

    game = Game(field_size=(10, 10), mode=mode)
    game.fast_map_config("configs/maze.txt")
    for obj in game.intelligent_objects.values():
        print("obj for braining: ", obj)
        try:
            obj.set_brain(brain)
            print("brain setted")
        except Exception as exc:
            print(exc)

    if mode == "PYGAME":
        pygame.init()
        screen = pygame.display.set_mode((10*64, 10*64))
    
    STOP_GAME = False
    x = 100
    for i in range(100):
        time.sleep(0.5)

        frame = Frame(game.field.get_size())
        if mode == "PYGAME":
            frame.attach_screen(screen)
            frame.set_cell_size(64)
            screen.fill((0, 0, 0))
        game.render(frame=frame)
        frame.show()

        if mode == "PYGAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        STOP_GAME = True
            pygame.display.flip()

        asks = game.ask_intelligent()
        print(asks)
        game.process_events(asks)

        if STOP_GAME:
            break 

        x -= 1 
    
    return x

if __name__ == "__main__":
    population_1 = np.random.randn(5, 4, 4)
    population_2 = np.random.randn(5, 4)
    
    run([population_1[0], population_2[0]], "PYGAME")
