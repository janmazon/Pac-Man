from .maze import Maze
from .pacman import PacMan
from .ghosts import Ghost, Blinky, Pinky, Inky, Clyde


class Level():

    _maze: Maze
    _ghosts: list[Ghost]
    _pacman: PacMan
    _score: int
    _cheats: bool

    def __init__(self, mazegen: list[list[int]]):
        self._maze = Maze(mazegen)
        self._initialize_ghosts()
        self._initialize_pacman()
        self._score = 0
        self._cheats = False

    def getMaze(self) -> Maze:
        return self._maze

    def setMaze(self, p_maze: Maze) -> None:
        self._maze = p_maze

    def _initialize_ghosts(self) -> None:

        self._ghosts = []
        self._ghosts.append(Blinky((0, 0)))
        self._ghosts.append(Pinky((0, 0)))
        self._ghosts.append(Inky((0, 0)))
        self._ghosts.append(Clyde((0, 0)))

    def _initialize_pacman(self) -> None:

        self._pacman = PacMan((0, 0), 3)

    # Test methods

    def print_info(self) -> None:

        self._pacman.print_info()
        for i in range(0, 4):
            self._ghosts[i].print_info()

        self._maze.print_info()
