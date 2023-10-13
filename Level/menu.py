"""
This module contains menu-related functions.
"""

import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE  # pylint: disable = no-name-in-module

from Logic.input_box import InputBox
from Logic import checkbox


def blur_surface(surface: pygame.Surface, amount: int):
    """
    Blurs the given surface.

    :param surface: The surface of the whole game.
    :param amount: The intensity of the blur.
    :return: The blurred surface.
    """
    if amount < 1:
        raise ValueError("")

    scale = 1.0 / float(amount)
    surface_size = surface.get_size()
    scale_size = (int(surface_size[0] * scale), int(surface_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surface_size)
    return surf


def print_text(display: pygame.Surface, text: str, font_size: int, colour: tuple[int, int, int], x_pos: float,
               y_pos: float, clickable: bool = False, pos: str = 'center'):
    """
    Prints a given text on a given surface.

    :param display: The surface.
    :param text: The text.
    :param font_size: The font size of the text.
    :param colour: THe colour of the text.
    :param x_pos: The horizontal position on the surface.
    :param y_pos: The vertical position on the surface.
    :param clickable: Whether the text should be clickable or not
    :param pos: The alignment of the text
    :return: Nothing or the text rectangle
    """

    file_path = "Resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, font_size)
    text = font.render(text, True, colour)
    # text.set_alpha(200)
    text_rect = text.get_rect(center=(x_pos, y_pos)) if pos == 'center' else text.get_rect(topleft=(x_pos, y_pos))
    # text_rect.center = (x_pos, y_pos)
    display.blit(text, text_rect)
    return text_rect if clickable else None


def paused(display: pygame.Surface, clock: pygame.time.Clock, width: int, height: int, checkboxes: dict[str, bool]):
    """
    Pauses the game (opens the pause menu).

    :param display: The surface.
    :param clock: A pygame clock to help track the elapsed time.
    :param width: The width of the game window.
    :param height: The height of the game window.
    :param checkboxes: A dict of checkboxes with their toggle status.
    :return: The updated dictionary of checkboxes with their status.
    """
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
                                from main import main_menu  # pylint: disable = import-outside-toplevel
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


def draw_hud(display: pygame.Surface, nr_of_lives: int, score: int):
    """
    Draws the HUD ar the bottom of the main window.

    :param display: The surface.
    :param nr_of_lives: The number of lives left.
    :param score: The current score of the player.
    :return: Nothing.
    """
    # Life text
    print_text(display, 'Lives:', 16, (222, 222, 222), 35, 455)

    # Life icons
    life = pygame.Surface((30, 30))
    life.fill((0, 0, 0))
    life.set_colorkey((0, 0, 0))
    pygame.draw.circle(life, (255, 255, 0), (30 // 2, 30 // 2), 7)
    rect = life.get_rect()

    for i in range(nr_of_lives):
        display.blit(life, (rect[0] + 60 + i * 20, rect[1] + 440, rect[2] + 60 + i * 20, rect[3] + 470))

    # Copyright
    file_path = "Resources\\PixeloidSans.ttf"
    smallfont = pygame.font.Font(file_path, 10)
    text = smallfont.render('© 2023', True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (180, 455)
    display.blit(text, text_rect)

    # Score text
    print_text(display, 'Score:', 16, (222, 222, 222), 270, 455)

    # Current score
    score = score % 1600000
    if score > 999999:
        score = str(score)
        score = chr(int(score[:2]) + 55) + score[2:]
    else:
        score = str(score).zfill(6)
    print_text(display, f'{score}', 16, (222, 222, 222), 340, 455)


def draw_surface(display: pygame.Surface, surfaces: pygame.sprite.Group):
    """
    Draws all surfaces of the given group on the main display surface.

    :param display: The surface of the main display.
    :param surfaces: A group of sprites.
    :return: Nothing.
    """
    for surf in surfaces:
        display.blit(surf.surf, surf.rect)


def game_over():
    """
    Shows the game over screen

    :return: Nothing.
    """
    clock = pygame.time.Clock()
    surf = pygame.display.get_surface()
    surf.fill((50, 50, 50))  # this fills the entire surface

    input_box = InputBox(100, 400, 140, 32, active=True)

    high_scores = [
        # SMB Any% Times
        ('Niftski', 454631),
        ('Kosmic', 455646),
        ('Darbian', 456528),
        ('GTAce', 455364),
        ('AndrewG', 456695),
        # MK64 (ASCII Letters)
        ('Abney', 777564),
        # SM64
        ('GreenSuigi', 646464),
        ('Kano', 646401),  # 0, 1 Star Runner
        ('Simply', 640000),
        # Speedrunnning Youtubers (Subscriber Count in ten)
        ('SmallAnt1', 279000),
        ('Bismuth', 20800),
        ('SummoningSalt', 175000),
        ('Linkus7', 26700),
        ('AverageTrey', 6270),
        ('Msushi', 14400),
        ('Wirtual', 105000),
        ('Karl Jobst', 88600),
        # LoL Players
        ('Faker', 999999),
        ('Uzi', 111111),
        ('XPeke', 560413),  # Game Length of Kassadin Backdoor, plus year
        ('YellowStar', 0000000),
        # Others
        ('Todd Todgers', -1),  # if you know, you know
        ('Billy Mitchell', -99),  # Video Game Player of the Century ;)
    ]
    # Sort dict (based on score value)
    high_scores = [('God', '∞')] + sorted(high_scores, key=lambda tup: tup[1], reverse=True)
    indexes = [0] + sorted(list(random.sample(range(1, len(high_scores) - 1), 8))) + [len(high_scores) - 1]

    while True:
        # Exit upon pressing ALT + F4
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LALT] and keys[pygame.K_F4]:
            pygame.quit()
            sys.exit(0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            input_box.handle_event(event)

        surf.fill((50, 50, 50))  # this fills the entire surface

        # Print title
        print_text(surf, 'High Scores', 22, (222, 222, 222), surf.get_width() / 2, 20)

        # Print names and (random selection of) scores
        for i in range(len(indexes)):
            print_text(surf, f"{indexes[i] + 1:02d}. {high_scores[indexes[i]][0]:<14}", 16,
                       (222, 222, 222), surf.get_width() / 6, 50 + 20 * i, pos='topleft')

            value = f"{high_scores[indexes[i]][1]:06d}" if isinstance(high_scores[indexes[i]][1], int) \
                else high_scores[indexes[i]][1]
            print_text(surf, f"{value}", 16, (222, 222, 222),
                       surf.get_width() - surf.get_width() / 3, 50 + 20 * i, pos='topleft')

        print_text(surf, 'Enter your name', 18, (222, 222, 222), surf.get_width() / 2, 350)

        input_box.update()
        input_box.draw(surf)

        pygame.display.update()
        clock.tick(15)
