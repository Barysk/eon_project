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
        self._avg_used_transceivers: float = 0
        self._avg_dropped_bitrate: float = 0
        return

    def _solve_rsa(self, super_channel: SuperChannel, time: int) -> float:
        """Solves the RSA problem for the given SuperChannel
        (ie assigns it a route, modulation and spectral resources respecting the constraints)

        :param super_channel: SuperChannel object to be assigned a new solution
        :param time: current iteration in the network simulation
        :return: dropped bitrate (0 in case of success)
        """
        pass

    def _init_superchannels(self) -> None:
        """Build new superchannels, assuming none exist."""
        pass

    def run(self):
        """Runs the algorithm and logs performance."""
        self._init_superchannels()

        used_transceivers_overall = 0
        desired_bitrate_overall = 0.0
        dropped_bitrate_overall = 0.0

        for iteration in range(len(self.connections[0].rates)):
            dropped_bitrate = self._update_superchannels(iteration)

            used_transceivers = 0
            desired_bitrate = 0

            for super_channel in self.super_channels:
                used_transceivers += (super_channel.channel_number or 0) # handle the unassigned superchannels
                desired_bitrate += super_channel.get_desired_rate(iteration)

            used_transceivers_overall += used_transceivers
            desired_bitrate_overall += desired_bitrate
            dropped_bitrate_overall += dropped_bitrate

            print(f"DEBUG: Iteration {iteration:3} | Desired bitrate: {desired_bitrate:6.0f} | Dropped bitrate: {dropped_bitrate:6.0f} | Used transceivers: {used_transceivers}")

        self._avg_used_transceivers = used_transceivers_overall / len(self.connections[0].rates)
        self._avg_dropped_bitrate = dropped_bitrate_overall / desired_bitrate_overall

    def get_overall_performance(self) -> tuple[float, float]:
        """
        Returns the perforamce of the algorithm.
        :return: A pair of (average used transceivers, average dropped bitrate)
        """

        return self._avg_used_transceivers, self._avg_dropped_bitrate

    def _rebuild_assignments(self, time: int) -> float:
        """
        Cleans the resource allocation and regenerates the solutions.
        Preserves the created SuperChannels.
        :param time: current iteration in the network simulation
        :return: The total dropped bitrate after the reassignment
        """
        for super_channel in self.super_channels:  # free the resources
            super_channel.clear_solution()

        dropped_bitrate = 0.0
        for super_channel in self.super_channels:  # generate new solutions
            dropped_bitrate += self._solve_rsa(super_channel, time)

        return dropped_bitrate

    def _update_superchannels(self, time: int) -> float:
        """
        Updates the superchannels by recalculating the desired rates and, if necessary, routing and modulating them differently.
        :return: The total dropped bitrate after the update from channels we couldn't serve
        """

        failed = False
        # for each superchanel...
        for sup_chan in self.super_channels:
            # ... check if:
            if (sup_chan.get_desired_rate(time) > sup_chan.modulation.bitrate * sup_chan.channel_number # the demand is too large OR
                    or sup_chan.get_desired_rate(time) < 0.9 * sup_chan.modulation.bitrate * sup_chan.channel_number # the demand is too small OR
                    or sup_chan.route is None): # the channel is unassigned
                # ... and if not, try to reassign it
                if self._solve_rsa(sup_chan, time) > 0:
                    failed = True
                    break
        # on a failure, rebuild all assignments from scratch
        if failed:
            return self._rebuild_assignments(time)

        # successful update
        return 0
