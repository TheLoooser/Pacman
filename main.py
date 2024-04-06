"""
This script is the main entry point to the game.
"""

# Built-in
import random
import sys
from collections import defaultdict
from typing import Any, cast

# Packages
import numpy as np

import yaml  # isort: split

# Pygame
import pygame
import pygame_menu
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, WINDOWCLOSE
from pygame_menu.locals import ALIGN_LEFT, ALIGN_RIGHT

# Modules
from characters.enemy import Enemy
from characters.player import Player
from level.field import Field
from level.grid import Grid
from level.menu import blur_surface, draw_hud, draw_surface, paused
from level.window import change_surface, create_window
from logic import timer

# Based on: https://coderslegacy.com/python/pygame-platformer-game-development/

pygame.init()

HEIGHT = 440  # 22 * 20
WIDTH = 380  # 19 * 20
SPEED = 2  # The game breaks if the speed is not an integer.
FPS = 60

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT + 1.5 * 20))
pygame.display.set_caption("Pacman")


def get_move_pattern(enemy: str, is_feared: bool) -> str:
    """
    Returns the string name of the enemy if the enemy is not feared. Otherwise, 'feared' will be returned

    :param enemy: The name of the enemy.
    :param is_feared: Whether the enemy is currently feared or not.
    :return: The name of the enemy or 'feared'.
    """
    return enemy if not is_feared else "feared"


def run(params: dict = {}) -> None:
    """
    The main game loop

    :param params: A dictionary of game parameters
    :return: Nothing
    """

    if not params:
        # Initialise parameters
        params = {
            "width": 380,
            "height": 440,
            "speed": SPEED,
            "lives": 3,
            "score": 0,
            "timer": -1,
            # 'display': display_surface, 'clock': FramePerSec,
            # Initialise variables for the second window
            "window": -1,
            "renderer": -1,
            "toggle": False,  # window will be created later
        }

    # Initialise Map
    grid = Grid()
    cells = grid.init_map()
    pellets = [(1, 3), (17, 3), (1, 16), (17, 16)]
    if "dots" not in params.keys():
        params["dots"] = grid.init_dots(pellets)
        params["max_points"] = (len(params["dots"]) - 1) * 100

    # Matrix
    base_matrix = np.array(Grid().walls)
    old_matrix = np.copy(base_matrix)

    # Create a player
    player = Player()

    # Create ghost(s)
    blinky = Enemy(9 * 20 + 10, 9 * 20 + 10, "blinky", (255, 0, 0))
    pinky = Enemy(9 * 20 + 10, 10 * 20 + 10, "pinky", (255, 105, 180))
    inky = Enemy(8 * 20 + 10, 10 * 20 + 10, "inky", (0, 255, 255))
    clyde = Enemy(10 * 20 + 10, 10 * 20 + 10, "clyde", (250, 185, 85))
    enemies = {"blinky": blinky, "pinky": pinky, "inky": inky, "clyde": clyde}

    # Create a sprite group
    cell_sprites = pygame.sprite.Group()  # type: pygame.sprite.Group
    for row in cells:
        cell_sprites.add(row)

    character_sprites = pygame.sprite.Group()  # type: pygame.sprite.Group
    character_sprites.add([player, blinky, pinky, inky, clyde])

    # Ghost house door
    door = {}  # type: dict
    door_surface = pygame.Surface((20, 3))
    door_surface.fill((255, 165, 0))
    door["surface"] = door_surface
    door["rectangle"] = door_surface.get_rect(center=(9 * 20 + 11, 9 * 20 + 2))

    # Initialise variables
    previous_cell = (16, 9, (0, 0, 0))
    next_move = False
    direction = -1
    old_field = Field(-1, -1, (0, 0, 255))
    matrix = np.empty(0)
    fear_duration = 5  # sec
    fear_timer = timer.Timer()
    release_times = dict(zip(["blinky", "pinky", "inky", "clyde"], sorted(random.sample(range(0, 10), 4))))
    release_timer = timer.Timer()
    release_timer.start()
    if params["timer"] == -1:
        params["timer"] = timer.Timer()
        params["timer"].start()
    checkboxes = {"path_highlights": False}

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
            elif getattr(event, "window", None) == params["window"]:
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == WINDOWCLOSE:
                    params["toggle"] = not params["toggle"]
                    params["window"].destroy()
                # Close 2nd window if it is in focus and toggle key is pressed
                if event.type == KEYDOWN and params["toggle"] and event.key == pygame.K_t:
                    params["toggle"] = not params["toggle"]
                    params["window"].destroy()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pause game
                    display_surface.blit(blur_surface(display_surface, 2), (0, 0))
                    params["timer"].pause()
                    release_timer.pause()
                    if fear_timer.is_running():
                        fear_timer.pause()
                        checkboxes = paused(display_surface, FramePerSec, WIDTH, HEIGHT, checkboxes)
                        fear_timer.resume()
                    else:
                        checkboxes = paused(display_surface, FramePerSec, WIDTH, HEIGHT, checkboxes)
                    params["timer"].resume()
                    release_timer.resume()
                # Close 2nd window if main window is currently in focus
                elif event.key == pygame.K_t:
                    if params["toggle"]:
                        params["window"].destroy()
                    else:
                        params["window"], params["renderer"] = create_window(matrix)  # type: ignore
                    params["toggle"] = not params["toggle"]
            elif event.type == WINDOWCLOSE:
                pygame.quit()
                sys.exit(0)

        # Draw surfaces
        display_surface.fill((0, 0, 0))  # Initialise black background
        draw_hud(display_surface, params["lives"], params["score"])
        draw_surface(display_surface, cell_sprites)
        draw_surface(display_surface, params["dots"].values())
        draw_surface(display_surface, character_sprites)
        display_surface.blit(door["surface"], door["rectangle"])

        # Move player and ghosts
        i, j, previous_cell, cells = player.highlight_player_cell(cells, previous_cell, grid)
        next_move, direction, old_field, fear_state = player.move_player(
            next_move, direction, grid, i, j, cells, old_field, params
        )

        # Fear timer
        if fear_state:
            fear_timer.start()

        if fear_timer.get_elapsed_time() > fear_duration:
            fear_timer.stop()
        if fear_timer.is_running():
            fear_state = True

        for enemy_name, enemy in enemies.items():
            if release_timer.get_elapsed_time() > release_times[enemy_name]:
                position = blinky.pos if enemy_name == "inky" else None
                enemy.move_enemy(
                    cells,
                    grid,
                    player,
                    params,
                    get_move_pattern(enemy_name, fear_state),
                    checkboxes["path_highlights"],
                    cast(tuple[int, int], position),
                )

        # Todo: Gradually increase enemy speed over time
        #       Investigate no path found bug when player is somewhere in lower half
        #       Investigate inky getting stuck in tunnel

        # Update score
        params["score"] = (
            params["max_points"] - len(params["dots"]) * 100 + blinky.score + inky.score + pinky.score + clyde.score
        )

        # Update second window
        base_matrix = np.array(Grid().walls)
        for key in params["dots"]:
            base_matrix[key[1]][key[0]] = 3 if key in pellets else 2
        player_pos_x, player_pos_y = player.get_current_cell()
        matrix = np.copy(base_matrix)
        matrix[player_pos_y][player_pos_x] = 6
        for enemy in enemies.values():
            pos_x, pos_y = enemy.get_current_cell()
            matrix[pos_y][pos_x] = 5 if fear_state and enemy.pos != enemy.home else 4
        if params["toggle"]:
            if not np.array_equal(old_matrix, matrix):
                old_matrix = np.copy(matrix)
                change_surface(params["window"].size, params["renderer"], matrix)

        # Game updates
        pygame.display.update()
        FramePerSec.tick(FPS)

        # FPS
        pygame.display.set_caption(f"Pacman (FPS: {FramePerSec.get_fps():.1f})")


def get_theme() -> pygame_menu.themes.Theme:
    """
    Return a configured pygame_menu theme.

    :return: The pygame_menu theme.
    """
    my_theme = pygame_menu.themes.THEME_DARK
    my_theme.widget_font = pygame_menu.font.FONT_8BIT
    my_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    return my_theme


def main_menu() -> None:
    """
    Main menu
    """

    my_menu = pygame_menu.Menu("", WIDTH, HEIGHT, theme=get_theme())
    my_menu.add.label("Pacman", font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 100))
    my_menu.add.button("Play", run)
    my_menu.add.button("Credits", credits_menu)
    my_menu.add.button("Scores", score_menu)
    my_menu.add.button("Quit", pygame_menu.events.EXIT)
    my_menu.mainloop(display_surface)


def credits_menu() -> None:
    """
    Credits menu
    """

    my_credits = pygame_menu.Menu("", WIDTH, HEIGHT, theme=get_theme())
    my_credits.add.label("Credits", font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 20))
    my_credits.add.label("Creator\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(0, 0))
    my_credits.add.label("Co Creator\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-15, 0))
    my_credits.add.label("Director\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-5, 0))
    my_credits.add.label("Programmer\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-25, 0))
    my_credits.add.label("Artist\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(8, 0))
    my_credits.add.label("Writer\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(5, 0))
    my_credits.add.label("Designer\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-5, 0))
    my_credits.add.label("Playtester\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-20, 0))
    my_credits.add.label("Producer\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-8, 0))
    my_credits.add.label("Special Thanks\t Dizzy", font_size=12, font_color=(200, 200, 200), margin=(-38, 30))
    my_credits.add.button("Back", main_menu)
    my_credits.mainloop(display_surface)


def score_menu() -> None:
    """
    High score menu
    """

    my_scores = pygame_menu.Menu("", WIDTH, HEIGHT, theme=get_theme())
    my_scores.add.label("High Scores", font_size=32, font_color=(130, 130, 130), font_shadow=True, margin=(0, 20))

    # Load high scores
    with open("resources/high_scores.yaml", "r", encoding="utf-8") as stream:
        try:
            high_scores = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    top_score = {"name": "God", "value": "∞"}

    # Sort dict (based on score value)
    high_scores = [top_score] + sorted(high_scores, key=lambda d: d["value"], reverse=True)
    indexes = [0, 1, 2] + sorted(list(random.sample(range(3, len(high_scores)), 7)))

    def def_value() -> tuple[int, int, int]:
        return 200, 200, 200

    colours = defaultdict(def_value)  # type: defaultdict[Any, tuple[int, int, int]]
    colours[0] = (255, 215, 0)  # gold
    colours[1] = (165, 169, 180)  # silver
    colours[2] = (205, 127, 50)  # bronze

    # Print names and (random selection of) scores
    for i, index in enumerate(indexes):
        my_scores.add.label(
            f"{index + 1:02d}", font_size=14, align=ALIGN_LEFT, font_color=colours[i], font_shadow=True, margin=(10, 0)
        )
        my_scores.add.label(
            f"{high_scores[index]['name']:<14}",
            font_size=14,
            align=ALIGN_LEFT,
            font_color=colours[i],
            font_shadow=True,
            margin=(50, 0),
            float=True,
        )
        value = (
            f"{high_scores[index]['value']:06d}"
            if isinstance(high_scores[index]["value"], int)
            else high_scores[index]["value"]
        )
        if i == 0:
            lbl = my_scores.add.label(
                "8",
                font_size=14,
                align=ALIGN_RIGHT,
                font_color=colours[i],
                font_shadow=True,
                margin=(-20, 0),
                float=True,
            )
            lbl.rotate(90)  # type: ignore
        else:
            my_scores.add.label(
                f"{value}",
                font_size=14,
                align=ALIGN_RIGHT,
                font_color=colours[i],
                font_shadow=True,
                margin=(-20, 0),
                float=True,
            )

    my_scores.add.label("", font_size=12, font_color=(200, 200, 200), margin=(0, 20))
    my_scores.add.button("Back", main_menu)
    my_scores.mainloop(display_surface)


if __name__ == "__main__":
    main_menu()

    # Press key (for AI):
    # https://stackoverflow.com/questions/55728777/how-to-simulate-key-press-event-in-python-on-another-program-running-in-python
