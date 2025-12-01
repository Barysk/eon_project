from typing import Final

from connection import Connection


class SuperChannel:
    """
    A class representing a bundle of connections with the same source and destination. Defines the encoding used by them and the route used.
    """
    def __init__(self, connections : list[Connection], routes : list[int]):
        self.__connections = connections
        self.__source : Final[int] = connections[0].source
        self.__destination : Final[int] = connections[0].destination
        self.__routes = routes

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination