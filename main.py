import pygame
from pygame.locals import *
import sys
import copy
from cell import Cell
from player import Player
from grid import Grid
from enemy import Enemy
from field import Field

# Based on: https://coderslegacy.com/python/pygame-platformer-game-development/

pygame.init()

HEIGHT = 440  # 22 * 20
WIDTH = 380  # 19 * 20
SPEED = 1  # 2
FPS = 60

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


def init_map(grid):
    cells = []
    for j in range(22):
        grid_row = []
        for i in range(19):
            if grid.walls[j][i]:
                grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 255)))
            else:
                grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 0)))
        cells.append(grid_row)

    return cells


def close_game_when_exiting():
    # Close game upon exiting the window
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def draw_game(all_sprites):
    # Initialise black background
    display_surface.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)


def highlight_player_cell(player, cells, previous_cell, grid):
    # Highlight the current grid cell of the player
    i, j = player.get_current_cell()
    # cells[j][i].surf.fill((255, 0, 0))

    if not (j == previous_cell[0] and i == previous_cell[1]):
        cells[previous_cell[0]][previous_cell[1]].surf.fill(previous_cell[2])
        col = (0, 0, 255) if grid.is_wall(j, i) else (0, 0, 0)
        previous_cell = (j, i, col)

    return i, j, previous_cell, cells


def move_player(player, next_move, old_direction, grid, i, j, cells, old_field):
    # Player movement
    pressed_key = pygame.key.get_pressed()
    next_move, new_direction = player.set_direction(pressed_key, next_move, old_direction)

    # Highlight the next cell for which the player is headed
    x_new, y_new = grid.get_next_cell((i, j), player.get_direction())
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
        if ((player.get_direction() % 2 == 0
             and player.pos.x % 10 == 0
             and (player.pos.x / 10) % 2 == 1)
                or (player.get_direction() % 2 == 1
                    and (player.pos.y - 5) % 10 == 0
                    and ((player.pos.y - 5) / 10) % 2 == 0)):
            player.move(new_direction, SPEED, WIDTH)
            old_direction = new_direction
            next_move = False
        else:
            player.move(old_direction, SPEED, WIDTH)
    elif next_move and grid.is_wall(y_new, x_new):  # Keep direction
        if grid.is_wall(y_old, x_old):
            if old_direction % 2 == 1 and player.pos.x % 10 == 0 and (player.pos.x / 10) % 2 == 1:
                player.stop()
            elif old_direction % 2 == 0 and (player.pos.y - 5) % 10 == 0 and (
                    (player.pos.y - 5) / 10) % 2 == 0:
                player.stop()
            else:
                player.move(old_direction, SPEED, WIDTH)
        else:
            player.move(old_direction, SPEED, WIDTH)
    elif grid.is_wall(y_new, x_new):  # Stop the player before hitting a wall
        if player.get_direction() % 2 == 1 and player.pos.x % 10 == 0 and (player.pos.x / 10) % 2 == 1:
            player.stop()
        elif player.get_direction() % 2 == 0 and (player.pos.y - 5) % 10 == 0 and (
                (player.pos.y - 5) / 10) % 2 == 0:
            player.stop()
        else:
            player.move(old_direction, SPEED, WIDTH)
    else:
        player.move(old_direction, SPEED, WIDTH)

    # if pygame.sprite.spritecollideany(player, all_sprites):
    #     player.stop()
    return next_move, old_direction, new_direction, new_field


def move_enemy(blinky, old_path, cells, grid, player):
    surface = pygame.Surface((5, 5))
    surface.fill((0, 0, 0))

    # Update enemy target
    for pos_y, pos_x in old_path:  # Clear old path
        cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

    new_path = blinky.get_path(grid.walls, player.get_current_cell())  # Get new path
    surface.fill((200, 50, 50))
    for pos_y, pos_x in new_path:  # Highlight new path
        cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

    old_path = new_path  # Update path
    blinky.move(*new_path[1], SPEED / 3, WIDTH)

    return old_path


def move_pinky(pinky, old_path, cells, grid, player):
    surface = pygame.Surface((5, 5))
    surface.fill((0, 0, 0))
    for pos_y, pos_x in old_path:  # Clear old path
        cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

    cell = grid.get_cell_in_front(*player.get_current_cell(), player.get_direction(), 2)
    x, y = cell
    cells[y][x].surf.fill((255, 105, 180))
    # Todo: Fix pinky path (near portal), Combine pinky and blinky move functions (redundant code atm)

    maze = copy.deepcopy(grid.walls)
    player_pos_x, player_pos_y = player.get_current_cell()
    if (x, y) != (player_pos_x, player_pos_y):
        maze[player_pos_y][player_pos_x] = 1

    new_path = pinky.get_path(maze, cell)  # Get new path
    surface.fill((255, 105, 180))
    for pos_y, pos_x in new_path:  # Highlight new path
        cells[pos_y][pos_x].surf.blit(surface, (7.5, 7.5))

    # y, x = new_path[-1]
    # cells[y][x].surf.fill((255, 105, 180))

    old_path = new_path  # Update path
    pinky.move(*new_path[1], SPEED / 3, WIDTH)

    return old_path


def run():
    # Initialise Map
    grid = Grid()
    cells = init_map(grid)

    # Create a player
    player = Player()

    # Create ghost(s)
    blinky = Enemy(9 * 20 + 10, 8 * 20 + 10, (255, 0, 0))
    pinky = Enemy(1 * 20 + 10, 1 * 20 + 10, (255, 105, 180))

    # Create a sprite group
    all_sprites = pygame.sprite.Group()
    for row in cells:
        all_sprites.add(row)
    all_sprites.add(player)
    all_sprites.add(blinky)
    all_sprites.add(pinky)

    previous_cell = (16, 9, (0, 0, 0))
    next_move = False
    old_direction = -1
    old_field = Field(-1, -1, (0, 0, 255))
    old_path = []
    old_path2 = []

    # Main Game Loop
    while True:
        close_game_when_exiting()
        draw_game(all_sprites)
        i, j, previous_cell, cells = highlight_player_cell(player, cells, previous_cell, grid)
        next_move, old_direction, new_direction, old_field = move_player(player, next_move, old_direction, grid, i, j,
                                                                         cells, old_field)
        old_path = move_enemy(blinky, old_path, cells, grid, player)

        old_path2 = move_pinky(pinky, old_path2, cells, grid, player)

        # Game updates
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    run()
