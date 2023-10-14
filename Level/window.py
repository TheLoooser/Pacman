"""
This module contains functions which enable the creation of a second window.
"""
from collections.abc import Iterable
import numpy
import pygame
from pygame._sdl2 import Window, Texture, Renderer  # WARNING: Module still in development


def change_surface(window_size: Iterable[int], renderer: Renderer, matrix: numpy.array) -> None:
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

    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 8)
    colour_dict = {
        0: (0, 0, 0),  # corridor
        1: (0, 0, 255),  # wall
        2: (69, 69, 69),  # dot
        99: (255, 165, 0)  # player
    }

    for i in range(19):
        for j in range(22):
            number = matrix[j][i]
            t = font.render(f"{number}", True, colour_dict[number])
            tr = t.get_rect()
            tr.center = (w * i + w / 2, h * j + h / 2)
            surf.blit(t, tr)

    tex = Texture.from_surface(renderer, surf)
    renderer.clear()
    tex.draw()
    renderer.present()
    del tex


def create_window(matrix: numpy.array) -> tuple[Window, Renderer]:
    """
    Creates a second window.

    :param matrix: The matrix of the main game window.
    :return: The second window instance and its renderer.
    """
    win = Window("2nd window", size=(256, 256), always_on_top=True)
    win.opacity = 0.8
    renderer = Renderer(win)
    change_surface(win.size, renderer, matrix)

    return win, renderer
