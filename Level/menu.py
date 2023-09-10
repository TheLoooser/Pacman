import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import sys

from Logic import checkbox


def blur_surface(surface, amount):
    if amount < 1:
        raise ValueError("")

    scale = 1.0 / float(amount)
    surface_size = surface.get_size()
    scale_size = (int(surface_size[0] * scale), int(surface_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surface_size)
    return surf


def print_text(display, text, font_size, colour, x_pos, y_pos, clickable=False):
    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, font_size)
    text = font.render(text, True, colour)
    # text.set_alpha(200)
    text_rect = text.get_rect()
    text_rect.center = (x_pos, y_pos)
    display.blit(text, text_rect)
    return text_rect if clickable else None


def paused(display, clock, width, height, checkboxes):
    # Darken pause background
    s = pygame.Surface((width, height))  # the size of your rect
    s.set_alpha(50)  # alpha level
    s.fill((50, 50, 50))  # this fills the entire surface
    display.blit(s, (0, 0))

    # Print pause text
    print_text(display, "Pause", 50, (222, 222, 222),
               (display.get_width() / 2), (display.get_height() * .2))
    print_text(display, "Press ESC to continue", 18, (222, 222, 222),
               (display.get_width() / 2), (display.get_height() * .2) + 50)
    # Buttons
    # Todo: Add subtexts to buttons (for secondary texts -> smaller fontsize, under main text)
    button_rects = {'back': print_text(display, "BACK (Resume Game)", 18, (222, 222, 222),
                                       (display.get_width() / 2), (display.get_height() / 2) + 50, True),
                    'exit': print_text(display, "EXIT (Return to Main Menu)", 18, (222, 222, 222),
                                       (display.get_width() / 2), (display.get_height() / 2) + 80, True),
                    'quit': print_text(display, "QUIT (Close the application)", 18, (222, 222, 222),
                                       (display.get_width() / 2), (display.get_height() * .8), True)}

    # Checkbox
    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 18)
    chckbx = checkbox.CheckBox(display, (display.get_width() * .3), (display.get_height() / 2), 1,
                               caption="Highlight paths", font=font, font_color=(222, 222, 222),
                               checked=checkboxes['path_highlights'])

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        match button:
                            case "back":
                                pause = False
                            case "exit":
                                pause = False
                                from main import main_menu
                                main_menu()
                            case "quit":
                                pygame.quit()
                                sys.exit()
                            case _:
                                sys.exit("Button not found.")

            chckbx.update_checkbox(event)

        chckbx.render_checkbox()
        pygame.display.update()
        clock.tick(15)

    checkboxes['path_highlights'] = chckbx.checked
    return checkboxes


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
        display.blit(life, (rect[0] + 60 + i * 20, rect[1] + 440, rect[2] + 60 + i * 20, rect[3] + 470))

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
