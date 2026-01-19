import time
import copy

from src.algorithms.first_fit_ng import FirstFitNG
from src.algorithms.first_fit_sg import FirstFitSG
from src.algorithms.exact_fit_ng import ExactFitNG
from src.algorithms.exact_fit_sg import ExactFitSG
from src.data_structures.modulation import Modulation
from src.data_structures.data_importer import read_graph_from_file, read_routes_from_file, read_connections_from_folder

net = read_graph_from_file("assets/POL12/pol12.net")
pat = read_routes_from_file("assets/POL12/pol12.pat", net)
dem = read_connections_from_folder("assets/POL12/demands_0", 400)

MOD = [Modulation(name="QPSK",   max_distance=999999, bit_rate=200, width=6),
       Modulation(name="8-QAM",  max_distance=999999, bit_rate=400, width=9),
       Modulation(name="16-QAM", max_distance=800,    bit_rate=400, width=6),
       Modulation(name="16-QAM", max_distance=1600,   bit_rate=600, width=9),
       Modulation(name="32-QAM", max_distance=200,    bit_rate=800, width=9)]

start = time.time()

print("FirstFitNG")
first_fit_ng = FirstFitNG(
        graph       = copy.deepcopy(net),
        connections = copy.deepcopy(dem),
        routes      = copy.deepcopy(pat),
        modulations = MOD)
first_fit_ng.run()

print("FirstFitSG")
first_fit_sg = FirstFitSG(
        graph       = copy.deepcopy(net),
        connections = copy.deepcopy(dem),
        routes      = copy.deepcopy(pat),
        modulations = MOD)
first_fit_sg.run()

print("ExactFitNG")
exact_fit_ng = ExactFitNG(
        graph       = copy.deepcopy(net),
        connections = copy.deepcopy(dem),
        routes      = copy.deepcopy(pat),
        modulations = MOD)
exact_fit_ng.run()

print("ExactFitSG")
exact_fit_sg = ExactFitSG(
        graph       = copy.deepcopy(net),
        connections = copy.deepcopy(dem),
        routes      = copy.deepcopy(pat),
        modulations = MOD)
exact_fit_sg.run()

end = time.time()
print("time: ", end - start)
