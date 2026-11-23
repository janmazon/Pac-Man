from .cell import Cell, PelletType


class Maze():

    _map: list[list[Cell]]
    _test: list[list[int]]
    _height: int
    _width: int

    def __init__(self, mazegen: list[list[int]]) -> None:
        self._test = mazegen
        self._create_cells(mazegen)
        self._height = len(mazegen)

        if mazegen:
            self._width = len(mazegen[0])
        else:
            self._width = 0

        self._place_special_pellets()

    def _place_special_pellets(self) -> None:
        if self._width == 0 or self._height == 0:
            return

        center = self.getCell(self._width // 2, self._height // 2)
        center.setPellet(PelletType.NONE)

        max_x = self._width - 1
        max_y = self._height - 1
        corners = [
            (0, 0),
            (max_x, 0),
            (0, max_y),
            (max_x, max_y),
        ]
        for x, y in corners:
            cell = self.getCell(x, y)
            if not cell._is_42:
                cell.setPellet(PelletType.SUPER)

    def _create_cells(self, mazgen: list[list[int]]) -> None:

        self._map = []
        for i in range(len(mazgen)):
            self._map.append([])

            for j in range(len(mazgen[i])):

                self._map[i].append(Cell(mazgen[i][j]))

    def getCell(self, x: int, y: int) -> Cell:

        return self._map[y][x]

    def getHeight(self) -> int:

        return self._height

    def getWidth(self) -> int:

        return self._width

    # Test methods

    def print_info(self) -> None:
        print(f"Hello I'm Maze and this is my list:\n{self._test}")
        print(f"Celda (0, 0): {self._map[0][0].__str__()}")
        print(f"Celda (1, 0): {self._map[1][0].__str__()}")
        print(f"Celda (0, 1): {self._map[0][1].__str__()}")
