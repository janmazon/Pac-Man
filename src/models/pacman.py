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
    _prev_coords: tuple[int, int]
    _move_progress: float
    _next_direction: Directions

    def __init__(
            self, p_coords: tuple[int, int],
            p_lives: int):
        self._coords = p_coords
        self._lives = p_lives
        self._respawn_point = p_coords
        self._cheats = False
        self._invincible = False
        self._speed = 4.0
        self._facing = Directions.EAST
        self._prev_coords = p_coords
        self._move_progress = 1.0
        self._next_direction = Directions.EAST

    def getCoords(self) -> tuple[int, int]:
        return self._coords

    def getLives(self) -> int:
        return self._lives

    def getFacing(self) -> Directions:
        return self._facing

    def setFacing(self, direction: Directions) -> None:
        self._facing = direction

    def setNextDirection(self, direction: Directions) -> None:
        self._next_direction = direction

    def move(self, direction: Directions, level: "Level") -> None:
        from .level import Level

        x, y = self._coords
        self._facing = direction

        cell = level.getMaze().getCell(x, y)
        if not cell.has_wall(direction):

            match direction:

                case Directions.NORTH:
                    if y-1 >= 0:
                        self._coords = (x, y-1)

                case Directions.EAST:
                    if x+1 >= 0:
                        self._coords = (x+1, y)

                case Directions.SOUTH:
                    if y+1 >= 0:
                        self._coords = (x, y+1)

                case Directions.WEST:
                    if x-1 >= 0:
                        self._coords = (x-1, y)

            self._prev_coords = (x, y)

    def update(self, dt: float, level: "Level") -> None:
        from .level import Level

        if self._move_progress < 1.0:

            if (self._move_progress + self._speed * dt) >= 1.0:
                self._move_progress = 1.0
                self._prev_coords = self._coords
            else:
                self._move_progress += self._speed * dt

        elif self._move_progress >= 1.0:
            x, y = self._coords
            cell = level.getMaze().getCell(x, y)
            if not cell.has_wall(self._next_direction):
                self.move(self._facing, level)
                self._move_progress = 0.0
                self._facing = self._next_direction

    def getVisualCoords(self, ) -> tuple[float, float]:

        prev_x, prev_y = self._prev_coords
        current_x, current_y = self._coords
        x = prev_x + (current_x - prev_x) * self._move_progress
        y = prev_y + (current_y - prev_y) * self._move_progress

        return (x, y)

    # Test methods

    def print_info(self) -> None:
        print("Hello I'm PacMan")
