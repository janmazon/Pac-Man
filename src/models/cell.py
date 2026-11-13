class Cell:

    _N: int
    _E: int
    _S: int
    _W: int
    _is_42: bool

    def __init__(self, p_value: int):

        self._W = (p_value >> 3) & 1
        self._S = (p_value >> 2) & 1
        self._E = (p_value >> 1) & 1
        self._N = p_value & 1

        if p_value == 15:
            self._is_42 = True
        else:
            self._is_42 = False

    def __str__(self) -> str:

        return (f"W={self._W}-S={self._S}-E={self._E}-N={self._N}")
