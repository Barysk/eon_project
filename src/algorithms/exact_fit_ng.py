from networkx import DiGraph

from src.algorithms.algorithm import Algorithm
from src.data_structures.connection import Connection
from src.data_structures.modulation import Modulation
from src.data_structures.route import Route
from src.data_structures.superchannel import SuperChannel

class ExactFitNG(Algorithm):
    """Exact Fit algorithm without grooming"""

    TOTAL_SPECTRUM = 320

    def __init__(self, graph: DiGraph, connections: list[Connection],
                 routes: list[Route], modulations: list[Modulation]):
        super().__init__(graph, connections, routes, modulations)

    def _solve_rsa(self, super_channel: SuperChannel, time: int):
        if not self.modulations:
            raise ValueError("No modulations available to solve RSA.")

        desired_rate = super_channel.get_desired_rate(time)

        for route in filter(lambda r: r.source == super_channel.source and r.destination == super_channel.destination, self.routes):

            if not getattr(route, "edges", None):
                continue

            total_free = [
                all(edge["slots"].is_spectrum_free(i, 1) for edge in route.edges)
                for i in range(self.TOTAL_SPECTRUM)
            ]

            free_intervals = []
            i = 0
            while i < self.TOTAL_SPECTRUM:
                if total_free[i]:
                    start = i
                    length = 0
                    while i < self.TOTAL_SPECTRUM and total_free[i]:
                        length += 1
                        i += 1
                    free_intervals.append((start, length))
                else:
                    i += 1

            if not free_intervals:
                continue

            min_mod_width = min(m.width for m in self.modulations)
            max_channel_number = max(1, self.TOTAL_SPECTRUM // min_mod_width)

            for channel_number in range(1, max_channel_number + 1):
                candidates = [
                    m for m in self.modulations
                    if m.max_distance >= route.distance and (m.bitrate * channel_number) >= desired_rate
                ]
                if not candidates:
                    continue

                candidates.sort(key=lambda m: m.width)

                for modulation in candidates:
                    required_slots = modulation.width * channel_number
                    if required_slots > self.TOTAL_SPECTRUM:
                        continue

                    # exact
                    exact = next(((s, l) for (s, l) in free_intervals if l == required_slots), None)
                    if exact is not None:
                        start_index = exact[0]
                        super_channel.assign_solution(route, modulation, start_index, channel_number)
                        return

                    # # best-fit fallback
                    # larger_candidates = [(s, l) for (s, l) in free_intervals if l >= required_slots]
                    # if larger_candidates:
                    #     # choose smallest length, tie-break by leftmost start
                    #     best = min(larger_candidates, key=lambda x: (x[1], x[0]))
                    #     start_index = best[0]  # left-align inside the chosen interval
                    #     super_channel.assign_solution(route, modulation, start_index, channel_number)
                    #     return

                    # first-fit fallback
                    for (s, l) in free_intervals:
                        if l >= required_slots:
                            start_index = s
                            super_channel.assign_solution(route, modulation, start_index, channel_number)
                            return

        raise ValueError("Could not solve RSA for current state!")

    def _init_superchannels(self):
        if len(self.super_channels) != 0:
            raise ValueError("Superchannels already exist! Unstable behaviour!")
        for connection in self.connections:
            new_channel = SuperChannel(connections=[connection])
            self.super_channels.append(new_channel)
        self._rebuild_assignments(0)

