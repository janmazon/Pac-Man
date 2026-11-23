import pygame


class PauseView:

    def __init__(self, options: list[str]) -> None:
        self._options = options
        self._size: tuple[int, int] = (0, 0)
        self._overlay: pygame.Surface | None = None
        self._title_font: pygame.font.Font | None = None
        self._option_font: pygame.font.Font | None = None

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
            screen.blit(surf, surf.get_rect(center=(w // 2, y)))
