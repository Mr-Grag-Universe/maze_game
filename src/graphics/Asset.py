import pygame

class Asset:
    symbol_img = "#"
    pygame_img = None
    def __init__(self, symbol_img, path=None) -> None:
        self.symbol_img = symbol_img
        if path:
            self.pygame_img = pygame.image.load(f'imgs/{path}/idle.png')