from typing import Final


class Modulation:
    def __init__(self, name : str, rate : int, max_distance : int):
        self.name : Final[str] = name
        self.rate : Final[int] = rate
        self.range : Final[int] = max_distance