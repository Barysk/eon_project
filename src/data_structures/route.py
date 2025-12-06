from typing import Final


class Route:
    def __init__(self, source : int, destination : int, edges : list[int], distance : int) -> None:
        self.source : Final[int] = source
        self.destination : Final[int] = destination
        self.edges : Final[list[int]] = edges
        self.distance : Final[int] = distance

    def __repr__(self) -> str:
        return f"[Route from {self.source} to {self.destination}]"