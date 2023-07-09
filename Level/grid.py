from enum import Enum
from Level.cell import Cell


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Grid:
    def __init__(self):
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

    def init_map(self):
        cells = []
        for j in range(22):
            grid_row = []
            for i in range(19):
                if self.walls[j][i]:
                    grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 255)))
                else:
                    grid_row.append(Cell(i * 20 + 10, j * 20 + 10, (0, 0, 0)))
            cells.append(grid_row)

        return cells

    def is_wall(self, i, j):
        return self.walls[i][j]

    def get_next_cell(self, current_cell, direction):
        i, j = current_cell
        if direction == -1:
            return i, j

        if direction % 2 == 0:
            j = j - 1 if direction == 0 else j + 1
        else:
            i = i + 1 if direction == 1 else i - 1

        # Todo: Modulo to wrap top/bot
        return i % len(self.walls[0]), j

    def get_cell_in_front(self, i, j, direction, n=2):
        # print(f"{i},{j}, {direction}")
        if n == 0:
            return i, j

        def swap(a, b):
            return b, a

        if self.is_wall(*swap(*self.get_next_cell((i, j), direction))):
            return i, j
        else:
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

    def get_adjacent_cells(self, c_i, c_j, n=1, is_not_wall=False):
        indexes = []
        start_i, start_j = (c_i - n) % len(self.walls[0]), (c_j - n) % len(self.walls)
        for i in range(2 * n + 1):
            for j in range(2 * n + 1):
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


if __name__ == "__main__":
    g = Grid()
    c = g.get_cell_in_front(4, 16, 3, 2)
    print(c)

    a = g.get_adjacent_cells(1, 2, 2, True)
    print(a)
