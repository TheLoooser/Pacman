import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import sys


def blur_surface(surface, amount):
    if amount < 1:
        raise ValueError("")

    scale = 1.0 / float(amount)
    surface_size = surface.get_size()
    scale_size = (int(surface_size[0] * scale), int(surface_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surface_size)
    return surf


def paused(display, clock, width, height):
    # Darken pause background
    s = pygame.Surface((width, height))  # the size of your rect
    s.set_alpha(50)  # alpha level
    s.fill((50, 50, 50))  # this fills the entire surface
    display.blit(s, (0, 0))

    # Print pause text
    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 50)
    text = font.render('Pause', True, (222, 222, 222))
    # text.set_alpha(200)
    text_rect = text.get_rect()
    text_rect.center = ((display.get_width() / 2), (display.get_height() / 2))
    display.blit(text, text_rect)

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
        clock.tick(15)


def draw_hud(display, nr_of_lives, score):
    # Life text
    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 16)
    text = font.render('Lives:', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (35, 455)
    display.blit(text, text_rect)

    # Life icons
    life = pygame.Surface((30, 30))
    life.fill((0, 0, 0))
    life.set_colorkey((0, 0, 0))
    pygame.draw.circle(life, (255, 255, 0), (30 // 2, 30 // 2), 7)
    rect = life.get_rect()

    for i in range(nr_of_lives):
        display.blit(life, (rect[0] + 60 + i*20, rect[1] + 440, rect[2] + 60 + i*20, rect[3] + 470))

    # Score text
    font = pygame.font.Font(file_path, 16)
    text = font.render('Score:', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (230, 455)
    display.blit(text, text_rect)

    # Current score
    font = pygame.font.Font(file_path, 16)
    text = font.render(f'{score}', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (320, 455)
    display.blit(text, text_rect)


def draw_surface(display, surfaces):
    for surf in surfaces:
        display.blit(surf.surf, surf.rect)
