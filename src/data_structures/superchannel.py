from typing import Final, Optional

from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route


class SuperChannel:
    """
    A class representing a bundle of connections with the same source and destination, along with the route and
    modulation used to transmit them.
    """

    def __init__(self, connections: list[Connection], route: Route = None, modulation: Modulation = None,
                 spectral_position: int = None) -> None:
        # TODO: Documentation
        # read only variables
        self.__connections: Final[list[Connection]] = connections
        self.source: Final[int] = connections[0].source
        self.destination: Final[int] = connections[0].destination

        # modifiable variables
        self.modulation: Optional[Modulation] = modulation
        self.route: Optional[Route] = route
        self.spectral_position: Optional[int] = spectral_position

    def __repr__(self) -> str:
        return f"[Super channel from {self.source} to {self.destination}]"

    def get_rate(self, time: int) -> float:
        """Returns the collective rate of the superchannel."""
        cumulative_rate = 0
        for connection in self.__connections:
            cumulative_rate += connection.rates[time]
        return cumulative_rate

    def assign_solution(self, route : Route, modulation : Modulation, spectral_position : int) -> None:
        self.route = route
        self.modulation = modulation
        self.spectral_position = spectral_position

        for edge in route.edges:
            edge["slots"].reserve_slots(start=spectral_position, width=modulation.width)