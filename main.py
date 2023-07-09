import pygame
from pygame.locals import *
import sys

from Characters.player import Player
from Level.grid import Grid
from Characters.enemy import Enemy
from Level.field import Field

# Based on: https://coderslegacy.com/python/pygame-platformer-game-development/

pygame.init()

HEIGHT = 440  # 22 * 20
WIDTH = 380  # 19 * 20
SPEED = 1  # 2
FPS = 60

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


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


def run():
    # Initialise Map
    grid = Grid()
    cells = grid.init_map()

    # Create a player
    player = Player()

    # Create ghost(s)
    blinky = Enemy(9 * 20 + 10, 8 * 20 + 10, (255, 0, 0))
    pinky = Enemy(1 * 20 + 10, 1 * 20 + 10, (255, 105, 180))
    inky = Enemy(14 * 20 + 10, 15 * 20 + 10, (0, 255, 255))

    # Create a sprite group
    all_sprites = pygame.sprite.Group()
    for row in cells:
        all_sprites.add(row)
    all_sprites.add(player)
    all_sprites.add(blinky)
    all_sprites.add(pinky)
    all_sprites.add(inky)

    # Initialise variables
    previous_cell = (16, 9, (0, 0, 0))
    next_move = False
    old_direction = -1
    old_field = Field(-1, -1, (0, 0, 255))
    blinky_path, pinky_path, inky_path = [], [], []

    # Main Game Loop
    while True:
        close_game_when_exiting()
        draw_game(all_sprites)
        i, j, previous_cell, cells = player.highlight_player_cell(cells, previous_cell, grid)
        next_move, old_direction, new_direction, old_field = player.move_player(next_move, old_direction, grid, i, j,
                                                                                cells, old_field, SPEED, WIDTH)
        blinky_path = blinky.move_enemy(blinky_path, cells, grid, player, SPEED, WIDTH, "blinky")

        # Todo: Investigate no path found bug when player is somewhere in lower half
        pinky_path = pinky.move_enemy(pinky_path, cells, grid, player, SPEED, WIDTH, "pinky")

        # Todo: Investigate inky getting stuck in tunnel
        inky_path = inky.move_enemy(inky_path, cells, grid, player, SPEED, WIDTH, "inky", blinky.pos)

        # Game updates
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    run()
