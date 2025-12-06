from networkx import DiGraph

from src.data_structures.connection import Connection


class Algorithm:
    """Abstract class representing an algorithm with surrounding data structures."""
    def __init__(self):
        pass

    def run(self, graph : DiGraph, connections : list[Connection], routes : list[dict], modulations : list[dict]):
        pass
