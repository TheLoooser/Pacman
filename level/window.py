"""
This module contains functions which enable the creation of a second window.
"""
from collections.abc import Iterable

import numpy
import pygame
from pygame._sdl2 import Renderer  # WARNING: Module still in development
from pygame._sdl2 import Texture, Window


def change_surface(window_size: Iterable[int], renderer: Renderer, matrix: numpy.ndarray) -> None:
    """
    Updates the surface of the second window.

    :param window_size: The size of the secondary window.
    :param renderer: The renderer.
    :param matrix: The matrix of the main game window.
    :return: Nothing.
    """
    window_size = tuple(window_size)
    surf = pygame.Surface(window_size)
    surf.fill((255, 255, 255))

    w = window_size[0] / 19
    h = window_size[1] / 22

    file_path = "resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 8)
    colour_dict = {
        0: (0, 0, 0),  # corridor
        1: (0, 0, 255),  # wall
        2: (69, 69, 69),  # dot
        3: (34, 139, 34),  # pellet
        4: (255, 0, 0),  # ghost
        5: (255, 105, 180),  # feared ghost
        6: (255, 69, 0),  # player
    }

    for i in range(19):
        for j in range(22):
            number = int(matrix[j][i])
            t = font.render(f"{number}", True, colour_dict[number])
            tr = t.get_rect()
            tr.center = (int(w * i + w / 2), int(h * j + h / 2))
            surf.blit(t, tr)

    tex = Texture.from_surface(renderer, surf)
    renderer.clear()
    tex.draw()
    renderer.present()
    del tex


def create_window(matrix: numpy.ndarray) -> tuple[Window, Renderer]:
    """
    Creates a second window.

    :param matrix: The matrix of the main game window.
    :return: The second window instance and its renderer.
    """
    win = Window("2nd window", size=(256, 256), always_on_top=True)
    win.opacity = 1.0  # 0.8
    renderer = Renderer(win)
    change_surface(win.size, renderer, matrix)

    return win, renderer
