import pygame
from src.models import Highscore


class HighscoreView:

    def __init__(self, highscores: list[Highscore]) -> None:
        self._highscores = highscores
        self._bg_original: pygame.Surface | None = None
        self._bg_scaled: pygame.Surface | None = None
        self._size: tuple[int, int] = (0, 0)
        self._title_font: pygame.font.Font | None = None
        self._option_font: pygame.font.Font | None = None

    def load_assets(self) -> None:
        """Load menu images (needs the display to be created)."""
        try:
            self._bg_original = pygame.image.load(
                "assets/background.png"
            ).convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading menu background: {e}")
            self._bg_original = None

    def resize(self, width: int, height: int) -> None:
        """Rescale cached images (and later fonts/layout) to the window."""
        self._size = (width, height)
        self._title_font = pygame.font.Font(None, height // 8)
        self._option_font = pygame.font.Font(None, height // 16)
        if self._bg_original is not None:
            self._bg_scaled = pygame.transform.smoothscale(
                self._bg_original, (width, height)
            )

    def draw(self, screen: pygame.Surface) -> None:
        if self._bg_scaled is not None:
            screen.blit(self._bg_scaled, (0, 0))
        else:
            screen.fill("purple")

        self._draw_highscores(screen)

    def _draw_highscores(self, screen: pygame.Surface) -> None:

        w, h = self._size
        if self._title_font is None or self._option_font is None:
            return

        title = self._title_font.render("Highscores", True, "yellow")
        screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        for i, label in enumerate(self._highscores):
            text = f"{i+1}. {label.name} - {label.score}"
            surf = self._option_font.render(text, True, "white")
            y = h // 2 + i * (h // 10)
            screen.blit(surf, surf.get_rect(center=(w // 2, y)))
