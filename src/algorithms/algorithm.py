from networkx import DiGraph

from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route


class Algorithm:
    """Abstract class representing an algorithm with surrounding data structures."""
    def __init__(self):
        pass

    def run(self, graph : DiGraph, connections : list[Connection], routes : list[Route], modulations : list[Modulation]):
        pass
