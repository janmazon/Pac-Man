import pygame
from src.utils import AssetManager


class GameOverView:

    def __init__(self, score: int, continue_label: str) -> None:
        self._score = score
        self._continue_label = continue_label
        self._size: tuple[int, int] = (0, 0)
        self._title_font: pygame.font.Font | None = None
        self._text_font: pygame.font.Font | None = None
        self._bg_original: pygame.Surface | None = None
        self._bg_scaled: pygame.Surface | None = None
        self._pacman_src: list[pygame.Surface] = []
        self._pacman_frames: list[pygame.Surface] = []
        self._assets_loaded: bool = False

    def load_assets(self) -> None:
        if self._assets_loaded:
            return
        self._bg_original = AssetManager.get_image(
            "assets/background.png", alpha=False)
        self._pacman_src = AssetManager.get_sheet("assets/pacman.png", 4)
        self._assets_loaded = True

    def resize(self, width: int, height: int) -> None:
        self._size = (width, height)
        self._title_font = pygame.font.Font(None, height // 6)
        self._text_font = pygame.font.Font(None, height // 14)

        size = max(1, int(self._text_font.get_height() * 0.9))
        self._pacman_frames = [
            pygame.transform.smoothscale(f, (size, size))
            for f in self._pacman_src
        ]
        if self._bg_original is not None:
            self._bg_scaled = pygame.transform.smoothscale(
                self._bg_original, (width, height))

    def draw(self, screen: pygame.Surface, selected: int,
             name: str) -> None:
        if self._title_font is None or self._text_font is None:
            return

        if self._bg_scaled is not None:
            screen.blit(self._bg_scaled, (0, 0))
        else:
            screen.fill("black")

        w, h = self._size

        title = self._title_font.render("GAME OVER", True, "red")
        screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        score = self._text_font.render(
            f"Score: {self._score}", True, "white")
        screen.blit(score, score.get_rect(center=(w // 2, h * 3 // 8)))

        self._draw_name_box(screen, selected == 0, name)
        self._draw_continue(screen, selected == 1)

    def _draw_name_box(self, screen: pygame.Surface, active: bool,
                       name: str) -> None:
        if self._text_font is None:
            return
        w, h = self._size
        box = pygame.Rect(0, 0, w * 2 // 5, h // 10)
        box.center = (w // 2, h // 2 + h // 12)

        color = "yellow" if active else "white"
        pygame.draw.rect(screen, color, box, width=3, border_radius=8)

        text = name if name else "Enter your name"
        text_color = "white" if name else "gray"
        surf = self._text_font.render(text, True, text_color)
        screen.blit(surf, surf.get_rect(center=box.center))

    def _draw_continue(self, screen: pygame.Surface, active: bool) -> None:
        if self._text_font is None:
            return
        w, h = self._size
        color = "yellow" if active else "white"
        surf = self._text_font.render(self._continue_label, True, color)
        rect = surf.get_rect(center=(w // 2, h * 17 // 20))
        screen.blit(surf, rect)

        if active:
            gap = rect.height // 2
            if self._pacman_frames:
                sprite = self._pacman_frames[3]
                screen.blit(sprite, sprite.get_rect(
                    midright=(rect.left - gap, rect.centery)))
            else:
                radius = rect.height // 3
                pygame.draw.circle(
                    screen, "yellow",
                    (rect.left - gap - radius, rect.centery), radius)
