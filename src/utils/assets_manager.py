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
