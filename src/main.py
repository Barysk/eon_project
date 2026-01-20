import time
import csv

from src.algorithms.first_fit_ng import FirstFitNG
from src.algorithms.first_fit_sg import FirstFitSG
from src.algorithms.exact_fit_ng import ExactFitNG
from src.algorithms.exact_fit_sg import ExactFitSG
from src.data_structures.modulation import Modulation
from src.data_structures.data_importer import read_graph_from_file, read_routes_from_file, read_connections_from_folder
from dataclasses import dataclass

@dataclass
class TestInfo:
    net: str
    pat: str
    dem: str

RESULTS_FILENAME = "results.csv"

MOD = [
    Modulation(name="QPSK",   max_distance=999999, bit_rate=200, width=6),
    Modulation(name="8-QAM",  max_distance=999999, bit_rate=400, width=9),
    Modulation(name="16-QAM", max_distance=800,    bit_rate=400, width=6),
    Modulation(name="16-QAM", max_distance=1600,   bit_rate=600, width=9),
    Modulation(name="32-QAM", max_distance=200,    bit_rate=800, width=9)
]

TESTS = [
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_0"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_1"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_2"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_3"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_4"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_5"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_6"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_7"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_8"),
    TestInfo(net="./assets/POL12/pol12.net", pat="./assets/POL12/pol12.pat", dem="./assets/POL12/demands_9"),

    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_0"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_1"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_2"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_3"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_4"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_5"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_6"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_7"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_8"),
    TestInfo(net="./assets/US26/us26.net",   pat="./assets/US26/us26.pat",   dem="./assets/US26/demands_9"),
]

def run_tests(test_case: TestInfo, MOD, output_file="results.csv"):
    req_sets = [100, 200, 300, 400, 500]

    algorythms = [
        "First Fit No Grooming",
        "First Fit Static Grooming",
        "Exact Fit No Grooming",
        "Exact Fit Static Grooming",
    ]

    net_obj = read_graph_from_file(test_case.net)
    pat_obj = read_routes_from_file(test_case.pat, net_obj)

    for i, algorythm in enumerate(algorythms):
        with open(output_file, "a") as res_file:
            res_file.write(f"net: {test_case.net}\n")
            res_file.write(f"dem: {test_case.dem}\n")
            res_file.write(f"algorithm: {algorythm}\n\n")

            res_file.write(f"requests; avg_transceiver_use; avg_dropped_bitrate\n")

            for req_set in req_sets:
                dem_obj = read_connections_from_folder(test_case.dem, req_set)

                result: tuple[float, float]

                match i:
                    case 0:
                        ffng = FirstFitNG(
                            graph       = net_obj,
                            connections = dem_obj,
                            routes      = pat_obj,
                            modulations = MOD)

                        ffng.run()

                        result = ffng.get_overall_performance()
                    case 1:
                        ffsg = FirstFitSG(
                            graph       = net_obj,
                            connections = dem_obj,
                            routes      = pat_obj,
                            modulations = MOD)

                        ffsg.run()

                        result = ffsg.get_overall_performance()
                    case 2:
                        efng = ExactFitNG(
                            graph       = net_obj,
                            connections = dem_obj,
                            routes      = pat_obj,
                            modulations = MOD)

                        efng.run()

                        result = efng.get_overall_performance()
                    case 3:
                        efsg = ExactFitSG(
                            graph       = net_obj,
                            connections = dem_obj,
                            routes      = pat_obj,
                            modulations = MOD)

                        efsg.run()

                        result = efsg.get_overall_performance()
                res_file.write(f"{req_set}; {result[0]}; {result[1]}\n")
            res_file.write(f"\n")

#########################
# BEGIN                 #
#########################

start = time.time()

for test_case in TESTS:
    run_tests(test_case, MOD, RESULTS_FILENAME)

end = time.time()
print("whole time: ", end - start)
