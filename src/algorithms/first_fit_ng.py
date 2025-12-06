from networkx import DiGraph

from src.algorithms.algorithm import Algorithm
from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route


class FirsFitNG(Algorithm):
    """Implementation of the First Fit algorithm without grooming."""

    def run(self, graph: DiGraph, connections: list[Connection], routes: list[Route], modulations: list[Modulation]):

        # TODO: move this code into a function as it will be used again
        modulation_assignments = {}
        for connection in connections:
            shortest_route = min(
                filter(lambda r: r.source == connection.source and r.destination == connection.destination, routes),
                key=lambda r: r.distance)

            possible_modulations = list(filter(lambda m: m.max_distance > shortest_route.distance, modulations))    # among those modulations that reach...
            min_width = min(possible_modulations, key=lambda m2: m2.width).width
            possible_modulations = list(filter(lambda m: m.width == min_width, possible_modulations))               # ... pick the ones with the smallest width...
            best_modulation : Modulation = max(possible_modulations, key=lambda m: m.bit_rate)                      # ... and choose the one with the highest throughput

            modulation_assignments[connection] = best_modulation

        # TODO: the algorithm only chooses the modulation, it needs to also assign and manage them
        for iteration in range(len(connections[0].rates)):
            pass
