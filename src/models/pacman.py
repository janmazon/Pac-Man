class PacMan():

    _coords: tuple[int, int]
    _lives: int
    _respawn_point: tuple[int, int]
    _cheats: bool
    _invincible: bool
    _speed: float  # Tengo dudas de este

    def __init__(
            self, p_coords: tuple[int, int],
            p_lives: int):
        self._coords = p_coords
        self._lives = p_lives
        self._respawn_point = p_coords
        self._cheats = False
        self._invincible = False
        self._speed = 1.0

    def getCoords(self) -> tuple[int, int]:

        return self._coords

    # Test methods

    def print_info(self) -> None:
        print("Hello I'm PacMan")
