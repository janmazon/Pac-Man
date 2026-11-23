import pygame


class PauseView:

    _FRAME_SIZE: int = 512

    def __init__(self, options: list[str]) -> None:
        self._options = options
        self._size: tuple[int, int] = (0, 0)
        self._overlay: pygame.Surface | None = None
        self._title_font: pygame.font.Font | None = None
        self._option_font: pygame.font.Font | None = None
        self._pacman_src: list[pygame.Surface] = []
        self._scale: int = 40

        self._assets_loaded: bool = False

        self._paused_src: pygame.Surface | None = None
        self._paused_img: pygame.Surface | None = None
        self._assets_loaded: bool = False

    def load_assets(self) -> None:
        """Load pause banner and menu icons from disk (once)."""
        if self._assets_loaded:
            return

        try:
            self._paused_src = pygame.image.load(
                "assets/paused.png"
            ).convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading paused banner: {e}")
            self._paused_src = None

        self._assets_loaded = True

    def resize(self, width: int, height: int) -> None:
        """Rescale cached images (and later fonts/layout) to the window."""
        self._size = (width, height)
        self._overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 150))
        self._title_font = pygame.font.Font(None, height // 8)
        self._option_font = pygame.font.Font(None, height // 16)
        self._rescale_assets()

        if self._paused_src is not None:
            orig_w, orig_h = self._paused_src.get_size()
            target_h = max(1, int(height * 0.26))
            target_w = max(1, int(target_h * (orig_w / orig_h)))
            self._paused_img = pygame.transform.smoothscale(
                self._paused_src, (target_w, target_h)
            )

    def draw(self, screen: pygame.Surface, selected: int) -> None:
        if (self._overlay is None or self._title_font is None
                or self._option_font is None):
            return

        self._draw_menu(screen, selected)

    def _draw_menu(self, screen: pygame.Surface, selected: int) -> None:

        if (self._overlay is None or self._title_font is None
                or self._option_font is None):
            return

        screen.blit(self._overlay, (0, 0))

        w, h = self._size
        if self._paused_img is not None:
            screen.blit(
                self._paused_img,
                self._paused_img.get_rect(center=(w // 2, h // 5)),
            )
        else:
            title = self._title_font.render("PAUSA", True, "yellow")
            screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        for i, label in enumerate(self._options):
            color = "yellow" if i == selected else "white"
            surf = self._option_font.render(label, True, color)
            y = h // 2 + i * (h // 10)
            rect = surf.get_rect(center=(w // 2, y))
            screen.blit(surf, rect)

            if i == selected:
                gap = rect.height // 2
                if self._pacman_frames:
                    sprite = self._pacman_frames[0]
                    sprite_rect = sprite.get_rect(
                        midright=(rect.left - gap, rect.centery)
                    )
                    screen.blit(sprite, sprite_rect)
                else:
                    radius = rect.height // 3
                    pygame.draw.circle(
                        screen, "yellow",
                        (rect.left - gap - radius, rect.centery), radius
                    )

    # Para añadir la imagen de Pac-Man, borrar cuando AssetManager

    def _rescale_assets(self) -> None:
        size = (self._scale, self._scale)
        self._pacman_frames = [
            pygame.transform.smoothscale(f, size) for f in self._pacman_src
        ]

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

    def load_assets(self) -> None:
        """Load sprites and background from disk (once)."""
        if self._assets_loaded:
            return

        self._pacman_src = self._load_sheet("assets/pacman.png", 3)
