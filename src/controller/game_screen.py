from .screen import Screen
from .screen_manager import ScreenManager
from src.models import Level
from src.view import GameView
import pygame
from .pause_screen import PauseScreen
from src.models import Directions
from mazegenerator import MazeGenerator


class GameScreen(Screen):

    def __init__(self, manager: "ScreenManager", level: Level) -> None:
        super().__init__(manager)
        self._level = level
        self._view = GameView(level)
        self._pacman = level.getPacman()
        self._time: float = 300.0
        self._level_num: int = 1
        self._max_levels: int = 5
        self._ready_timer: float = 3.0
        self._started: bool = False

    def on_enter(self) -> None:
        self._view.load_assets()          # necesita la ventana ya creada
        surface = pygame.display.get_surface()
        if surface is not None:
            self._view.resize(*surface.get_size())

    def on_resize(self, width: int, height: int) -> None:
        self._view.resize(width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._manager.push(PauseScreen(self._manager))

        if event.type == pygame.KEYDOWN and self._ready_timer <= 0.0:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self._pacman.setNextDirection(Directions.NORTH)
                self._started = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._pacman.setNextDirection(Directions.SOUTH)
                self._started = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self._pacman.setNextDirection(Directions.WEST)
                self._started = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self._pacman.setNextDirection(Directions.EAST)
                self._started = True

    def update(self, dt: float) -> None:

        if self._ready_timer > 0.0:
            self._ready_timer = max(0.0, self._ready_timer - dt)
            return

        if not self._started:
            return

        self._time = max(0.0, self._time - dt)
        self._pacman.update(dt, self._level)

        if not self._level.has_remaining_pellets():
            self._advance_level()

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

    def _advance_level(self) -> None:
        from .main_menu_screen import MainMenuScreen

        self._level_num += 1
        if self._level_num > self._max_levels:
            self._manager.switch(MainMenuScreen(self._manager))
            return

        saved_score = self._level.getScore()
        saved_lives = self._pacman.getLives()

        maze_gen = MazeGenerator()
        maze_gen.generate()

        self._level = Level(maze_gen.maze)
        self._level._score = saved_score
        self._pacman = self._level.getPacman()
        self._pacman._lives = saved_lives

        self._view = GameView(self._level)
        self.on_enter()
        self._time = 300.0
        self._ready_timer = 3.0
        self._started = False

    def draw(self, surface: pygame.Surface) -> None:
        self._view.draw(surface, self._time, self._level_num,
                        self._ready_timer > 0.0)
