from time import sleep
import pygame
import sys
from src.game import Game
from src.graphics import Frame
from src.strategy.Brain import SimpleNNBrain

if __name__ == "__main__":
    mode = sys.argv[1]
    game = Game(field_size=(12, 11), mode=mode)
    game.fast_map_config("configs/maze_1.txt")

    # brain = SimpleNNBrain()
    # brain.set_weights(weights)

    for obj in game.intelligent_objects.values():
        print("obj for braining: ", obj)
        # try:
        #     obj.set_brain(brain)
        #     print("brain setted")
        # except Exception as exc:
        #     print(exc)

    if mode == "PYGAME":
        pygame.init()
        screen = pygame.display.set_mode((11*64, 12*64), vsync=True)

    STOP_GAME = False
    for i in range(100):
        sleep(0.5)

        frame = Frame((11, 12))
        if mode == "PYGAME":
            frame.attach_screen(screen)
            frame.set_cell_size(64)
            background = pygame.Surface(screen.get_size())
            background.fill((0, 0, 0))
            screen.blit(background, (0, 0))
        game.render(frame=frame)
        frame.show(mode)

        STOP_GAME = game.process_events()

        if mode == "PYGAME":
            pygame.display.flip()

        if STOP_GAME:
            if mode == 'PYGAME':
                pygame.quit()
            break