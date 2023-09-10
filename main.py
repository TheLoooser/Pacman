# Built-in
import sys
import numpy as np

# Pygame
import pygame
import pygame_menu
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, WINDOWCLOSE

# Modules
from Characters.player import Player
from Characters.enemy import Enemy
from Level.grid import Grid
from Level.field import Field
from Level.menu import draw_hud, draw_surface, blur_surface, paused
from Level.window import create_window, change_surface
from Logic import timer

# Based on: https://coderslegacy.com/python/pygame-platformer-game-development/

pygame.init()

HEIGHT = 440  # 22 * 20
WIDTH = 380  # 19 * 20
SPEED = 1  # 2
FPS = 60

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT + 1.5 * 20))
pygame.display.set_caption("Pacman")


def get_move_pattern(enemy, is_feared):
    return enemy if not is_feared else "feared"


def run():
    # Initialise Map
    grid = Grid()
    cells = grid.init_map()
    pellets = [(1, 3), (17, 3), (1, 16), (17, 16)]
    dots = grid.init_dots(pellets)
    max_points = (len(dots) - 1) * 100

    # Matrix
    base_matrix = np.array(Grid().walls)
    old_matrix = np.copy(base_matrix)

    # Create a player
    player = Player()

    # Create ghost(s)
    blinky = Enemy(9 * 20 + 10, 8 * 20 + 10, "blinky", (255, 0, 0))
    pinky = Enemy(1 * 20 + 10, 1 * 20 + 10, "pinky", (255, 105, 180))
    inky = Enemy(14 * 20 + 10, 15 * 20 + 10, "inky", (0, 255, 255))

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
    fear_duration = 5  # sec
    fear_timer = timer.Timer()
    checkboxes = {"path_highlights": True}

    # Initialise variables for the second window
    window, renderer = -1, -1  # window will be created later
    toggle = False

    # Main Game Loop
    while True:
        # Exit upon pressing ALT + F4
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LALT] and keys[pygame.K_F4]:
            pygame.quit()
            sys.exit(0)

        for event in pygame.event.get():
            # Close game upon exiting the window
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif getattr(event, "window", None) == window:
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == WINDOWCLOSE:
                    toggle = not toggle
                    window.destroy()
                # Close 2nd window if it is in focus and toggle key is pressed
                if event.type == KEYDOWN and toggle and event.key == pygame.K_t:
                    toggle = not toggle
                    window.destroy()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pause game
                    display_surface.blit(blur_surface(display_surface, 2), (0, 0))
                    if fear_timer.is_running():
                        fear_timer.pause()
                        checkboxes = paused(display_surface, FramePerSec, WIDTH, HEIGHT, checkboxes)
                        fear_timer.resume()
                    else:
                        checkboxes = paused(display_surface, FramePerSec, WIDTH, HEIGHT, checkboxes)
                        print(f"IN MAIN -> {checkboxes['path_highlights']}")
                # Close 2nd window if main window is currently in focus
                elif event.key == pygame.K_t:
                    if toggle:
                        window.destroy()
                    else:
                        window, renderer = create_window(matrix)
                    toggle = not toggle
            elif event.type == WINDOWCLOSE:
                pygame.quit()
                sys.exit(0)

        # Draw surfaces
        display_surface.fill((0, 0, 0))  # Initialise black background
        draw_hud(display_surface, 3, max_points - len(dots) * 100)
        draw_surface(display_surface, cell_sprites)
        draw_surface(display_surface, dots.values())
        draw_surface(display_surface, character_sprites)

        # Move player and ghosts
        i, j, previous_cell, cells = player.highlight_player_cell(cells, previous_cell, grid)
        next_move, old_direction, new_direction, old_field, dots, fear_state = \
            player.move_player(next_move, old_direction, grid, i, j, cells, old_field, dots, SPEED, WIDTH)

        # Fear timer
        if fear_state:
            fear_timer.start()

        if fear_timer.get_elapsed_time() > fear_duration:
            print("fear_over")
            fear_timer.stop()
        if fear_timer.is_running():
            fear_state = True

        # Todo: Gradually increase enemy speed over time
        blinky.move_enemy(cells, grid, player, SPEED, WIDTH, get_move_pattern("blinky", fear_state),
                          checkboxes['path_highlights'])

        # Todo: Investigate no path found bug when player is somewhere in lower half
        pinky.move_enemy(cells, grid, player, SPEED, WIDTH, get_move_pattern("pinky", fear_state),
                         checkboxes['path_highlights'])

        # Todo: Investigate inky getting stuck in tunnel
        inky.move_enemy(cells, grid, player, SPEED, WIDTH, get_move_pattern("inky", fear_state),
                        checkboxes['path_highlights'], blinky.pos)

        # Update second window
        base_matrix = np.array(Grid().walls)
        for key in dots:
            base_matrix[key[1]][key[0]] = 2
        player_pos_x, player_pos_y = player.get_current_cell()
        matrix = np.copy(base_matrix)
        matrix[player_pos_y][player_pos_x] = 99
        if toggle:
            if not np.array_equal(old_matrix, matrix):
                old_matrix = np.copy(matrix)
                change_surface(window.size, renderer, matrix)

        # Game updates
        pygame.display.update()
        FramePerSec.tick(FPS)

        # FPS
        pygame.display.set_caption(f"Pacman (FPS: {FramePerSec.get_fps():.1f})")


def get_theme():
    my_theme = pygame_menu.themes.THEME_DARK
    my_theme.widget_font = pygame_menu.font.FONT_8BIT
    my_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    return my_theme


def main_menu():
    # Main menu
    my_menu = pygame_menu.Menu('', WIDTH, HEIGHT, theme=get_theme())
    my_menu.add.label('Pacman', font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 100))
    my_menu.add.button('Play', run)
    my_menu.add.button('Credits', credits_menu)
    my_menu.add.button('Quit', pygame_menu.events.EXIT)
    my_menu.mainloop(display_surface)


def credits_menu():
    my_credits = pygame_menu.Menu('', WIDTH, HEIGHT, theme=get_theme())
    my_credits.add.label('Credits', font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 20))
    my_credits.add.label('Creator\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(0, 0))
    my_credits.add.label('Co-Creator\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-15, 0))
    my_credits.add.label('Director\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-5, 0))
    my_credits.add.label('Programmer\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-25, 0))
    my_credits.add.label('Artist\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(8, 0))
    my_credits.add.label('Writer\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(5, 0))
    my_credits.add.label('Designer\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-5, 0))
    my_credits.add.label('Playtester\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-20, 0))
    my_credits.add.label('Producer\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-8, 0))
    my_credits.add.label('Special Thanks\t Dizzy', font_size=12, font_color=(200, 200, 200), margin=(-38, 30))
    my_credits.add.button('Back', main_menu)
    my_credits.mainloop(display_surface)


if __name__ == "__main__":
    # run()

    main_menu()

    # TODO: Second Window with Matrix (coloured numbers)
    #       Align pause menu buttons
    #       Improve point system (e.g. time based)
    #       Add fear behaviour of ghosts
    #       Ghosts start from center of the map (ie their home)
    #       Add collision (ie ghosts kill pacman)
    #       Remove lives upon death
    #       Game over screen when running out of lives 
    #         (similar to pause, show score, go back to main menu, reset game variables, e.g. score and dots)
