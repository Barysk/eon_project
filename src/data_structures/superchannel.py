from typing import Final

from connection import Connection


class SuperChannel:
    """
    A class representing a bundle of connections with the same source and destination.
    """
    def __init__(self, connections : list[Connection]):
        self.__connections = connections
        self.source : Final[int] = connections[0].source
        self.destination : Final[int] = connections[0].destination


    def get_source(self) -> int:
        return self.__source

    def get_destination(self) -> int:
        return self.__destination

    def get_rate(self, time : int) -> float:
        cumulative_rate = 0
        for connection in self.__connections:
            cumulative_rate += connection.rates[time]
        return cumulative_rate