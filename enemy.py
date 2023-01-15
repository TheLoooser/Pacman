import pygame
from astar import astar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, colour):
        super().__init__()
        self.surf = pygame.Surface((19, 19))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x, y))

        self.pos = pygame.math.Vector2((190, 190))

    def get_path(self, grid, player_position):
        i, j = self.get_current_cell()
        i, j = j, i
        x, y = player_position
        x, y = y, x
        return astar(grid, (i, j), (x, y))

    def get_current_cell(self):
        return int(self.pos.x / 20) % 19, int((self.pos.y - 15) / 20) % 22
