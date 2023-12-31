import math
import sys
import pygame
from Logic.astar import astar
from Level.menu import game_over
import copy


def swap(a, b):
    return b, a


def get_maze(grid_walls, pos):
    ghost_house = [(9, 9), (10, 8), (10, 9), (10, 10)]
    maze = copy.deepcopy(grid_walls)
    # When the ghost is in his home
    if swap(*pos) in ghost_house:
        for room in ghost_house:
            maze[room[0]][room[1]] = 0

    return maze


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name, colour, path=None):
        super().__init__()
        self.name = name
        self.col = colour
        self._is_feared = 0
        if path is None:
            self.path = []
        else:
            self.path = path

        self.surf = pygame.Surface((18, 18))
        self.surf.fill((0, 0, 0))
        pygame.draw.circle(self.surf, colour, (18 // 2, 18 // 2), 9)
        pygame.draw.rect(self.surf, colour, pygame.Rect(0, 9, 18, 9))
        self.rect = self.surf.get_rect(center=(x, y))

        self._home = pygame.math.Vector2((x, y))
        self.pos = pygame.math.Vector2((x, y))
        self.vel = pygame.math.Vector2(0, 0)

        self.score = 0  # Points given to the player for being eaten

    def _reset_position(self):
        x = self._home.x
        y = self._home.y
        self.rect = self.surf.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2((x, y))
        pygame.draw.circle(self.surf, self.col, (18 // 2, 18 // 2), 9)
        pygame.draw.rect(self.surf, self.col, pygame.Rect(0, 9, 18, 9))

    def get_path(self, grid, player_position):
        i, j = swap(*self.get_current_cell())
        x, y = swap(*player_position)
        return astar(grid, (i, j), (x, y))

    def get_current_cell(self):
        return int((self.pos.x - 1) / 20) % 19, int((self.pos.y - 1) / 20) % 22

    def move(self, y, x, speed, width):
        target = pygame.math.Vector2(x * 20 + 10, y * 20 + 10)
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

    def move_enemy(self, cells, grid, player, params, enemy="blinky", highlight_path=True, position=None):
        surface = pygame.Surface((5, 5))
        surface.fill((0, 0, 0))
        color = (0, 0, 0)
        thickness = 1
        if self._is_feared == 0 and enemy == "feared":
            self._is_feared = 1
        elif enemy != "feared":
            self._is_feared = 0
            pygame.draw.circle(self.surf, self.col, (18 // 2, 18 // 2), 9)
            pygame.draw.rect(self.surf, self.col, pygame.Rect(0, 9, 18, 9))

        # Update enemy target
        for pos_y, pos_x in self.path:  # Clear old path
            pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 6), (6, 15), thickness)
            pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 15), (15, 15), thickness)
            pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 6), (15, 6), thickness)
            pygame.draw.line(cells[pos_y][pos_x].surf, color, (15, 6), (15, 15), thickness)

        match enemy:
            case "inky":
                target = player.pos - position + player.pos
                target.y = target.y - 2 * 15  # correction due to player offset

                possible_targets = []
                level = 1
                target_i = min(21, max(0, int((target.y - 10) / 20)))
                target_j = min(18, max(0, int((target.x - 10) / 20)))
                while not possible_targets:
                    possible_targets = grid.get_adjacent_cells(target_j, target_i, n=level, is_not_wall=True)
                    level += 1

                min_distance = (-1, math.inf)
                for index, cell in enumerate(possible_targets):
                    distance = pygame.math.Vector2(cell[0] * 20 + 10, cell[1] * 20 + 10).distance_to(self.pos)
                    if distance < min_distance[1]:
                        min_distance = (index, distance)

                # print(f"{possible_targets} - {min_distance} - {target}")
                maze = get_maze(grid.walls, self.get_current_cell())
                path = self.get_path(maze, possible_targets[min_distance[0]])  # Get new path
                color = (0, 255, 255)

            case "pinky":
                cell = grid.get_cell_in_front(*player.get_current_cell(), player.get_direction(), 2)
                x, y = cell
                # cells[y][x].surf.fill((255, 105, 180))

                maze = get_maze(grid.walls, self.get_current_cell())
                player_pos_x, player_pos_y = player.get_current_cell()
                if (x, y) != (player_pos_x, player_pos_y):
                    maze[player_pos_y][player_pos_x] = 1

                path = self.get_path(maze, cell)  # Get new path
                color = (255, 105, 180)

            case "blinky":
                maze = get_maze(grid.walls, self.get_current_cell())
                path = self.get_path(maze, player.get_current_cell())  # Get new path
                color = (200, 50, 50)

            case "feared":
                if self.pos != self._home:
                    colour = (0, 127, 255) if int(pygame.time.get_ticks() / 400) % 2 == 0 else (255, 255, 255)
                    pygame.draw.circle(self.surf, colour, (18 // 2, 18 // 2), 9)
                    pygame.draw.rect(self.surf, colour, pygame.Rect(0, 9, 18, 9))

                if self._is_feared == 3:
                    return  # wait for fear timer to be over
                elif self._is_feared < 2 or swap(*self.get_current_cell()) == self.path[-1]:
                    self._is_feared = 2
                    # Get new path to a random position
                    random_pos = grid.get_random_position()
                    maze = get_maze(grid.walls, self.get_current_cell())
                    path = self.get_path(maze, swap(*random_pos))
                    # print(f"Got a new path to a random position. {random_pos} -> {path}")
                elif self.path:
                    maze = get_maze(grid.walls, self.get_current_cell())
                    new_path = self.get_path(maze, swap(*self.path[-1]))
                    if len(new_path) >= len(self.path):
                        path = self.path
                    else:
                        path = new_path
                else:
                    path = []

                color = (127, 127, 127)

            case _:
                sys.exit("Enemy move pattern not found.")

        if highlight_path and path:
            for pos_y, pos_x in path:  # Highlight new path
                pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 6), (6, 15), thickness)
                pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 15), (15, 15), thickness)
                pygame.draw.line(cells[pos_y][pos_x].surf, color, (6, 6), (15, 6), thickness)
                pygame.draw.line(cells[pos_y][pos_x].surf, color, (15, 6), (15, 15), thickness)

        # Collision
        if player.get_current_cell() == self.get_current_cell():
            if enemy == 'feared':
                self._is_feared = 3  # ghost was eaten while being feared
                self._reset_position()  # return to home
                self.score += 3333
                return
            else:
                # DISCLAIMER: This is NOT clean code!
                from main import run
                params['lives'] = params['lives'] - 1
                if params['lives'] == 0:
                    print("GAME OVER!!!")
                    game_over(params['score'])
                else:
                    run(params)

        def tuple_difference(t1, t2, add=False):
            return tuple(map(lambda i, j: i - j if not add else i + j, t1, t2))

        # Do not move the enemy if no path has been found
        if not path:
            return

        speed, width = params['speed'], params['width']
        if len(path) > 1:
            # Make ghosts warp around border
            diff = tuple_difference(path[0], path[1])
            if sum(diff) > 1:
                self.move(*tuple_difference(path[0], diff, True), speed / 3, width)
            elif sum(diff) < -1:
                abs_diff = tuple(abs(d) for d in diff)
                self.move(*tuple_difference(path[0], abs_diff), speed / 3, width)
            # Move ghosts along calculated path
            elif swap(*self.get_current_cell()) == path[0]:
                self.move(*path[1], speed / 3, width)
            else:
                self.move(*path[0], speed / 3, width)
        else:
            self.move(*path[0], speed / 3, width)

        self.path = path
