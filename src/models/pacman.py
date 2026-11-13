class PacMan():

    coords: tuple[int, int]
    lives: int
    respawn_point: tuple[int, int]
    cheats: bool
    invincible: bool
    speed: float  # Tengo dudas de este

    def __init__(
            self, p_coord: tuple[int, int],
            p_lives: int, p_respawn: tuple[int, int]):
        self._coords = p_coord
        self._lives = p_lives
        self._respawn_point = p_respawn
        self._cheats = False
        self._invincible = False
        self._speed = 1.0
