from typing import Final, Any


class Route:
    """A class representing a route between two channels. Immutable."""
    def __init__(self, source : int, destination : int, edges : list[dict], distance : int) -> None:
        self.source : Final[int] = source
        self.destination : Final[int] = destination
        self.edges : Final[list[dict[str, Any]]] = edges
        self.distance : Final[int] = distance

    def __repr__(self) -> str:
        return f"[Route from {self.source} to {self.destination}]"