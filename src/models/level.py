from .maze import Maze
from .pacman import PacMan
from .ghosts import Ghost
from src.factories import GhostFactory


class Level():

    _maze: Maze
    _ghosts: list[Ghost]
    _pacman: PacMan
    _score: int
    _cheats: bool

    def __init__(self, mazegen: list[list[int]]) -> None:
        self._maze = Maze(mazegen)
        self._initialize_ghosts()
        self._initialize_pacman()
        self._score = 0
        self._cheats = False

    def getMaze(self) -> Maze:
        return self._maze

    def setMaze(self, p_maze: Maze) -> None:
        self._maze = p_maze

    def getGhosts(self) -> list[Ghost]:
        return self._ghosts

    def setGhosts(self, p_ghosts: list[Ghost]) -> None:
        self._ghosts = p_ghosts

    def getPacman(self) -> PacMan:
        return self._pacman

    def setPacman(self, p_pacman: PacMan) -> None:
        self._pacman = p_pacman

    def _initialize_ghosts(self) -> None:

        col = self._maze.getWidth() - 1
        row = self._maze.getHeight() - 1
        self._ghosts = GhostFactory.create_all(col, row)
        """ self._ghosts = []
        self._ghosts.append(Blinky((0, 0)))
        self._ghosts.append(Pinky((max_x, 0)))
        self._ghosts.append(Inky((0, max_y)))
        self._ghosts.append(Clyde((max_x, max_y))) """

    def _initialize_pacman(self) -> None:

        center_x = self._maze.getWidth() // 2
        center_y = self._maze.getHeight() // 2
        self._pacman = PacMan((center_x, center_y), 3)

    # Test methods

    def print_info(self) -> None:

        self._pacman.print_info()
        for i in range(0, 4):
            self._ghosts[i].print_info()

        self._maze.print_info()
