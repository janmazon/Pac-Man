import pygame


class PauseView:

    def __init__(self, options: list[str]) -> None:
        self._options = options
        self._size: tuple[int, int] = (0, 0)
        self._overlay: pygame.Surface | None = None
        self._title_font: pygame.font.Font | None = None
        self._option_font: pygame.font.Font | None = None

    def resize(self, width: int, height: int) -> None:
        """Rescale cached images (and later fonts/layout) to the window."""
        self._size = (width, height)
        self._overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 150))
        # self._overlay.fill((0, 0, 0, 175))
        self._title_font = pygame.font.Font(None, height // 8)
        self._option_font = pygame.font.Font(None, height // 16)

    def draw(self, screen: pygame.Surface, selected: int) -> None:
        if (self._overlay is None or self._title_font is None
                or self._option_font is None):
            return

        self._draw_menu(screen, selected)

    def _draw_menu(self, screen: pygame.Surface, selected: int) -> None:

        screen.blit(self._overlay, (0, 0))

        w, h = self._size
        if self._title_font is None or self._option_font is None:
            return

        title = self._title_font.render("PAUSA", True, "yellow")
        screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        for i, label in enumerate(self._options):
            color = "yellow" if i == selected else "white"
            surf = self._option_font.render(label, True, color)
            y = h // 2 + i * (h // 10)
            screen.blit(surf, surf.get_rect(center=(w // 2, y)))
