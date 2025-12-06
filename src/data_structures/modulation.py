from typing import Final


class Modulation:
    def __init__(self, name : str, bit_rate : int, max_distance : int, width : int):
        self.name : Final[str] = name
        self.bit_rate : Final[int] = bit_rate
        self.max_distance : Final[int] = max_distance
        self.width : Final[int] = width

    def __repr__(self) -> str:
        return self.name