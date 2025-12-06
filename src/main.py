from src.algorithms.first_fit_ng import FirsFitNG
from src.data_structures.modulation import Modulation
from src.data_structures.data_importer import read_graph_from_file, read_routes_from_file, read_connections_from_folder

POL12 = read_graph_from_file("assets/POL12/pol12.net")
POL12_rt = read_routes_from_file("assets/POL12/pol12.pat", POL12)
POL12_connections = read_connections_from_folder("assets/POL12/demands_0", 50)

modulations = [Modulation(name="QPSK", max_distance=9999, bit_rate=200, width=6),
               Modulation(name="8-QAM", max_distance=9999, bit_rate=400, width=9),
               Modulation(name="16-QAM", max_distance=800, bit_rate=400, width=6),
               Modulation(name="16-QAM", max_distance=1600, bit_rate=600, width=9),
               Modulation(name="32-QAM", max_distance=200, bit_rate=800, width=9)]

first_fit_ng = FirsFitNG()
first_fit_ng.run(graph=POL12, connections=POL12_connections, routes=POL12_rt, modulations=modulations)
