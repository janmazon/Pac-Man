import pygame

from .screen_manager import ScreenManager
from .main_menu_screen import MainMenuScreen
from src.models import Highscore


class App:
    """Owns the window and runs the main loop."""

    _FPS: int = 60

    def __init__(self) -> None:
        self._running: bool = False

    def run(self, highscores: list[Highscore]) -> None:
        pygame.init()
        try:
            info = pygame.display.Info()
            size = (info.current_w * 2 // 3, info.current_h * 2 // 3)
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            pygame.display.set_caption("Pac-Man")
            clock = pygame.time.Clock()

            manager = ScreenManager(highscores)
            manager.switch(MainMenuScreen(manager))

            self._running = True
            while self._running and manager.current is not None:
                dt = clock.tick(self._FPS) / 1000

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    else:
                        manager.handle_event(event)

                manager.update(dt)
                manager.draw(screen)
                pygame.display.flip()
        finally:
            pygame.quit()
