from networkx import DiGraph

from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route
from src.data_structures.superchannel import SuperChannel


class Algorithm:
    """Abstract class representing an algorithm with surrounding data structures."""

    def __init__(self, graph : DiGraph[int], connections : list[Connection], routes : list[Route], modulations : list[Modulation]):
        self.time : int = 0
        self.graph : DiGraph[int] = graph
        self.routes : list[Route]= routes
        self.modulations : list[Modulation] = modulations
        self.connections : list[Connection] = connections
        self.super_channels : list[SuperChannel] = [] # initializing the super channels is implementation's responsibility
        return

    def run(self):
        pass
