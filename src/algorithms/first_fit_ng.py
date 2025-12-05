from networkx import DiGraph

from src.algorithms.algorithm import Algorithm
from src.data_structures.connection import Connection


class FirsFitNG(Algorithm):
    """Implementation of the First Fit algorithm without grooming."""
    def run(self, graph : DiGraph, connections : list[Connection], routes : list[dict]):
        for iteration in range(len(connections[0].rates)):
            pass
