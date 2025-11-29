from networkx import DiGraph
from src.slots import Slots


def create_graph_from_file(filename: str) -> DiGraph:
    """
    Creates a directed graph from the specified file.
    :param filename: relative path to the file
    :return: a directional graph represented by the file
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    graph = DiGraph()
    for i in range(2, len(lines)):
        dists = list(map(int, lines[i].split()))
        for j in range(len(dists)):
            if dists[j] > 0:
                graph.add_edge(i - 2, j, distance=dists[j], slots=Slots())
    return graph
