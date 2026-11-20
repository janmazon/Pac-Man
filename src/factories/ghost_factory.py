from src.models.ghosts import Ghost, Personality, Inky, Blinky, Pinky, Clyde


class GhostFactory:
    """Creates ghosts by personality and places them in maze corners."""

    _REGISTRY: dict[Personality, type[Ghost]] = {
        Personality.BLINKY: Blinky,
        Personality.PINKY: Pinky,
        Personality.INKY: Inky,
        Personality.CLYDE: Clyde,
    }

    @classmethod
    def create(cls, personality: Personality,
               coords: tuple[int, int]) -> Ghost:
        """Create a single ghost.

        Raises:
            ValueError: if the personality has no registered class.
        """
        try:
            return cls._REGISTRY[personality](coords)
        except KeyError:
            raise ValueError(
                f"No ghost registered for {personality}"
            ) from None

    @classmethod
    def create_all(cls, cols: int, rows: int) -> list[Ghost]:
        """Create one ghost per personality, one in each maze corner."""
        corners: dict[Personality, tuple[int, int]] = {
            Personality.BLINKY: (0, 0),
            Personality.PINKY: (cols, 0),
            Personality.INKY: (0, rows),
            Personality.CLYDE: (cols, rows),
        }
        return [cls.create(p, corners[p]) for p in Personality]
