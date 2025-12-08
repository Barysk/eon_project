from networkx import DiGraph

from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route
from src.data_structures.superchannel import SuperChannel


class Algorithm:
    """Abstract class representing an algorithm with surrounding data structures."""

    def __init__(self, graph: DiGraph, connections: list[Connection], routes: list[Route],
                 modulations: list[Modulation]):
        self.time: int = 0
        self.graph: DiGraph[int] = graph
        self.routes: list[Route] = routes
        self.modulations: list[Modulation] = modulations
        self.connections: list[Connection] = connections
        # initializing the super channels is implementation's responsibility
        self.super_channels: list[SuperChannel] = []
        return

    def _solve_rsa(self, super_channel: SuperChannel, time: int):
        """Solves the RSA problem for the given SuperChannel
        (ie assigns it a route, modulation and spectral resources respecting the constraints)

        :param super_channel: SuperChannel object to be assigned a new solution
        :param time: current iteration in the network simulation
        """
        pass

    def _init_superchannels(self):
        """Build new superchannels, assuming none exist."""
        pass

    def run(self):
        """Runs the algorithm and logs performance."""
        self._init_superchannels()
        cumulative_perf = 0
        for iteration in range(len(self.connections[0].rates)):
            self._update_superchannels(iteration)
            perf = 0
            for super_channel in self.super_channels:
                perf += super_channel.channel_number
            cumulative_perf += perf
            print(f"Iteration {iteration}: {perf}")
        print(f"Overall: {cumulative_perf}")

    def _rebuild_assignments(self, time: int) -> None:
        """Cleans the resource allocation and regenerates the solutions.
        Preserves the created SuperChannels."""
        for super_channel in self.super_channels:  # free the resources
            super_channel.clear_solution()

        # if everything works as it should, now the resources are freed up
        for super_channel in self.super_channels:  # generate new solutions
            self._solve_rsa(super_channel, time)

    def _update_superchannels(self, time: int) -> None:
        """Updates the superchannels by recalculating the desired rates and, if necessary, routing and modulating them differently."""
        try:
            for sup_chan in self.super_channels:
                if sup_chan.get_desired_rate(time) > sup_chan.modulation.bitrate * sup_chan.channel_number:
                    self._solve_rsa(sup_chan, time)
        except ValueError:  # The problem is unsolvable
            self._rebuild_assignments(time)
