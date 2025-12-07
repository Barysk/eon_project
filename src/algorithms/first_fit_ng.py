from networkx import DiGraph

from src.algorithms.algorithm import Algorithm
from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route
from src.data_structures.superchannel import SuperChannel


class FirsFitNG(Algorithm):
    """Implementation of the First Fit algorithm without grooming."""

    def __init__(self, graph: DiGraph, connections: list[Connection], routes: list[Route], modulations: list[Modulation]):
        super().__init__(graph, connections, routes, modulations)

    def __solve_rsa(self, super_channel : SuperChannel, time : int):
        for route in filter(lambda r: r.source == super_channel.source and r.destination == super_channel.destination,
                            self.routes):  # for every potential route
            possible_modulations = list(
                filter(lambda m: m.max_distance > route.distance and m.bitrate > super_channel.get_rate(time),
                       self.modulations))
            possible_modulations.sort(key=lambda m: m.width)  # TODO: possible bug, is the sorting direction good?

            for modulation in possible_modulations:
                for spectrum_start in range(320):
                    found_allocation = True
                    for edge in route.edges:
                        if not edge["slots"].is_spectrum_free(spectrum_start, modulation.width):
                            found_allocation = False
                            break
                    if found_allocation:
                        super_channel.assign_solution(route, modulation, spectrum_start)
                        return
        raise ValueError("Could not solve RSA for current state!")

    def __update_superchannels(self, time: int) -> None:
        """Updates the superchannels by recalculating the rates and, if necessary, routing and modulating them differently."""
        for sup_chan in self.super_channels:
            if sup_chan.get_rate(time) > sup_chan.modulation.bitrate:
                try:
                    self.__solve_rsa(sup_chan, time)
                except ValueError:
                    self.__rebuild_assignments()


    def __init_superchannels(self):
        """Build new superchannels, assuming a clean state"""
        for connection in self.connections:
            new_channel = SuperChannel(connections=[connection])
            self.__solve_rsa(new_channel, 0)


    def __rebuild_assignments(self):
        """Regenerate the assignments from scratch. Cleans the network state."""
        for edge in self.graph.edges:
            edge["slots"].clear()

        for super_channel in self.super_channels:
            super_channel.modulation = None
            super_channel.spectral_position = None
            super_channel.route = None
        pass

    def run(self):
        self.__init_superchannels()
        for iteration in range(len(self.connections[0].rates)):
            pass

