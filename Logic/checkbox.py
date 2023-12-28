"""
This file contains an implementation of checkboxes.
Code is based on: https://stackoverflow.com/questions/38551168/radio-button-in-pygame
"""

import pygame

pygame.font.init()


class CheckBox:
    """
    A class to represent a checkbox.
    """
    def __init__(self, surface: pygame.Surface, x: float, y: float, color: tuple[int, int, int] = (230, 230, 230),
                 caption: str = "", outline_color: tuple[int, int, int] = (0, 0, 0),
                 check_color: tuple[int, int, int] = (0, 0, 0), font_size: int = 22,
                 font_color: tuple[int, int, int] = (0, 0, 0), text_offset: tuple[int, int] = (28, 1),
                 font: pygame.font = pygame.font.SysFont('Ariel Black', 22), checked: bool = False) -> None:
        """
        Constructs a checkbox object.

        :param surface: The surface on which the checkbox is drawn.
        :param x: The horizontal position.
        :param y: The vertical position.
        :param color: The checkbox colour.
        :param caption: The caption of the checkbox.
        :param outline_color: The outline colour.
        :param check_color: The colour of the checkmark.
        :param font_size: The font size.
        :param font_color: The font colour.
        :param text_offset: The offset of the text.
        :param font: The font.
        :param checked: Whether the checkbox is checked or not.
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.font = font

        # checkbox object
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, _ = self.font.size(self.caption)
        self.checkbox_obj = pygame.Rect(self.x + w + 24, self.y + 4, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = checked
        self.click = False

    def _draw_button_text(self) -> None:
        """
        Draws the caption of the checkbox.

        :return: Nothing.
        """
        _, h = self.font.size(self.caption)
        self.font_pos = (self.x, self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self) -> None:
        """
        Renders the checkbox.

        :return: Nothing.
        """
        self._draw_button_text()
        if not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            w, _ = self.font.size(self.caption)
            pygame.draw.circle(self.surface, self.cc, (self.x + w + 30, self.y + 10), 4)
        elif self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)

    def _update(self) -> None:
        """
        Fill in or clear the checkbox.

        :return: Nothing.
        """
        x, y = pygame.mouse.get_pos()
        px, py, w, _ = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True
            print(str(self.caption) + ' toggle ' + str(self.checked))

    def update_checkbox(self, event_object) -> None:
        """
        Updates the checkbox.

        :param event_object: An input event object.
        :return: Nothing.
        """
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update()
