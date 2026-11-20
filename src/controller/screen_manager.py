from .screen import Screen
import pygame


class ScreenManager:
    """Keeps a stack of screens; only the top one receives input/updates."""

    def __init__(self) -> None:
        self._stack: list[Screen] = []

    def push(self, screen: Screen) -> None:
        """Put a screen on top (e.g. pause over the game)."""
        self._stack.append(screen)
        screen.on_enter()

    def pop(self) -> None:
        """Remove the top screen and go back to the one below."""
        if self._stack:
            self._stack.pop().on_exit()

    def switch(self, screen: Screen) -> None:
        """Replace the whole stack with a new screen."""
        while self._stack:
            self._stack.pop().on_exit()
        self.push(screen)

    @property
    def current(self) -> Screen | None:
        return self._stack[-1] if self._stack else None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.VIDEORESIZE:
            for screen in self._stack:
                screen.on_resize(event.w, event.h)
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float) -> None:
        if self.current:               # solo la de arriba se actualiza
            self.current.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        for screen in self._stack:     # todas, de abajo a arriba
            screen.draw(surface)
