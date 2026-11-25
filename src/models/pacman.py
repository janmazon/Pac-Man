from enum import Enum


class Directions(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class PacMan():

    _coords: tuple[int, int]
    _lives: int
    _respawn_point: tuple[int, int]
    _cheats: bool
    _invincible: bool
    _speed: float  # Tengo dudas de este
    _facing: Directions

    def __init__(
            self, p_coords: tuple[int, int],
            p_lives: int):
        self._coords = p_coords
        self._lives = p_lives
        self._respawn_point = p_coords
        self._cheats = False
        self._invincible = False
        self._speed = 1.0
        self._facing = Directions.EAST

    def getCoords(self) -> tuple[int, int]:
        return self._coords

    def getLives(self) -> int:
        return self._lives

    def move(self, direction: Directions, level: "Level") -> None:
        from .level import Level

        x, y = self._coords

        cell = level.getMaze().getCell(x, y)
        if not cell.has_wall(direction):

            match direction:

                case Directions.NORTH:
                    if y-1 >= 0:
                        self._coords = (x, y-1)
                        self._facing = Directions.NORTH

                case Directions.EAST:
                    if x+1 >= 0:
                        self._coords = (x+1, y)
                        self._facing = Directions.EAST

                case Directions.SOUTH:
                    if y+1 >= 0:
                        self._coords = (x, y+1)
                        self._facing = Directions.SOUTH

                case Directions.WEST:
                    if x-1 >= 0:
                        self._coords = (x-1, y)
                        self._facing = Directions.WEST

    # Test methods

    def print_info(self) -> None:
        print("Hello I'm PacMan")
