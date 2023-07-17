import pygame_menu

from Characters.player import Player
from Level.grid import Grid
from Characters.enemy import Enemy
from Level.field import Field
from Level.menu import *

# Based on: https://coderslegacy.com/python/pygame-platformer-game-development/

pygame.init()

HEIGHT = 440  # 22 * 20
WIDTH = 380  # 19 * 20
SPEED = 1  # 2
FPS = 60

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT + 1.5 * 20))
pygame.display.set_caption("Game")


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
                    paused(display_surface, FramePerSec, WIDTH, HEIGHT)

        # Draw surfaces
        display_surface.fill((0, 0, 0))  # Initialise black background
        draw_hud(display_surface, 3, 174859)
        draw_surface(display_surface, cell_sprites)
        draw_surface(display_surface, dots.values())
        draw_surface(display_surface, character_sprites)

        # Move player and ghosts
        i, j, previous_cell, cells = player.highlight_player_cell(cells, previous_cell, grid)
        next_move, old_direction, new_direction, old_field, dots = player.move_player(next_move, old_direction, grid, i,
                                                                                      j, cells, old_field, dots, SPEED,
                                                                                      WIDTH)

        # Todo: Gradually increase enemy speed over time
        blinky_path = blinky.move_enemy(blinky_path, cells, grid, player, SPEED, WIDTH, "blinky")

        # Todo: Investigate no path found bug when player is somewhere in lower half
        pinky_path = pinky.move_enemy(pinky_path, cells, grid, player, SPEED, WIDTH, "pinky")

        # Todo: Investigate inky getting stuck in tunnel
        inky_path = inky.move_enemy(inky_path, cells, grid, player, SPEED, WIDTH, "inky", blinky.pos)

        # Game updates
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    # run()

    # Main menu
    my_theme = pygame_menu.themes.THEME_DARK
    my_theme.widget_font = pygame_menu.font.FONT_8BIT
    my_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

    menu = pygame_menu.Menu('', WIDTH, HEIGHT, theme=my_theme)
    menu.add.label('Pacman', font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 100))
    menu.add.button('Play', run)
    menu.add.button('Credits')
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(display_surface)
