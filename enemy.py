import pygame
from astar import astar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, colour):
        super().__init__()
        self.surf = pygame.Surface((19, 19))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x, y))

        self.pos = pygame.math.Vector2((x, y))
        self.vel = pygame.math.Vector2(0, 0)

    def get_path(self, grid, player_position):
        i, j = self.get_current_cell()
        i, j = j, i
        x, y = player_position
        x, y = y, x
        return astar(grid, (i, j), (x, y))

    def get_current_cell(self):
        return int(self.pos.x / 20) % 19, int(self.pos.y / 20) % 22

    def move(self, y, x, speed, width):
        target = pygame.math.Vector2(x*20+10, y*20+10)
        direction = pygame.math.Vector2(self.pos - target).normalize()

        if direction == [1, 0]:
            self.vel.x = -speed
            self.vel.y = 0
        if direction == [-1, 0]:
            self.vel.x = speed
            self.vel.y = 0
        if direction == [0, 1]:
            self.vel.y = -speed
            self.vel.x = 0
        if direction == [0, -1]:
            self.vel.y = speed
            self.vel.x = 0

        self.pos += self.vel

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
        self.rect.midbottom = self.pos + pygame.math.Vector2(0, 10)
