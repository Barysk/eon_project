import os

from networkx import DiGraph
from src.connection import Connection
from src.slots import Slots


def read_graph_from_file(filename: str) -> DiGraph:
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

def read_connection_from_file(filename: str) -> Connection:
    """
    Reads a connection from the specified file.
    :param filename: file path
    :return: a Connection object read from the file
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    src = int(lines[0].strip())
    dst = int(lines[1].strip())
    rates = list(map(float, lines[3:]))
    return Connection(src, dst, rates)

def read_connections_from_folder(folder: str, limit : int = -1) -> list[Connection]:
    """
    Reads Connections from files in a specified folder
    :param folder: folder path
    :param limit: number of connections to read. Default value of "-1" disables the limit.
    :return:
    """
    connections = []
    if limit == -1:
        for file in os.listdir(folder):
            connections.append(read_connection_from_file(os.path.join(folder, file)))
    else:
        for i in range(limit):
            connections.append(read_connection_from_file(os.path.join(folder, os.listdir(folder)[i])))
    return connections