import pygame
from src.models.level import Level
from src.models.ghosts import Direction
from src.models.cell import PelletType


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
        self._walls_surface: pygame.Surface | None = None
        self._assets_loaded: bool = False

        self._pellet_src: pygame.Surface | None = None
        self._superpellet_src: pygame.Surface | None = None
        self._pellet_img: pygame.Surface | None = None
        self._superpellet_img: pygame.Surface | None = None

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

        self._pacman_src = self._load_sheet("assets/pacman.png", 4)

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
                "assets/game_background.png"
            ).convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading background: {e}")
            self._bg_original = None

        try:
            self._pellet_src = pygame.image.load(
                "assets/pellet.png"
            ).convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading pellet: {e}")
            self._pellet_src = None

        try:
            self._superpellet_src = pygame.image.load(
                "assets/superpellet.png"
            ).convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading superpellet: {e}")
            self._superpellet_src = None

        self._assets_loaded = True

    def resize(self, win_w: int, win_h: int) -> None:
        """Recompute layout and rescale every cached image."""
        self._update_layout(win_w, win_h)
        self._rescale_assets(win_w, win_h)
        self._build_walls_surface(win_w, win_h)

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
        entity_px = max(1, int(self._scale * 0.7))
        size = (entity_px, entity_px)
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
        if self._pellet_src is not None:
            p_size = max(1, int(self._scale * 0.4))
            self._pellet_img = pygame.transform.smoothscale(
                self._pellet_src, (p_size, p_size)
            )
        if self._superpellet_src is not None:
            sp_size = max(1, int(self._scale * 0.70))
            self._superpellet_img = pygame.transform.smoothscale(
                self._superpellet_src, (sp_size, sp_size)
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
        cx, cy = self.world_to_screen(x + 0.5, y + 0.5)

        if len(self._pacman_frames) > 2:
            frame = self._pacman_frames[2]
            screen.blit(frame, frame.get_rect(center=(cx, cy)))
        else:
            pygame.draw.circle(
                screen, "yellow", (cx, cy), self._scale * 0.35
            )

    def _draw_ghosts(self, screen: pygame.Surface) -> None:
        dir_index = {
            Direction.UP: 0,
            Direction.DOWN: 1,
            Direction.LEFT: 2,
            Direction.RIGHT: 3,
        }
        for ghost in self._level.getGhosts():
            x, y = ghost.getCoords()
            cx, cy = self.world_to_screen(x + 0.5, y + 0.5)

            color = ghost.getColor()
            frames = self._ghost_frames.get(color.name)
            idx = dir_index[ghost.getDirection()]

            if frames and len(frames) > idx:
                frame = frames[idx]
                screen.blit(frame, frame.get_rect(center=(cx, cy)))
            else:
                pygame.draw.circle(
                    screen, color.value, (cx, cy), self._scale * 0.35
                )

    # ---------- laberinto ----------

    def _draw_map(self, screen: pygame.Surface) -> None:
        if self._walls_surface is not None:
            screen.blit(self._walls_surface, (0, 0))

        maze_map = self._level.getMaze()._map
        for y in range(len(maze_map)):
            for x in range(len(maze_map[y])):
                if not maze_map[y][x]._is_42:
                    self._draw_pellets(y, x, screen)
                else:
                    self._draw_42(y, x, screen)

    def _draw_wall(self, surface: pygame.Surface,
                   source: tuple[int, int],
                   target: tuple[int, int]) -> None:
        """Draw one wall segment."""

        start = self.world_to_screen(*source)
        end = self.world_to_screen(*target)

        pygame.draw.line(
            surface,
            (255, 170, 30),
            start,
            end,
            self._wall_width
        )

        # Redondeamos los extremos para conectar los segmentos
        radius = max(1, self._wall_width // 2)

        pygame.draw.circle(surface, (255, 170, 30), start, radius)
        pygame.draw.circle(surface, (255, 170, 30), end, radius)

    def _build_walls_surface(self, width: int, height: int) -> None:
        """Pre-render all maze walls with a soft lava glow."""
        maze_map = self._level.getMaze()._map
        result = pygame.Surface((width, height), pygame.SRCALPHA)
        maze_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for y in range(len(maze_map)):
            for x in range(len(maze_map[y])):
                cell = maze_map[y][x]
                if cell._is_42:
                    continue

                walls = []
                if cell._E == 1:
                    walls.append(((x + 1, y), (x + 1, y + 1)))
                if cell._W == 1:
                    walls.append(((x, y), (x, y + 1)))
                if cell._N == 1:
                    walls.append(((x, y), (x + 1, y)))
                if cell._S == 1:
                    walls.append(((x, y + 1), (x + 1, y + 1)))

                for source, target in walls:
                    self._draw_wall(maze_surface, source, target)

                    start = self.world_to_screen(*source)
                    end = self.world_to_screen(*target)
                    glow_width = self._wall_width * 4
                    glow_radius = max(1, glow_width // 2)

                    pygame.draw.line(
                        glow_surface, (255, 100, 0, 90),
                        start, end, glow_width
                    )
                    pygame.draw.circle(
                        glow_surface, (255, 100, 0, 90), start, glow_radius
                    )
                    pygame.draw.circle(
                        glow_surface, (255, 100, 0, 90), end, glow_radius
                    )

        small_size = (max(1, width // 6), max(1, height // 6))
        glow_small = pygame.transform.smoothscale(glow_surface, small_size)
        glow_blurred = pygame.transform.smoothscale(
            glow_small, (width, height)
        )

        result.blit(glow_blurred, (0, 0))
        result.blit(maze_surface, (0, 0))
        self._walls_surface = result

    def _draw_pellets(self, y: int, x: int, screen: pygame.Surface) -> None:
        pellet = self._level.getMaze().getCell(x, y).getPellet()
        if pellet == PelletType.NONE:
            return

        if pellet == PelletType.SUPER and any(
            ghost.getCoords() == (x, y)
            for ghost in self._level.getGhosts()
        ):
            return

        pellet_x, pellet_y = self.world_to_screen(x + 0.5, y + 0.5)
        img = (
            self._superpellet_img
            if pellet == PelletType.SUPER
            else self._pellet_img
        )

        if img is not None:
            screen.blit(img, img.get_rect(center=(pellet_x, pellet_y)))
        else:
            radius = (
                self._pellet_radius * 2
                if pellet == PelletType.SUPER
                else self._pellet_radius
            )
            pygame.draw.circle(screen, "white", (pellet_x, pellet_y), radius)

    def _draw_42(self, y: int, x: int, screen: pygame.Surface) -> None:
        sx, sy = self.world_to_screen(x, y)
        pygame.draw.rect(screen, "orange", (sx, sy, self._scale, self._scale))
