from .screen import Screen
from .screen_manager import ScreenManager
from src.models import Level
from src.view import LevelView
import pygame


class GameScreen(Screen):

    def __init__(self, manager: "ScreenManager", level: Level) -> None:
        super().__init__(manager)
        self._level = level
        self._view = LevelView(level)

    def on_enter(self) -> None:
        self._view.load_assets()          # necesita la ventana ya creada
        surface = pygame.display.get_surface()
        if surface is not None:
            self._view.resize(*surface.get_size())

    def on_resize(self, width: int, height: int) -> None:
        self._view.resize(width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # self._manager.push(PauseScreen(self._manager))
            print("Game paused")

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
