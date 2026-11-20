from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.view import ViewController


class Screen(ABC):
    """Base class for every screen of the game."""

    def __init__(self, manager: "ViewController") -> None:
        self._manager = manager

    def on_enter(self) -> None:
        """Called when the screen becomes active."""

    def on_exit(self) -> None:
        """Called when the screen is removed."""

    def on_resize(self, width: int, height: int) -> None:
        """Called when the window changes size."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...
