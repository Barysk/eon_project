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
        self.channel_number: Optional[int] = None

    def __repr__(self) -> str:
        return f"[Super channel from {self.source} to {self.destination}]"

    def get_desired_rate(self, time: int) -> float:
        """Returns the collective desired rate of the underlying connections."""
        cumulative_rate = 0
        for connection in self.__connections:
            cumulative_rate += connection.rates[time]
        return cumulative_rate

    def assign_solution(self, route : Route, modulation : Modulation, spectral_position : int, channel_number : int) -> None:
        """Stores the spectral assignments and used connection parameters."""
        self.route = route
        self.modulation = modulation
        self.spectral_position = spectral_position
        self.channel_number = channel_number

        for edge in route.edges:
            edge["slots"].reserve_slots(start=spectral_position, width=modulation.width * channel_number)

    def clear_solution(self) -> None:
        """Returns the superchannel to a clear state, freeing the used resources in the process."""
        if self.route is not None:
            for edge in self.route.edges:
                edge["slots"].clear() # free up the spectrum used by the superchannel

        self.route = None
        self.modulation = None
        self.spectral_position = None
        self.channel_number = None

    def get_debug(self, iteration : int) -> str:
        return f"{self.source}\t{self.destination}\t{self.get_desired_rate(iteration):3.3f}\t{self.modulation}\t{self.route.distance}\t{self.modulation.max_distance}"