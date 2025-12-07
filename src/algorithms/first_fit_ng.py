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
                filter(lambda m: m.max_distance > route.distance and m.bitrate > super_channel.get_desired_rate(time),
                       self.modulations))
            possible_modulations.sort(key=lambda m: m.width)

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
        try:
            for sup_chan in self.super_channels:
                if sup_chan.get_desired_rate(time) > sup_chan.modulation.bitrate:
                    self.__solve_rsa(sup_chan, time)
        except ValueError:
            self.__rebuild_assignments(time)


    def __init_superchannels(self):
        """Build new superchannels, assuming none exist."""
        if not len(self.super_channels) == 0:
            raise ValueError("Superchannels already exist! Unstable behaviour!")
        for connection in self.connections:
            new_channel = SuperChannel(connections=[connection])
            self.super_channels.append(new_channel)
        self.__rebuild_assignments(0)


    def __rebuild_assignments(self, time: int) -> None:
        """Regenerate the assignments from scratch. Cleans the network state."""
        for super_channel in self.super_channels: # free the resources
            super_channel.clear_solution()

        # if everything works as it should, now the network is all freed up
        for super_channel in self.super_channels: # generate new solutions
            self.__solve_rsa(super_channel, time)


    def run(self):
        self.__init_superchannels()
        for iteration in range(len(self.connections[0].rates)):
            self.__update_superchannels(iteration)
            if iteration == 200:
                print(f"SRC\tDST\tBAND\tMOD\t\t\t\t\tRT DIST\tMAX DIST")
                for super_channel in self.super_channels:
                    print(super_channel.get_debug(iteration))

