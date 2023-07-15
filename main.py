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


def blur_surface(surface, amount):
    if amount < 1:
        raise ValueError("")

    scale = 1.0/float(amount)
    surface_size = surface.get_size()
    scale_size = (int(surface_size[0] * scale), int(surface_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surface_size)
    return surf


def paused():
    # Darken pause background
    s = pygame.Surface((WIDTH, HEIGHT))  # the size of your rect
    s.set_alpha(50)  # alpha level
    s.fill((50, 50, 50))  # this fills the entire surface
    display_surface.blit(s, (0, 0))

    # Print pause text
    font = pygame.font.SysFont("arial", 50)
    text = font.render('Pause', True, (222, 222, 222))
    # text.set_alpha(200)
    text_rect = text.get_rect()
    text_rect.center = ((display_surface.get_width() / 2), (display_surface.get_height() / 2))
    display_surface.blit(text, text_rect)

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False

        # button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        # button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        FramePerSec.tick(15)


def draw_surface(surfaces):
    for surf in surfaces:
        display_surface.blit(surf.surf, surf.rect)


def run():
    # Initialise Map
    grid = Grid()
    cells = grid.init_map()
    dots = grid.init_dots()

    # Create a player
    player = Player()

    # Create ghost(s)
    blinky = Enemy(9 * 20 + 10, 8 * 20 + 10, (255, 0, 0))
    pinky = Enemy(1 * 20 + 10, 1 * 20 + 10, (255, 105, 180))
    inky = Enemy(14 * 20 + 10, 15 * 20 + 10, (0, 255, 255))

    # Create a sprite group
    cell_sprites = pygame.sprite.Group()
    for row in cells:
        cell_sprites.add(row)

    character_sprites = pygame.sprite.Group()
    character_sprites.add([player, blinky, pinky, inky])

    # Initialise variables
    previous_cell = (16, 9, (0, 0, 0))
    next_move = False
    old_direction = -1
    old_field = Field(-1, -1, (0, 0, 255))
    blinky_path, pinky_path, inky_path = [], [], []

    # Main Game Loop
    while True:
        for event in pygame.event.get():
            # Close game upon exiting the window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pause game
                    display_surface.blit(blur_surface(display_surface, 2), (0, 0))
                    paused()

        display_surface.fill((0, 0, 0))  # Initialise black background
        draw_surface(cell_sprites)
        draw_surface(dots)
        draw_surface(character_sprites)

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
