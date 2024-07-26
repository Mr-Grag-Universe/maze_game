from time import sleep
import pygame
import sys
from src.game import Game
from src.graphics import Frame
from src.strategy.Brain import SimpleNNBrain

if __name__ == "__main__":
    mode = sys.argv[1]
    game = Game(field_size=(10, 10), mode=mode)
    game.fast_map_config("configs/map.txt")

    brain = SimpleNNBrain()
    # brain.set_weights(weights)

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
    for i in range(100):
        sleep(0.5)

        frame = Frame((10, 10))
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