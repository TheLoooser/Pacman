import pygame
from Logic.astar import astar
import copy


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
        return int((self.pos.x - 1) / 20) % 19, int((self.pos.y - 1) / 20) % 22

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

    def move_enemy(self, path, cells, grid, player, speed, width, pinky=False):
        surface = pygame.Surface((5, 5))
        surface.fill((0, 0, 0))

        # Update enemy target
        for pos_y, pos_x in path:  # Clear old path
            cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

        if pinky:
            cell = grid.get_cell_in_front(*player.get_current_cell(), player.get_direction(), 2)
            x, y = cell
            # cells[y][x].surf.fill((255, 105, 180))

            maze = copy.deepcopy(grid.walls)
            player_pos_x, player_pos_y = player.get_current_cell()
            if (x, y) != (player_pos_x, player_pos_y):
                maze[player_pos_y][player_pos_x] = 1

            path = self.get_path(maze, cell)  # Get new path
            surface.fill((255, 105, 180))
        else:
            path = self.get_path(grid.walls, player.get_current_cell())  # Get new path
            surface.fill((200, 50, 50))

        for pos_y, pos_x in path:  # Highlight new path
            cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

        def tuple_difference(t1, t2, add=False):
            return tuple(map(lambda i, j: i - j if not add else i + j, t1, t2))

        if len(path) > 1:
            diff = tuple_difference(path[0], path[1])
            if sum(diff) > 1:
                self.move(*tuple_difference(path[0], diff, True), speed / 3, width)
            elif sum(diff) < -1:
                abs_diff = tuple(abs(d) for d in diff)
                self.move(*tuple_difference(path[0], abs_diff), speed / 3, width)
            else:
                self.move(*path[1], speed / 3, width)

        return path
