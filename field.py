class Field:
    def __init__(self, x, y, colour):
        self._x = x
        self._y = y
        self._colour = colour

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    @property
    def coordinates(self):
        return self._x, self._y

    @coordinates.setter
    def coordinates(self, coordinates):
        self._x = coordinates[0]
        self._y = coordinates[1]
