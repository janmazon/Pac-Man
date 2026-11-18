import pygame
from src.models.level import Level
from src.models.cell import Cell


class Pygame:

    _MARGIN: int = 40
    _scale: float = 40
    _offset_x: float = 50
    _offset_y: float = 50
    _level: Level

    def __init__(self, p_level: Level):
        self._level = p_level

    @property
    def _wall_width(self) -> int:
        return max(1, self._scale // 10)

    @property
    def _pellet_radius(self) -> int:
        return max(1, self._scale // 12)

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

    def _update_layout(self, win_w: int, win_h: int) -> None:
        """Compute scale and offsets so the maze fits and is centered."""
        maze_map = self._level.getMaze()._map
        rows = len(maze_map)
        cols = len(maze_map[0])

        avail_w = win_w - 2 * self._MARGIN
        avail_h = win_h - 2 * self._MARGIN

        self._scale = max(1, min(avail_w // cols, avail_h // rows))
        self._offset_x = (win_w - self._scale * cols) // 2
        self._offset_y = (win_h - self._scale * rows) // 2

    def show_view(self) -> None:

        pygame.init()

        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h

        WIDTH = screen_width * 2 // 3
        HEIGHT = screen_height * 2 // 3

        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        self._update_layout(*screen.get_size())
        clock = pygame.time.Clock()
        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        running = False

                elif event.type == pygame.VIDEORESIZE:
                    self._update_layout(*screen.get_size())

            screen.fill("white")
            clock.tick(60)
            self._paint_map(screen)
            self._draw_pacman(screen)
            self._draw_ghosts(screen)
            pygame.display.flip()

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
                self._wall_width)

        if map[y][x]._W == 1:
            source = (x, y)
            target = (x, y + 1)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                self._wall_width)

        if map[y][x]._N == 1:
            source = (x, y)
            target = (x + 1, y)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                self._wall_width)

        if map[y][x]._S == 1:
            source = (x, y + 1)
            target = (x + 1, y + 1)
            source_x, source_y = self.world_to_screen(*source)
            target_x, target_y = self.world_to_screen(*target)
            pygame.draw.line(
                screen, "black", (source_x, source_y),
                (target_x, target_y),
                self._wall_width)

    def _draw_pellets(self, y: int, x: int, screen: pygame.Surface) -> None:

        radius = self._pellet_radius
        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        circle_x = (source_x + target_x) / 2
        circle_y = (source_y + target_y) / 2

        pygame.draw.circle(screen, "black", (circle_x, circle_y), radius)

    def _draw_pacman(self, screen: pygame.Surface) -> None:

        radius = self._pellet_radius * 3
        x, y = self._level.getPacman().getCoords()
        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        circle_x = (source_x + target_x) / 2
        circle_y = (source_y + target_y) / 2

        pygame.draw.circle(screen, "yellow", (circle_x, circle_y), radius)

    def _draw_ghosts(self, screen: pygame.Surface) -> None:

        radius = self._pellet_radius * 3
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
