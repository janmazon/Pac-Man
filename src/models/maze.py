from .cell import Cell


class Maze():

    _map: list[list[Cell]]
    _test: list[list[int]]

    def __init__(self, mazegen: list[list[int]]):
        self._test = mazegen
        self._create_cells(mazegen)

    def _create_cells(self, mazgen: list[list[int]]) -> None:

        self._map = []
        for i in range(len(mazgen)):
            self._map.append([])

            for j in range(len(mazgen[i])):

                self._map[i].append(Cell(mazgen[i][j]))

    def getCell(self, x: int, y: int) -> Cell:

        return self._map[x][y]

    # Test methods

    def print_info(self) -> None:
        print(f"Hello I'm Maze and this is my list:\n{self._test}")
        print(f"Celda (0, 0): {self._map[0][0].__str__()}")
        print(f"Celda (1, 0): {self._map[1][0].__str__()}")
        print(f"Celda (0, 1): {self._map[0][1].__str__()}")
