from enum import Enum
from abc import ABC, abstractmethod


class Status(Enum):
    CHASE = "chase"
    FRIGHTENED = "frightened"
    EATEN = "eaten"
    SPAWN = "spawn"
    FROZEN = "frozen"
    START = "start"


class Personality(Enum):

    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class Color(Enum):

    RED = "red"
    PINK = "pink"
    CYAN = "cyan"
    ORANGE = "orange"
    BLUE = "blue"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Ghost(ABC):

    _coords: tuple[int, int]
    _edible: bool
    _respawn_point: tuple[int, int]
    _status: Status
    _color: Color
    _personality: Personality
    _direction: Direction

    def __init__(self, p_coords: tuple[int, int]) -> None:

        self._coords = p_coords
        self._respawn_point = p_coords
        self._edible = False
        self._status = Status.START
        self._direction = Direction.RIGHT

    def getCoords(self) -> tuple[int, int]:
        return self._coords

    def getColor(self) -> Color:
        return self._color

    def getDirection(self) -> Direction:
        return self._direction

    def setDirection(self, p_direction: Direction) -> None:
        self._direction = p_direction

    @abstractmethod
    def chase_pacman(self) -> None:
        pass

    # Test methods

    def print_info(self) -> None:
        print(f"Hello I'm Ghost {self._personality.value}")
        print("And my chase is:", end="")
        self.chase_pacman()


class Blinky(Ghost):

    _personality: Personality = Personality.BLINKY
    _color: Color = Color.RED

    def __init__(self, p_coords: tuple[int, int]) -> None:
        super().__init__(p_coords)

    def chase_pacman(self) -> None:
        print("Direct chase")


class Pinky(Ghost):

    _personality: Personality = Personality.PINKY
    _color: Color = Color.PINK

    def __init__(self, p_coords: tuple[int, int]) -> None:
        super().__init__(p_coords)

    def chase_pacman(self) -> None:
        print("Ambush chase")


class Inky(Ghost):

    _personality: Personality = Personality.INKY
    _color: Color = Color.CYAN

    def __init__(self, p_coords: tuple[int, int]) -> None:
        super().__init__(p_coords)

    def chase_pacman(self) -> None:
        print("Unpredictible chase")


class Clyde(Ghost):

    _personality: Personality = Personality.CLYDE
    _color: Color = Color.ORANGE

    def __init__(self, p_coords: tuple[int, int]) -> None:
        super().__init__(p_coords)

    def chase_pacman(self) -> None:
        print("Indiferent chase")
