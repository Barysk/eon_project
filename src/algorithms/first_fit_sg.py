from collections import defaultdict

from networkx import DiGraph

from src.algorithms.algorithm import Algorithm
from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route
from src.data_structures.superchannel import SuperChannel


class FirstFitSG(Algorithm):
    """Implementation of the First Fit algorithm with static grooming at the start."""

    def __init__(self, graph: DiGraph, connections: list[Connection], routes: list[Route], modulations: list[Modulation]):
        super().__init__(graph, connections, routes, modulations)

    def _solve_rsa(self, super_channel : SuperChannel, time : int) -> float:
        for route in filter(lambda r: r.source == super_channel.source and r.destination == super_channel.destination,
                            self.routes):  # for every potential route (filter is stable, so the shortest first)

            channel_number = 0 # number of channels, used to serve superchannels with large throughput
            possible_modulations = []
            while len(possible_modulations) == 0:
                channel_number += 1
                possible_modulations = list(
                    filter(lambda m: m.max_distance > route.distance and m.bitrate * channel_number > super_channel.get_desired_rate(time),
                           self.modulations))
            possible_modulations.sort(key=lambda m: m.width)

            for modulation in possible_modulations:
                for spectrum_start in range(320):
                    found_allocation = True
                    for edge in route.edges:
                        if not edge["slots"].is_spectrum_free(spectrum_start, modulation.width*channel_number):
                            found_allocation = False
                            break
                    if found_allocation:
                        super_channel.assign_solution(route, modulation, spectrum_start, channel_number)
                        return 0.0  # successfully assigned
        return super_channel.get_desired_rate(time) # how much bitrate did we drop

    def _init_superchannels(self):
        if not len(self.super_channels) == 0:
            raise ValueError("Superchannels already exist! Unstable behaviour!")

        grouped_connections = {}
        for connection in self.connections:
            key = (connection.source, connection.destination)
            if key not in grouped_connections:
                grouped_connections[key] = [connection]
            else:
                grouped_connections[key].append(connection)

        for key, connections in grouped_connections.items():
            new_channel = SuperChannel(connections=connections)
            self.super_channels.append(new_channel)
        self._rebuild_assignments(0)

