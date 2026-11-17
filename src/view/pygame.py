import pygame
from src.models.level import Level
from src.models.cell import Cell


class Pygame:

    _scale: float = 40
    _offset_x: float = 50
    _offset_y: float = 50
    _min_x: float
    _max_x: float
    _min_y: float
    _max_y: float
    _level: Level

    def __init__(self, p_level: Level):
        self._level = p_level

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """function that converts graph coordinates into screen coordinates.

        Args:
            x (float): coordinate x in the graph.
            y (float): coordinate y in the graph.

        Returns:
            tuple[float, float]: the corresponding x, y coordinates on the
                screen.
        """

        return (
            x * self._scale + self._offset_x,
            y * self._scale + self._offset_y
        )

    def show_view(self) -> None:

        pygame.init()

        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h

        WIDTH = screen_width * 2 // 3
        HEIGHT = screen_height * 2 // 3

        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        screen.fill("white")

        running = True

        self._paint_map(screen)
        self._draw_pacman(screen)
        self._draw_ghosts(screen)
        pygame.display.flip()

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        running = False

        pygame.quit()

    def _paint_map(self, screen: pygame.Surface) -> None:

        map = self._level.getMaze()._map

        for y in range(len(map)):

            for x in range(len(map[y])):

                if not map[y][x]._is_42:
                    self._draw_maze(y, x, screen, map)
                    self._draw_pellets(y, x, screen)
                else:
                    self._draw_42(y, x, screen)

    def _draw_maze(self, y: int, x: int, screen: pygame.Surface,
                   map: list[list[Cell]]) -> None:

        if map[y][x]._E == 1:
            source = (x+1, y)
            target = (x + 1, y + 1)

            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                4)

        if map[y][x]._W == 1:
            source = (x, y)
            target = (x, y + 1)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                4)

        if map[y][x]._N == 1:
            source = (x, y)
            target = (x + 1, y)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                4)

        if map[y][x]._S == 1:
            source = (x, y + 1)
            target = (x + 1, y + 1)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                4)

    def _draw_pellets(self, y: int, x: int, screen: pygame.Surface) -> None:

        radius = 3
        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        circle_x = (source_x + target_x) / 2
        circle_y = (source_y + target_y) / 2

        pygame.draw.circle(screen, "black", (circle_x, circle_y), radius)

    def _draw_pacman(self, screen: pygame.Surface) -> None:

        radius = 14
        x, y = self._level.getPacman().getCoords()
        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        circle_x = (source_x + target_x) / 2
        circle_y = (source_y + target_y) / 2

        pygame.draw.circle(screen, "yellow", (circle_x, circle_y), radius)

    def _draw_ghosts(self, screen: pygame.Surface) -> None:

        radius = 14
        for ghost in self._level.getGhosts():
            x, y = ghost.getCoords()
            source = (x, y)
            target = (x + 1, y + 1)

            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)

            circle_x = (source_x + target_x) / 2
            circle_y = (source_y + target_y) / 2

            pygame.draw.circle(screen, ghost.getColor().value,
                               (circle_x, circle_y), radius)

    def _draw_42(self, y: int, x: int, screen: pygame.Surface) -> None:

        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        width = target_x - source_x
        height = target_y - source_y
        pygame.draw.rect(screen, "black", (source_x, source_y, width, height))
