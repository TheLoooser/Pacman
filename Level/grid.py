"""
This module contains an enumeration of directions and the grid (i.e. the map) of the game.
"""

import random
from enum import Enum

from Level.cell import Cell
from Logic.dot import Dot


class Direction(Enum):
    """
    An enumeration of the four main directions.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Grid:
    """
    A class to represent a grid.
    """

    def __init__(self):
        """
        Constructs a grid object (2D matrix).
        """
        self.walls = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def init_map(self) -> list[list[Cell]]:
        """
        Initialises the grid with the appropriate cell sprites.

        :return: A matrix of cell objects.
        """
        home = [(9, 9), (8, 10), (9, 10), (10, 10)]
        cells = []
        for j in range(22):
            grid_row = []
            for i in range(19):
                if self.walls[j][i]:
                    if (i, j) in home:
                        grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 0)))
                    else:
                        grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 255)))
                else:
                    grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 0)))
            cells.append(grid_row)

        return cells

    def init_dots(self, pellets: list[tuple[int, int]]) -> dict[tuple[int, int], Dot]:
        """
        Initialises the dots (and pellets) on the grid.

        :param pellets: A list of coordinates of the large dots.
        :return: A dictionary of dot objects.
        """
        dots = {}
        for j in range(22):
            for i in range(19):
                if not self.walls[j][i]:
                    is_pellet = (i, j) in pellets
                    dots[(i, j)] = Dot(i * 20 + 10, j * 20 + 10, is_pellet)

        return dots

    def is_wall(self, i: int, j: int) -> bool:
        """
        Checks whether the cell at the given position is a wall or not.

        :param i: The vertical index (row).
        :param j: The horizontal index (column).
        :return: True if the cell at this location if a wall, False otherwise.
        """
        return self.walls[i][j]

    def get_next_cell(self, current_cell: tuple[int, int], direction: int) -> tuple[int, int]:
        """
        Get the next adjacent cell in a given direction.

        :param current_cell: The current cell (usually of the player).
        :param direction: The facing direction.
        :return: A tuple of indexes corresponding to the next cell
        """
        i, j = current_cell
        if direction == -1:
            return i, j

        if direction % 2 == 0:
            j = j - 1 if direction == 0 else j + 1
        else:
            i = i + 1 if direction == 1 else i - 1

        # Todo: Modulo to wrap top/bot
        return i % len(self.walls[0]), j

    def get_cell_in_front(self, i: int, j: int, direction: int, n: int = 2) -> tuple[int, int]:
        """
        Recursively get the position of the cell n stapes in front of the given position.

        :param i: The vertical index (row) of the current cell.
        :param j: The horizontal index (column) of the current cell.
        :param direction:  The facing direction.
        :param n: The depth of the recursion
        :return: A tuple of indexes corresponding to the next cell
        """
        # print(f"{i},{j}, {direction}")
        if n == 0:
            return i, j

        def swap(left, right):
            return right, left

        if self.is_wall(*swap(*self.get_next_cell((i, j), direction))):
            return i, j

        match direction:
            case Direction.UP.value:
                return self.get_cell_in_front(i, j - 1, direction, n - 1)
            case Direction.RIGHT.value:
                return self.get_cell_in_front((i + 1) % len(self.walls[0]), j, direction, n - 1)
            case Direction.DOWN.value:
                return self.get_cell_in_front(i, j + 1, direction, n - 1)
            case Direction.LEFT.value:
                return self.get_cell_in_front((i - 1) % len(self.walls[0]), j, direction, n - 1)
            case _:
                print(f"Direction = {direction}")
                print("This should not have happened...?")
                return i, j

    def get_adjacent_cells(self, c_i: int, c_j: int, n: int = 1, is_not_wall: bool = False) -> list[list[int]]:
        """
        Get a list of tuples containing the indexes of all adjacent cells.

        :param c_i: The vertical index (row) of the given cell.
        :param c_j: The horizontal index (column) of the given cell.
        :param n: The radius in which to look for adjacent cells.
        :param is_not_wall: Whether to include walls or not.
        :return: The list of tuples containing the indexes of the adjacent cells.
        """
        indexes = []
        start_i, start_j = (c_i - n) % len(self.walls[0]), (c_j - n) % len(self.walls)
        for _ in range(2 * n + 1):
            for _ in range(2 * n + 1):
                if start_i == (c_i - n) % len(self.walls[0]) \
                        or start_j == (c_j - n) % len(self.walls) \
                        or start_i == (c_i + n) % len(self.walls[0]) \
                        or start_j == (c_j + n) % len(self.walls):
                    if is_not_wall and not self.is_wall(start_j, start_i):
                        indexes.append([start_i, start_j])
                    elif not is_not_wall:
                        indexes.append([start_i, start_j])

                start_j = (start_j + 1) % len(self.walls)
            start_i = (start_i + 1) % len(self.walls[0])
            start_j = (c_j - n) % len(self.walls)

        return indexes

    def get_random_position(self) -> tuple[int, int]:
        """
        Get a random position on the grid, which is not a wall.

        :return: A tuple of indexes corresponding to a random cell
        """

        i = random.randint(0, len(self.walls) - 1)
        while sum(self.walls[i]) == len(self.walls[0]):
            i = random.randint(0, len(self.walls) - 1)

        j = random.randint(0, len(self.walls[i]) - 1)
        while self.walls[i][j] == 1:
            j = (j + 1) % len(self.walls[i])

        return i, j


if __name__ == "__main__":
    g = Grid()
    c = g.get_cell_in_front(4, 16, 3, 2)
    print(c)

    a = g.get_adjacent_cells(1, 2, 2, True)
    print(a)
