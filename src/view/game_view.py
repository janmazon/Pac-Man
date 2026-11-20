import pygame
from src.models.level import Level
from src.models.cell import Cell


class GameView:
    """Renders a level (maze, pellets, pacman, ghosts) on a surface."""

    _MARGIN: int = 150
    _FRAME_SIZE: int = 512

    def __init__(self, p_level: Level) -> None:
        self._level = p_level
        self._scale: int = 40
        self._offset_x: int = 0
        self._offset_y: int = 0

        # frames originales (512x512) y escalados al tamaño actual
        self._pacman_src: list[pygame.Surface] = []
        self._ghost_src: dict[str, list[pygame.Surface]] = {}
        self._pacman_frames: list[pygame.Surface] = []
        self._ghost_frames: dict[str, list[pygame.Surface]] = {}

        self._bg_original: pygame.Surface | None = None
        self._bg_scaled: pygame.Surface | None = None
        self._assets_loaded: bool = False

    # ---------- helpers de escala ----------

    @property
    def _wall_width(self) -> int:
        return max(1, self._scale // 10)

    @property
    def _pellet_radius(self) -> int:
        return max(1, self._scale // 12)

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """Convert maze coordinates into screen coordinates."""
        return (
            x * self._scale + self._offset_x,
            y * self._scale + self._offset_y,
        )

    # ---------- API pública (la usa GameScreen) ----------

    def load_assets(self) -> None:
        """Load sprites and background from disk (once)."""
        if self._assets_loaded:
            return

        self._pacman_src = self._load_sheet("assets/pacman.png", 3)

        ghost_files = {
            "RED": "assets/blinky.png",
            "PINK": "assets/pinky.png",
            "CYAN": "assets/inky.png",
            "ORANGE": "assets/clyde.png",
        }
        for color_name, path in ghost_files.items():
            self._ghost_src[color_name] = self._load_sheet(path, 4)

        try:
            self._bg_original = pygame.image.load(
                "assets/game_background3.png"
            ).convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading background: {e}")
            self._bg_original = None

        self._assets_loaded = True

    def resize(self, win_w: int, win_h: int) -> None:
        """Recompute layout and rescale every cached image."""
        self._update_layout(win_w, win_h)
        self._rescale_assets(win_w, win_h)

    def draw(self, screen: pygame.Surface) -> None:
        if self._bg_scaled is not None:
            screen.blit(self._bg_scaled, (0, 0))
        else:
            screen.fill("white")
        self._draw_map(screen)
        self._draw_pacman(screen)
        self._draw_ghosts(screen)

    # ---------- assets ----------

    def _load_sheet(self, path: str, n_frames: int) -> list[pygame.Surface]:
        """Slice a horizontal sprite sheet into n_frames surfaces."""
        frames: list[pygame.Surface] = []
        size = self._FRAME_SIZE
        try:
            sheet = pygame.image.load(path).convert_alpha()
            for i in range(n_frames):
                frame = pygame.Surface((size, size), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (i * size, 0, size, size))
                frames.append(frame)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading {path}: {e}")
        return frames

    def _rescale_assets(self, win_w: int, win_h: int) -> None:
        size = (self._scale, self._scale)
        self._pacman_frames = [
            pygame.transform.smoothscale(f, size) for f in self._pacman_src
        ]
        self._ghost_frames = {
            name: [pygame.transform.smoothscale(f, size) for f in frames]
            for name, frames in self._ghost_src.items()
        }
        if self._bg_original is not None:
            self._bg_scaled = pygame.transform.smoothscale(
                self._bg_original, (win_w, win_h)
            )

    # ---------- layout ----------

    def _update_layout(self, win_w: int, win_h: int) -> None:
        maze_map = self._level.getMaze()._map
        rows = len(maze_map)
        cols = len(maze_map[0])

        avail_w = win_w - 2 * self._MARGIN
        avail_h = win_h - 2 * self._MARGIN

        self._scale = max(1, min(avail_w // cols, avail_h // rows))
        self._offset_x = (win_w - self._scale * cols) // 2
        self._offset_y = (win_h - self._scale * rows) // 2

    # ---------- entidades ----------

    def _draw_pacman(self, screen: pygame.Surface) -> None:
        x, y = self._level.getPacman().getCoords()
        sx, sy = self.world_to_screen(x, y)

        if self._pacman_frames:
            screen.blit(self._pacman_frames[0], (sx, sy))
        else:
            half = self._scale / 2
            pygame.draw.circle(
                screen, "yellow", (sx + half, sy + half), self._scale * 0.4
            )

    def _draw_ghosts(self, screen: pygame.Surface) -> None:
        for ghost in self._level.getGhosts():
            x, y = ghost.getCoords()
            sx, sy = self.world_to_screen(x, y)

            color = ghost.getColor()
            frames = self._ghost_frames.get(color.name)

            if frames:
                screen.blit(frames[2], (sx, sy))  # 2 = derecha, de momento
            else:
                half = self._scale / 2
                pygame.draw.circle(
                    screen, color.value, (sx + half, sy + half),
                    self._scale * 0.4,
                )

    # ---------- laberinto ----------

    def _draw_map(self, screen: pygame.Surface) -> None:
        maze_map = self._level.getMaze()._map

        for y in range(len(maze_map)):
            for x in range(len(maze_map[y])):
                if not maze_map[y][x]._is_42:
                    self._draw_maze(y, x, screen, maze_map)
                    self._draw_pellets(y, x, screen)
                else:
                    self._draw_42(y, x, screen)

    def _draw_wall(self, screen: pygame.Surface,
                   source: tuple[int, int],
                   target: tuple[int, int]) -> None:
        """Draw one wall segment between two maze corner points."""
        pygame.draw.line(
            screen, "orange",
            self.world_to_screen(*source),
            self.world_to_screen(*target),
            self._wall_width,
        )

    def _draw_maze(self, y: int, x: int, screen: pygame.Surface,
                   maze_map: list[list[Cell]]) -> None:
        cell = maze_map[y][x]

        if cell._E == 1:
            self._draw_wall(screen, (x + 1, y), (x + 1, y + 1))
        if cell._W == 1:
            self._draw_wall(screen, (x, y), (x, y + 1))
        if cell._N == 1:
            self._draw_wall(screen, (x, y), (x + 1, y))
        if cell._S == 1:
            self._draw_wall(screen, (x, y + 1), (x + 1, y + 1))

    def _draw_pellets(self, y: int, x: int, screen: pygame.Surface) -> None:
        pellet_x, pellet_y = self.world_to_screen(x + 0.5, y + 0.5)
        pygame.draw.circle(
            screen, "white", (pellet_x, pellet_y),
            self._pellet_radius)

    def _draw_42(self, y: int, x: int, screen: pygame.Surface) -> None:
        sx, sy = self.world_to_screen(x, y)
        pygame.draw.rect(screen, "black", (sx, sy, self._scale, self._scale))
