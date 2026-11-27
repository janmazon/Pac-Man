from enum import Enum

import pygame

from .screen import Screen
from .screen_manager import ScreenManager
from src.view import GameOverView


class GameOverFields(Enum):
    NAME = "Name"
    CONTINUE = "Continue"


class GameOverScreen(Screen):

    _FIELDS: list[GameOverFields] = [
        GameOverFields.NAME, GameOverFields.CONTINUE]

    def __init__(self, manager: "ScreenManager", score: int) -> None:
        super().__init__(manager)
        self._score = score
        self._name: str = ""                 # se rellenará más adelante
        self._selected: int = 0
        self._view = GameOverView(score, GameOverFields.CONTINUE.value)

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

        # Solo flechas: cuando se escriba el nombre, W y S serán letras
        if event.key == pygame.K_UP:
            self._selected = (self._selected - 1) % len(self._FIELDS)
        elif event.key == pygame.K_DOWN:
            self._selected = (self._selected + 1) % len(self._FIELDS)
        elif event.key == pygame.K_RETURN:
            self._activate(self._FIELDS[self._selected])

        elif self._FIELDS[self._selected] == GameOverFields.NAME:
            if event.key == pygame.K_BACKSPACE:
                self._remove_character()
            else:
                self._write_character(event.unicode)

    def _write_character(self, text: str) -> None:

        if len(self._name + text) <= 10:
            if text.isalnum() or (text == " " and len(self._name) > 0):
                self._name += text

    def _remove_character(self) -> None:

        self._name = self._name[:-1] if self._name else ""

    def _activate(self, field: GameOverFields) -> None:
        from .main_menu_screen import MainMenuScreen

        if field == GameOverFields.CONTINUE:
            self._manager.switch(MainMenuScreen(self._manager))
        # NAME: aquí irá la edición del texto

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self._view.draw(surface, self._selected, self._name)
