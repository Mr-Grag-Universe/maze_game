import os
import pygame
from . import Asset
from ..game_types import GameMode, Position

class Frame:
    def __init__(self, field_size) -> None:
        self.map = [[" "] * field_size[0] for _ in range(field_size[1])]
        self.screen = None
        self.cell_size = None

    def attach_screen(self, screen : pygame.Surface) -> None:
        self.screen = screen

    def set_cell_size(self, size=8) -> None:
        self.cell_size = size

    def show(self, mode):
        print("show")
        # os.system('cls')
        match mode:
            case "CONSOLE":
                for line in self.map:
                    print(''.join(line))
            case "PYGAME":
                pass
            case _:
                raise RuntimeError(f"There is not such <{mode}> mode!")

    def render(self, asset : Asset, position : Position, mode : GameMode = "CONSOLE"):
        match mode:
            case "CONSOLE":
                symbol_img = asset.symbol_img
                for i, line in enumerate(symbol_img):
                    self.map[position.y][position.x : position.x+len(line)] = list(line)
            case "PYGAME":
                pygame_asset = asset.pygame_img
                position = list(position.to_tuple())
                position[0] *= self.cell_size
                position[1] *= self.cell_size
                self.screen.blit(pygame_asset, position)
            case _:
                raise NotImplementedError("this mode rendering is not implemented yet")

    def __repr__(self) -> str:
        return "<Frame: \n" + '\n'.join(str(self.map)) + "\n>"