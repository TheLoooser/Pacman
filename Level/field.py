"""
This module contains an implementation of a Field object
(similar to the cell object, but without the sprite).
"""


class Field:
    """
    A class to represent a field (square on the grid).
    """
    def __init__(self, x: int, y: int, colour: tuple[int, int, int]):
        """
        Constructs a field object.

        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :param colour: The colour of the cell/sprite.
        """
        self._x = x
        self._y = y
        self._colour = colour

    @property
    def colour(self) -> tuple[int, int, int]:
        """
        Get the colour of the field.

        :return: The colour.
        """
        return self._colour

    @colour.setter
    def colour(self, colour: tuple[int, int, int]) -> None:
        """
        Set the field colour.

        :param colour: The new colour.
        :return: Nothing.
        """
        self._colour = colour

    @property
    def coordinates(self) -> tuple[int, int]:
        """
        Get the coordinates of the field.

        :return: The field coordinates.
        """
        return self._x, self._y

    @coordinates.setter
    def coordinates(self, coordinates: tuple[int, int]) -> None:
        """
        Set the coordinates of the field.

        :param coordinates: The new coordinates.
        :return: Nothing.
        """
        self._x = coordinates[0]
        self._y = coordinates[1]
