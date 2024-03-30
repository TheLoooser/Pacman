"""
This module contains an implementation of an input box.
Code is based on: https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
"""
import pygame as pg
import pygame.event

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:
    """
    A class to represent an input box.
    """

    def __init__(self, x: int, y: int, w: int, h: int, text: str = '', active: bool = False) -> None:
        """
        Constructs an input box object.

        :param x: The horizontal position.
        :param y: The vertical position.
        :param w: The width.
        :param h: The height.
        :param text: The text.
        :param active: Whether the input box is active or not.
        """
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE if not active else COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = active

    def handle_event(self, event: pygame.event.Event) -> None | str:
        """
        Handle the interactions with the input box.

        :param event: A pygame event.
        :return: Nothing.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_ESCAPE:
                    self.active = False
                    self.color = COLOR_INACTIVE
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

        return None

    def update(self) -> None:
        """
        Updates the input box (resize).

        :return: Nothing.
        """
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the input box.

        :param screen: A pygame surface on which to draw the input box.
        :return: Nothing.
        """
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
