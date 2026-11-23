from .screen import Screen
from .screen_manager import ScreenManager
from src.view import PauseView
import pygame
from enum import Enum


class PauseOptions(Enum):
    CONTINUE = "Continue"
    CHEATS = "Cheats"
    MAIN_MENU = "Main Menu"
    EXIT = "Exit"


class PauseScreen(Screen):

    _OPTIONS: list[PauseOptions] = [
        PauseOptions.CONTINUE, PauseOptions.CHEATS, PauseOptions.MAIN_MENU,
        PauseOptions.EXIT]

    def __init__(self, manager: "ScreenManager") -> None:
        super().__init__(manager)
        self._view = PauseView([opt.value for opt in self._OPTIONS])
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

        if event.key in (pygame.K_UP, pygame.K_w):
            self._selected = (self._selected - 1) % len(self._OPTIONS)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self._selected = (self._selected + 1) % len(self._OPTIONS)
        elif event.key == pygame.K_RETURN:
            self._activate(self._selected)

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

    def _activate(self, index: int) -> None:
        from .main_menu_screen import MainMenuScreen
        """Run the action of the chosen option."""
        option = self._OPTIONS[index]
        if option == PauseOptions.CONTINUE:
            self._manager.pop()
        elif option == PauseOptions.CHEATS:
            ...  # self._manager.push(HighscoresScreen(self._manager))
            print("Get Cheated")
        elif option == PauseOptions.MAIN_MENU:
            menu = MainMenuScreen(self._manager)
            self._manager.switch(menu)
        elif option == PauseOptions.EXIT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, surface: pygame.Surface) -> None:
        self._view.draw(surface, self._selected)
