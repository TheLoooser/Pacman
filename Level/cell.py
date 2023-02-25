import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, colour):
        super().__init__()
        self.surf = pygame.Surface((19, 19))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x, y))
