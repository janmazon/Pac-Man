import pygame
from src.models import Highscore
from src.utils import AssetManager


class HighscoreView:

    def __init__(self, highscores: list[Highscore]) -> None:
        self._highscores = highscores
        self._bg_original: pygame.Surface | None = None
        self._bg_scaled: pygame.Surface | None = None
        self._size: tuple[int, int] = (0, 0)
        self._title_font: pygame.font.Font | None = None
        self._option_font: pygame.font.Font | None = None

        self._title_src: pygame.Surface | None = None
        self._title_img: pygame.Surface | None = None
        self._assets_loaded: bool = False

    def load_assets(self) -> None:
        """Load menu images (needs the display to be created)."""
        if self._assets_loaded:
            return

        self._bg_original = AssetManager.get_image(
            "assets/background.png", alpha=False)
        self._title_src = AssetManager.get_image(
            "assets/highscores.png", alpha=True)

        self._assets_loaded = True

    def resize(self, width: int, height: int) -> None:
        """Rescale cached images (and later fonts/layout) to the window."""
        self._size = (width, height)
        self._title_font = pygame.font.Font(None, height // 8)
        self._option_font = pygame.font.Font(None, height // 16)
        if self._bg_original is not None:
            self._bg_scaled = pygame.transform.smoothscale(
                self._bg_original, (width, height)
            )
        if self._title_src is not None:
            orig_w, orig_h = self._title_src.get_size()
            target_h = max(1, int(height * 0.26))
            target_w = max(1, int(target_h * (orig_w / orig_h)))
            self._title_img = pygame.transform.smoothscale(
                self._title_src, (target_w, target_h)
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

        if self._title_img is not None:
            screen.blit(
                self._title_img,
                self._title_img.get_rect(center=(w // 2, h // 5)),
            )
        else:
            title = self._title_font.render("Highscores", True, "yellow")
            screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        for i in range(10):
            if i < len(self._highscores):
                entry = self._highscores[i]
                text = f"{i + 1}. {entry.name} - {entry.score}"
            else:
                text = f"{i + 1}."

            if i < 5:
                x = int(w * 0.20)
            else:
                x = int(w * 0.56)

            y = int(h * 0.44) + (i % 5) * int(h * 0.09)

            surf = self._option_font.render(text, True, "white")
            screen.blit(surf, surf.get_rect(midleft=(x, y)))
