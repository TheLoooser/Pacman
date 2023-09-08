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

    font = pygame.font.Font(file_path, 18)
    text = font.render('Press ESC to continue', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = ((display.get_width() / 2), (display.get_height() / 2) + 50)
    display.blit(text, text_rect)

    pause = True
    while pause:
        # Exit upon pressing ALT + F4
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LALT] and keys[pygame.K_F4]:
            pygame.quit()
            sys.exit(0)

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

    # Copyright
    smallfont = pygame.font.Font(file_path, 10)
    text = smallfont.render('© 2023', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (180, 455)
    display.blit(text, text_rect)

    # Score text
    text = font.render('Score:', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (270, 455)
    display.blit(text, text_rect)

    # Current score
    score = score % 1600000
    if score > 999999:
        score = str(score)
        score = chr(int(score[:2]) + 55) + score[2:]
    else:
        score = str(score).zfill(6)
    font = pygame.font.Font(file_path, 16)
    text = font.render(f'{score}', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (340, 455)
    display.blit(text, text_rect)


def draw_surface(display, surfaces):
    for surf in surfaces:
        display.blit(surf.surf, surf.rect)
