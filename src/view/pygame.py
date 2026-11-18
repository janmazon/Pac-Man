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
        self._pacman_frames: list[pygame.Surface] = []
        self._assets_loaded: bool = False

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

        self._load_assets()

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

    """ def _draw_pacman(self, screen: pygame.Surface) -> None:

        radius = self._pellet_radius * 3
        x, y = self._level.getPacman().getCoords()
        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        circle_x = (source_x + target_x) / 2
        circle_y = (source_y + target_y) / 2

        pygame.draw.circle(screen, "yellow", (circle_x, circle_y), radius) """

    def _draw_pacman(self, screen: pygame.Surface) -> None:
        coords = self._level.getPacman().getCoords()
        print("Coordenadas de Pac-Man:", coords)  # <- Comprueba en la terminal que cambian o existen
        
        x, y = coords
        source_x, source_y = self.world_to_screen(x, y)

        if self._pacman_frames:
            screen.blit(self._pacman_frames[0], (source_x, source_y))
        else:
            # Dibuja un círculo rojo temporal si entra aquí es que la imagen falló
            pygame.draw.circle(screen, "yellow", (source_x + 20, source_y + 20), 15)

    def _draw_ghosts(self, screen: pygame.Surface) -> None:
        for ghost in self._level.getGhosts():
            x, y = ghost.getCoords()
            source_x, source_y = self.world_to_screen(x, y)

            # Obtener el color del fantasma para saber qué sprite usar
            color_enum = ghost.getColor()
            color_name = getattr(color_enum, "name", "RED") # Asegura compatibilidad con tu clase Color

            if hasattr(self, "_ghost_frames") and color_name in self._ghost_frames and self._ghost_frames[color_name]:
                # Índice 2 por defecto (ej. mirando a la derecha). Puedes cambiarlo según la dirección del fantasma
                frame = self._ghost_frames[color_name][2]
                screen.blit(frame, (source_x, source_y))
            else:
                # Fallback al círculo original si falla la imagen
                radius = self._pellet_radius * 3
                target = (x + 1, y + 1)
                target_x, target_y = self.world_to_screen(*target)
                circle_x = (source_x + target_x) / 2
                circle_y = (source_y + target_y) / 2
                pygame.draw.circle(screen, ghost.getColor().value, (circle_x, circle_y), radius)

    def _draw_42(self, y: int, x: int, screen: pygame.Surface) -> None:

        source = (x, y)
        target = (x + 1, y + 1)

        source_x, source_y = self.world_to_screen(*source)
        target_x, target_y = self.world_to_screen(*target)

        width = target_x - source_x
        height = target_y - source_y
        pygame.draw.rect(screen, "black", (source_x, source_y, width, height))

    def _load_assets(self) -> None:
        """Carga los sprites de Pac-Man y los fantasmas de forma segura."""
        if self._assets_loaded:
            return
        
        target_size = int(self._scale)
        p_frame_w = 592
        p_frame_h = 592
        g_frame_w = 512
        g_frame_h = 512

        # 1. Cargar Pac-Man
        try:
            sheet_p = pygame.image.load("assets/pacman.png").convert_alpha()
            sheet_p.set_colorkey((0, 0, 0))
            self._pacman_frames = []
            for i in range(3):
                frame = pygame.Surface((p_frame_w, p_frame_h), pygame.SRCALPHA)
                frame.blit(sheet_p, (0, 0), (i * p_frame_w, 0, p_frame_w, p_frame_h))
                self._pacman_frames.append(pygame.transform.scale(frame, (target_size, target_size)))
        except Exception as e:
            print(f"Error cargando Pac-Man: {e}")
            self._pacman_frames = []

        # 2. Cargar Fantasmas (Blinky, Pinky, Inky, Clyde) -> 128x32 con 4 frames (Arriba, Abajo, Derecha, Izquierda)
        ghost_files = {
            "RED": "assets/blinky.png",
            "PINK": "assets/pinky.png",
            "CYAN": "assets/inky.png",
            "ORANGE": "assets/clyde.png"
        }
        
        self._ghost_frames = {}
        for color_name, path in ghost_files.items():
            try:
                sheet_g = pygame.image.load(path).convert_alpha()
                sheet_g.set_colorkey((0, 0, 0))
                frames = []
                for i in range(4): # 4 direcciones
                    frame = pygame.Surface((g_frame_w, g_frame_h), pygame.SRCALPHA)
                    frame.blit(sheet_g, (0, 0), (i * g_frame_w, 0, g_frame_w, g_frame_h))
                    frames.append(pygame.transform.scale(frame, (target_size, target_size)))
                self._ghost_frames[color_name] = frames
            except Exception as e:
                print(f"Error cargando fantasma {color_name}: {e}")
                self._ghost_frames[color_name] = []

        self._assets_loaded = True