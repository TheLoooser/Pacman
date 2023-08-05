import random
import pygame
from pygame._sdl2 import Window, Texture, Renderer  # WARNING: Module still in development


def cell_number(number):
    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 8)
    text = font.render(f"{number}", True, (0, 0, 0))
    return text


def change_surface(window_size, renderer, color=(255, 255, 255)):
    surf = pygame.Surface(window_size)
    surf.fill(color)

    r = random.randint(0, 5)
    t = cell_number(r)
    for i in range(19):
        for j in range(22):
            tr = t.get_rect()
            w = window_size[0] / 19
            h = window_size[1] / 22
            tr.center = (w * i + w / 2, h * j + h / 2)
            surf.blit(t, tr)

    tex = Texture.from_surface(renderer, surf)
    renderer.clear()
    tex.draw()
    renderer.present()
    del tex


def create_window(color=(255, 255, 255)):
    win = Window("2nd window", size=(256, 256), always_on_top=True)
    win.opacity = 0.8
    renderer = Renderer(win)
    change_surface(win.size, renderer, color)

    return win, renderer
