"""
This module contains an implementation of a player object.
"""
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

from Level.cell import Cell
from Level.field import Field
from Level.grid import Grid
from Level.menu import game_over, update_score


class Player(pygame.sprite.Sprite):
    """
    A class to represent a player.
    """

    def __init__(self):
        """
        Constructs a player object.
        """
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 0), (30 // 2, 30 // 2), 7.5)
        pygame.draw.polygon(self.surf, (0, 0, 0), [(0, 7), (0, 20), (15, 14)])
        self.rect = self.surf.get_rect()

        self.pos = pygame.math.Vector2((190, 345))
        self.vel = pygame.math.Vector2(0, 0)
        self.dir = -1

    def move(self, direction: int, speed: float, width: int) -> None:
        """
        Update the player's position.

        :param direction: The moving direction.
        :param speed: The speed of the player.
        :param width: The width of game window.
        :return: Nothing.
        """
        if direction == 3:
            self.vel.x = -speed
            self.vel.y = 0
        if direction == 1:
            self.vel.x = speed
            self.vel.y = 0
        if direction == 0:
            self.vel.y = -speed
            self.vel.x = 0
        if direction == 2:
            self.vel.y = speed
            self.vel.x = 0

        self.pos += self.vel

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
        self.rect.midbottom = self.pos

    def stop(self) -> None:
        """
        Stops the player at its current position.

        :return: Nothing.
        """
        self.vel = pygame.math.Vector2(0, 0)

    def get_current_cell(self) -> tuple[int, int]:
        """
        Gets the players current position in cell coordinates.

        :return: The position.
        """
        return int(self.pos.x / 20) % 19, int((self.pos.y - 15) / 20) % 22

    def set_direction(self, pressed_keys: any, next_move: bool, old_direction: int) -> tuple[bool, int]:
        """
        Sets the players moving direction.

        :param pressed_keys: Sequence of boolean values representing the state of every key on the keyboard.
        :param next_move: Whether a new direction has been requested by the user.
        :param old_direction: The old moving direction of the player.
        :return: A boolean indicating whether a new direction is requested or not and the old moving direction.
        """
        if pressed_keys[K_LEFT]:
            self.dir = 3
        if pressed_keys[K_RIGHT]:
            self.dir = 1
        if pressed_keys[K_UP]:
            self.dir = 0
        if pressed_keys[K_DOWN]:
            self.dir = 2
        if self.dir != old_direction:
            return True, self.dir

        return False | next_move, old_direction

    def get_direction(self) -> int:
        """
        Gets the current moving direction of the player.

        :return: The player's direction.
        """
        return self.dir

    def highlight_player_cell(
        self,
        cells: list[list[Cell]],
        previous_cell: tuple[int, int, tuple[int, int, int]],
        grid: Grid,
    ) -> tuple[int, int, tuple[int, int, tuple[int, int, int]], list[list[Cell]]]:
        """
        Highlight the current grid cell of the player.

        :param cells: The matrix of Cell objects.
        :param previous_cell: Index and colour of the previously highlighted cell.
        :param grid: The grid matrix of the game.
        :return: The current highlighted cell and the cell matrix.
        """
        i, j = self.get_current_cell()
        # cells[j][i].surf.fill((255, 0, 0))

        if not (j == previous_cell[0] and i == previous_cell[1]):
            cells[previous_cell[0]][previous_cell[1]].surf.fill(previous_cell[2])
            col = (0, 0, 255) if grid.is_wall(j, i) else (0, 0, 0)
            previous_cell = (j, i, col)

        return i, j, previous_cell, cells

    def move_player(
        self,
        next_move: bool,
        old_direction: int,
        grid: Grid,
        i: int,
        j: int,
        cells: list[list[Cell]],
        old_field: Field,
        params: dict[str, any],
    ) -> tuple[bool, int, int, Field, bool]:
        """
        Move the player.

        :param next_move: Whether an input for a new direction has been pressed or not.
        :param old_direction: The player's current moving direction.
        :param grid: The grid matrix of the game.
        :param i: The vertical index.
        :param j: The horizontal index.
        :param cells: The matrix of Cell objects.
        :param old_field: The previous field object.
        :param params: Various game parameters.
        :return: Updated player movement variables.
        """
        # Player movement
        pressed_key = pygame.key.get_pressed()
        next_move, new_direction = self.set_direction(pressed_key, next_move, old_direction)

        # Highlight the next cell for which the player is headed
        x_new, y_new = grid.get_next_cell((i, j), self.get_direction())
        colour = (0, 0, 255) if (grid.is_wall(y_new, x_new) and (y_new, x_new) != (9, 9)) else (0, 0, 0)
        new_field = Field(x_new, y_new, colour)

        cells[y_new][x_new].surf.fill((0, 255, 0))
        surface = pygame.Surface((17, 17))
        surface.fill(colour)
        cells[y_new][x_new].surf.blit(surface, (1, 1))

        # Overwrite the last highlighted cell (remove highlighted border)
        if new_field.coordinates != old_field.coordinates:
            x, y = old_field.coordinates
            cells[y][x].surf.fill(old_field.colour)

        x_old, y_old = grid.get_next_cell((i, j), old_direction)  # keep the old direction

        # Movement
        speed, width = params["speed"], params["width"]
        position = [int(self.pos.x), int(self.pos.y)]
        if next_move and not grid.is_wall(y_new, x_new):  # Change direction
            if (self.get_direction() % 2 == 0 and position[0] % 10 == 0 and (position[0] / 10) % 2 == 1) or (
                self.get_direction() % 2 == 1 and (position[1] - 5) % 10 == 0 and ((position[1] - 5) / 10) % 2 == 0
            ):
                self.move(new_direction, speed, width)

                # Rotate player sprite
                dir_change = new_direction - old_direction
                angle = (90 * dir_change) if dir_change % 2 == 0 else (90 * dir_change) + 180
                self.surf = pygame.transform.rotate(self.surf, angle)

                old_direction = new_direction
                next_move = False
            else:
                self.move(old_direction, speed, width)
        elif next_move and grid.is_wall(y_new, x_new):  # Keep direction
            if grid.is_wall(y_old, x_old):
                if old_direction % 2 == 1 and position[0] % 10 == 0 and (position[0] / 10) % 2 == 1:
                    self.stop()
                elif old_direction % 2 == 0 and (position[1] - 5) % 10 == 0 and ((position[1] - 5) / 10) % 2 == 0:
                    self.stop()
                else:
                    self.move(old_direction, speed, width)
            else:
                self.move(old_direction, speed, width)
        elif grid.is_wall(y_new, x_new):  # Stop the player before hitting a wall
            if self.get_direction() % 2 == 1 and position[0] % 10 == 0 and (position[0] / 10) % 2 == 1:
                self.stop()
            elif self.get_direction() % 2 == 0 and (position[1] - 5) % 10 == 0 and ((position[1] - 5) / 10) % 2 == 0:
                self.stop()
            else:
                self.move(old_direction, speed, width)
        else:
            self.move(old_direction, speed, width)

        # Eat dot
        fear_state = False
        if self.get_current_cell() in params["dots"]:
            dot = params["dots"].pop(self.get_current_cell(), None)
            if dot.is_pellet:
                fear_state = True

        # Game over when all dots are eaten
        if not params["dots"]:
            game_over(update_score(params["score"], params["timer"]))

        # if pygame.sprite.spritecollideany(player, all_sprites):
        #     player.stop()
        return next_move, old_direction, new_direction, new_field, fear_state
