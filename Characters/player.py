import pygame
from pygame.locals import *
from Level.field import Field


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 0), (30 // 2, 30 // 2), 7)
        self.rect = self.surf.get_rect()

        self.pos = pygame.math.Vector2((190, 345))
        self.vel = pygame.math.Vector2(0, 0)
        self.dir = -1

    def move(self, direction, speed, width):
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

    def stop(self):
        self.vel = pygame.math.Vector2(0, 0)

    def get_current_cell(self):
        return int(self.pos.x / 20) % 19, int((self.pos.y - 15) / 20) % 22

    def set_direction(self, pressed_keys, next_move, old_direction):
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
        else:
            return False | next_move, old_direction

    def get_direction(self):
        return self.dir

    def highlight_player_cell(self, cells, previous_cell, grid):
        # Highlight the current grid cell of the player
        i, j = self.get_current_cell()
        # cells[j][i].surf.fill((255, 0, 0))

        if not (j == previous_cell[0] and i == previous_cell[1]):
            cells[previous_cell[0]][previous_cell[1]].surf.fill(previous_cell[2])
            col = (0, 0, 255) if grid.is_wall(j, i) else (0, 0, 0)
            previous_cell = (j, i, col)

        return i, j, previous_cell, cells

    def move_player(self, next_move, old_direction, grid, i, j, cells, old_field, speed, width):
        # Player movement
        pressed_key = pygame.key.get_pressed()
        next_move, new_direction = self.set_direction(pressed_key, next_move, old_direction)

        # Highlight the next cell for which the player is headed
        x_new, y_new = grid.get_next_cell((i, j), self.get_direction())
        colour = (0, 0, 255) if grid.is_wall(y_new, x_new) else (0, 0, 0)
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
        if next_move and not grid.is_wall(y_new, x_new):  # Change direction
            if ((self.get_direction() % 2 == 0
                 and self.pos.x % 10 == 0
                 and (self.pos.x / 10) % 2 == 1)
                    or (self.get_direction() % 2 == 1
                        and (self.pos.y - 5) % 10 == 0
                        and ((self.pos.y - 5) / 10) % 2 == 0)):
                self.move(new_direction, speed, width)
                old_direction = new_direction
                next_move = False
            else:
                self.move(old_direction, speed, width)
        elif next_move and grid.is_wall(y_new, x_new):  # Keep direction
            if grid.is_wall(y_old, x_old):
                if old_direction % 2 == 1 and self.pos.x % 10 == 0 and (self.pos.x / 10) % 2 == 1:
                    self.stop()
                elif old_direction % 2 == 0 and (self.pos.y - 5) % 10 == 0 and (
                        (self.pos.y - 5) / 10) % 2 == 0:
                    self.stop()
                else:
                    self.move(old_direction, speed, width)
            else:
                self.move(old_direction, speed, width)
        elif grid.is_wall(y_new, x_new):  # Stop the player before hitting a wall
            if self.get_direction() % 2 == 1 and self.pos.x % 10 == 0 and (self.pos.x / 10) % 2 == 1:
                self.stop()
            elif self.get_direction() % 2 == 0 and (self.pos.y - 5) % 10 == 0 and (
                    (self.pos.y - 5) / 10) % 2 == 0:
                self.stop()
            else:
                self.move(old_direction, speed, width)
        else:
            self.move(old_direction, speed, width)

        # if pygame.sprite.spritecollideany(player, all_sprites):
        #     player.stop()
        return next_move, old_direction, new_direction, new_field
