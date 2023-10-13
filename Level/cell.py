"""
This module contains an implementation of a Cell object using a pygame sprite.
"""
import pygame


class Cell(pygame.sprite.Sprite):
    """
    A class to represent a sprite of a cell
    """

    def __init__(self, x: int, y: int, colour: tuple[int, int, int]):
        """
        Constructs a cell sprite.

        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :param colour: The colour of the cell/sprite.
        """
        super().__init__()
        self.surf = pygame.Surface((19, 19))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x, y))
