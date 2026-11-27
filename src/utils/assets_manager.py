import pygame
import sys


class AssetManager:
    _images: dict[str, pygame.Surface] = {}
    _sheets: dict[tuple[str, int], list[pygame.Surface]] = {}

    @classmethod
    def get_image(cls, path: str, alpha: bool = True) -> pygame.Surface:
        if path in cls._images:
            return cls._images[path]

        try:
            raw = pygame.image.load(path)
            surface = raw.convert_alpha() if alpha else raw.convert()
            cls._images[path] = surface
            return surface

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading {path}: {e}")
            sys.exit(1)

    @classmethod
    def get_sheet(cls, path: str, n_frames: int) -> list[pygame.Surface]:
        if (path, n_frames) in cls._sheets:
            return cls._sheets[(path, n_frames)]

        frames: list[pygame.Surface] = []
        try:
            sheet = pygame.image.load(path).convert_alpha()
            frame_w = sheet.get_width() // n_frames
            frame_h = sheet.get_height()

            for i in range(n_frames):
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (i * frame_w, 0, frame_w, frame_h))
                frames.append(frame)

            cls._sheets[(path, n_frames)] = frames
            return frames

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading {path}: {e}")
            sys.exit(1)

    @classmethod
    def preload_all(cls) -> None:
        images: list[tuple[str, bool]] = [
            ("assets/background.png", False),
            ("assets/game_background.png", False),
            ("assets/title.png", True),
            ("assets/highscores.png", True),
            ("assets/paused.png", True),
            ("assets/pellet.png", True),
            ("assets/superpellet.png", True),
            ("assets/hud_frame.png", True),
            ("assets/ready.png", True),
            # ("assets/defeat.png", True),
            # ("assets/instructions.png", True),
            ("assets/level_complete.png", True),
            # ("assets/victory.png", True),
        ]
        for path, alpha in images:
            cls.get_image(path, alpha)

        sheets: list[tuple[str, int]] = [
            ("assets/pacman.png", 4),
            ("assets/blinky.png", 4),
            ("assets/pinky.png", 4),
            ("assets/inky.png", 4),
            ("assets/clyde.png", 4),
            ("assets/hud_icons.png", 4),
            # ("assets/ghosts_states.png", 4),
        ]
        for path, n_frames in sheets:
            cls.get_sheet(path, n_frames)
