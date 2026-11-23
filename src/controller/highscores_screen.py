from .screen import Screen
from .screen_manager import ScreenManager
from src.view import HighscoreView
import pygame


class HighscoresScreen(Screen):

    def __init__(self, manager: "ScreenManager") -> None:
        super().__init__(manager)
        self._view = HighscoreView(manager._highscores)
        self._selected: int = 0

    def on_enter(self) -> None:
        self._view.load_assets()
        surface = pygame.display.get_surface()
        if surface is not None:
            self._view.resize(*surface.get_size())

    def on_resize(self, width: int, height: int) -> None:
        self._view.resize(width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self._manager.pop()

    def update(self, dt: float) -> None:
        pass  # lógica del juego con dt

        # Ejemplos de la logica

        """# Temporizador del nivel (90 s)
        self._time_left -= dt
        if self._time_left <= 0:
            ...  # fin de nivel por tiempo

        # Duración del modo asustado de los fantasmas
        self._frightened_timer -= dt
        if self._frightened_timer <= 0:
            self._status = Status.CHASE

        # Respawn de un fantasma comido (5 o 10 s)
        self._respawn_timer -= dt """

    def draw(self, surface: pygame.Surface) -> None:
        self._view.draw(surface)
