"""
This module contains menu-related functions.
"""

import random
import sys

import pygame
import yaml
from pygame.locals import K_ESCAPE  # pylint: disable = no-name-in-module
from pygame.locals import KEYDOWN, QUIT

from logic import checkbox
from logic.input_box import InputBox
from logic.timer import Timer


def blur_surface(surface: pygame.Surface, amount: int) -> pygame.Surface:
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


def print_text(
    display: pygame.Surface,
    text: str,
    font_size: int,
    colour: tuple[int, int, int],
    x_pos: float,
    y_pos: float,
    clickable: bool = False,
    pos: str = "center",
) -> None | pygame.Rect:
    """
    Prints a given text on a given surface.

    :param display: The surface.
    :param text: The text.
    :param font_size: The font size of the text.
    :param colour: The colour of the text.
    :param x_pos: The horizontal position on the surface.
    :param y_pos: The vertical position on the surface.
    :param clickable: Whether the text should be clickable or not
    :param pos: The alignment of the text
    :return: Nothing or the text rectangle
    """

    file_path = "resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, font_size)
    txt = font.render(text, True, colour)
    # text.set_alpha(200)
    text_rect = txt.get_rect(center=(x_pos, y_pos)) if pos == "center" else txt.get_rect(topleft=(x_pos, y_pos))
    # text_rect.center = (x_pos, y_pos)
    display.blit(txt, text_rect)
    return text_rect if clickable else None


def paused(
    display: pygame.Surface,
    clock: pygame.time.Clock,
    width: int,
    height: int,
    checkboxes: dict[str, bool],
) -> dict[str, bool]:
    """
    Pauses the game (opens the pause menu).

    :param display: The surface.
    :param clock: A pygame clock to help track the elapsed time.
    :param width: The width of the game window.
    :param height: The height of the game window.
    :param checkboxes: A dict of checkboxes with their toggle status.
    :return: The updated dictionary of checkboxes with their status.
    """
    background = display.copy()
    s = pygame.Surface((width, height))  # the size of your rect
    s.set_alpha(50)  # alpha level
    s.fill((50, 50, 50))  # this fills the entire surface

    # Checkbox
    file_path = "resources\\PixeloidSans.ttf"
    font = pygame.font.Font(file_path, 18)
    chckbx = checkbox.CheckBox(
        display,
        (display.get_width() * 0.3),
        (display.get_height() / 3),
        caption="Highlight paths",
        font=font,
        font_color=(222, 222, 222),
        checked=checkboxes["path_highlights"],
    )

    pause = True
    while pause:
        # Darken pause background
        display.blit(background, (0, 0))
        display.blit(s, (0, 0))

        # Print pause text
        print_text(
            display,
            "Pause",
            50,
            (222, 222, 222),
            (display.get_width() / 2),
            (display.get_height() * 0.15),
        )
        print_text(
            display,
            "Press ESC to continue",
            18,
            (222, 222, 222),
            (display.get_width() / 2),
            (display.get_height() * 0.15) + 50,
        )

        # Buttons
        button_rects = {
            "back": print_text(
                display,
                "BACK",
                33,
                (222, 222, 222),
                (display.get_width() / 2),
                (display.get_height() / 2) + 20,
                True,
            ),
            "exit": print_text(
                display,
                "EXIT",
                33,
                (222, 222, 222),
                (display.get_width() / 2),
                (display.get_height() / 2) + 70,
                True,
            ),
            "quit": print_text(
                display,
                "QUIT",
                33,
                (222, 222, 222),
                (display.get_width() / 2),
                (display.get_height() / 2) + 120,
                True,
            ),
        }

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
                    if rect and rect.collidepoint(event.pos):
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

        def get_hover_surface(button_name: str) -> pygame.Surface:
            match button_name:
                case "back":
                    message = "Resume the game"
                case "exit":
                    message = "Return to the main menu"
                case "quit":
                    message = "Close the application"
                case _:
                    message = "Something went wrong"
            hover_surface = font.render(message, True, pygame.Color(255, 255, 255), pygame.Color(34, 34, 34))
            return hover_surface

        # Display info text when hovering over buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button, rect in button_rects.items():
            if rect and rect.collidepoint((mouse_x, mouse_y)):
                display.blit(
                    get_hover_surface(button),
                    (mouse_x - rect.width / 2, mouse_y - rect.height / 2),
                )

        chckbx.render_checkbox()
        pygame.display.update()
        clock.tick(15)

    checkboxes["path_highlights"] = chckbx.checked
    return checkboxes


def draw_hud(display: pygame.Surface, nr_of_lives: int, score: int) -> None:
    """
    Draws the HUD at the bottom of the main window.

    :param display: The surface.
    :param nr_of_lives: The number of lives left.
    :param score: The current score of the player.
    :return: Nothing.
    """
    # Life text
    print_text(display, "Lives:", 16, (222, 222, 222), 35, 455)

    # Life icons
    life = pygame.Surface((30, 30))
    life.fill((0, 0, 0))
    life.set_colorkey((0, 0, 0))
    pygame.draw.circle(life, (255, 255, 0), (30 // 2, 30 // 2), 7)
    rect = life.get_rect()

    for i in range(nr_of_lives):
        display.blit(
            life,
            (
                rect[0] + 60 + i * 20,
                rect[1] + 440,
                rect[2] + 60 + i * 20,
                rect[3] + 470,
            ),
        )

    # Copyright
    file_path = "resources\\PixeloidSans.ttf"
    smallfont = pygame.font.Font(file_path, 10)
    text = smallfont.render("© 2023", True, (222, 222, 222))
    text_rect = text.get_rect()
    text_rect.center = (180, 455)
    display.blit(text, text_rect)

    # Score text
    print_text(display, "Score:", 16, (222, 222, 222), 270, 455)

    # Current score
    score = score % 1600000
    if score > 999999:
        score_str = str(score)
        score_str = chr(int(score_str[:2]) + 55) + score_str[2:]
    else:
        score_str = str(score).zfill(6)
    print_text(display, f"{score_str}", 16, (222, 222, 222), 340, 455)


def draw_surface(display: pygame.Surface, surfaces: pygame.sprite.Group) -> None:
    """
    Draws all surfaces of the given group on the main display surface.

    :param display: The surface of the main display.
    :param surfaces: A group of sprites.
    :return: Nothing.
    """
    for surf in surfaces:
        display.blit(surf.surf, surf.rect)


def update_score(score: int, timer: Timer) -> int:
    """
    Add time based bonus point for completing the level to the score

    :param score: The current score
    :param timer: The global game timer
    :return: The updated score
    """
    time = int(timer.get_elapsed_time())
    match time:
        case _ if time < 30:
            score += 600 + 500  # max bonus
        case _ if 30 <= time < 150:
            score += (120 - (time - 30)) * 5 + 500  # type: ignore
        case _ if time >= 150:
            score += 500
        case _:
            print(f"Impossible time. You finished in {time} seconds.")
    # print(f"Beat the game in {timer.get_elapsed_time()} seconds.")
    return score


def game_over(score: int) -> None:
    """
    Shows the game over screen

    :return: Nothing.
    """
    clock = pygame.time.Clock()
    surf = pygame.display.get_surface()
    surf.fill((50, 50, 50))  # this fills the entire surface

    next_rect = None
    input_box = InputBox(100, 400, 140, 32, active=True)

    # Load high scores
    with open("resources/high_scores.yaml", "r", encoding="utf-8") as stream:
        try:
            high_scores = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    top_score = {"name": "God", "value": "∞"}

    # Sort dict (based on score value)
    high_scores = [top_score] + sorted(high_scores, key=lambda d: d["value"], reverse=True)
    indexes = [0] + sorted(list(random.sample(range(1, len(high_scores) - 1), 8))) + [len(high_scores) - 1]

    user_name = None
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

            input_box_text = input_box.handle_event(event)
            user_name = input_box_text if input_box_text is not None and user_name is None else user_name

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect:
                    if next_rect.collidepoint(event.pos):
                        # Append player score to high scores
                        with open("resources/high_scores.yaml", "a", encoding="utf-8") as f:
                            f.write(f"- name: {user_name}\n  value: {score}\n")

                        from main import main_menu  # pylint: disable = import-outside-toplevel

                        main_menu()

        surf.fill((50, 50, 50))  # this fills the entire surface

        # Print title
        print_text(surf, "High Scores", 22, (222, 222, 222), surf.get_width() / 2, 20)

        # Print names and (random selection of) scores
        for i, index in enumerate(indexes):
            print_text(
                surf,
                f"{index + 1:02d}. {high_scores[index]['name']:<14}",
                16,
                (222, 222, 222),
                surf.get_width() / 6,
                50 + 20 * i,
                pos="topleft",
            )

            value = (
                f"{high_scores[index]['value']:06d}"
                if isinstance(high_scores[index]["value"], int)
                else high_scores[index]["value"]
            )
            print_text(
                surf,
                f"{value}",
                16,
                (222, 222, 222),
                surf.get_width() - surf.get_width() / 3,
                50 + 20 * i,
                pos="topleft",
            )

        # Show input box until the player has entered a username
        if not user_name:
            print_text(surf, "Enter your name", 18, (222, 222, 222), surf.get_width() / 2, 350)

            input_box.update()
            input_box.draw(surf)
        else:
            next_rect = print_text(
                surf,
                "→ NEXT →",
                22,
                (222, 222, 222),
                (surf.get_width() / 2),
                (surf.get_height() / 2) + 150,
                True,
            )

        pygame.display.update()
        clock.tick(15)
