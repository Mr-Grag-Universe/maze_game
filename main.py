from time import sleep
import pygame
import sys
from src.game import Game
from src.graphics import Frame

if __name__ == "__main__":
    mode = sys.argv[1]
    game = Game(field_size=(10, 10), mode=mode)
    game.fast_map_config("configs/map.txt")

    if mode == "PYGAME":
        pygame.init()
        screen = pygame.display.set_mode((10*64, 10*64))

    STOP_GAME = False
    for i in range(100):
        # sleep(0.5)

        frame = Frame((10, 10))
        if mode == "PYGAME":
            frame.attach_screen(screen)
            frame.set_cell_size(64)
        game.render(frame=frame)
        frame.show()

        if mode == "PYGAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        STOP_GAME = True
            pygame.display.flip()

        if STOP_GAME:
            break