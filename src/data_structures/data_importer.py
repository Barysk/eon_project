import os
from typing import Any

from networkx import DiGraph

from src.data_structures.connection import Connection
from src.data_structures.route import Route
from src.data_structures.slots import Slots


def read_graph_from_file(filename: str) -> DiGraph:
    """
    Creates a directed graph from the specified file.
    :param filename: relative path to the file
    :return: a directional graph represented by the file
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    graph = DiGraph()
    cnt = 0
    for i in range(2, len(lines)):
        dists = list(map(int, lines[i].split()))
        for j in range(len(dists)):
            if dists[j] > 0:
                graph.add_edge(i - 2, j, distance=dists[j], slots=Slots(), index=cnt)
                cnt += 1
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


def read_connections_from_folder(folder: str, limit: int = -1) -> list[Connection]:
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


def read_routes_from_file(filename: str, graph: DiGraph) -> list[Route]:
    """
    Reads route data from file and returns them as a list of dictionaries.
    :param filename: file to read data from
    :param graph: graph matching the path file
    :return: a list of dictionaries representing a route
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    lines = lines[1:]

    # indexing the edges for ease of access
    graph_edges : dict[int, dict[str, Any]] = {}
    for src, dest, edg_data in graph.edges(data=True):
        graph_edges[edg_data["index"]] = edg_data

    output = []
    src = 0
    dest = 0
    rt_num = 0
    for line in lines:
        if src == dest:
            dest += 1

        edge_list = list(map(int, line.split()))
        route_edges : list[int] = []
        for edg_index in range(len(edge_list)):
            if edge_list[edg_index] == 1:
                route_edges.append(edg_index)

        distance = 0
        for edge_index in route_edges:
            distance += graph_edges[edge_index]["distance"]

        rt = Route(source=src, destination=dest, edges=[graph_edges[edge_index] for edge_index in route_edges], distance=distance)
        output.append(rt)

        rt_num += 1

        if rt_num == 30:
            rt_num = 0
            dest += 1

        if dest == graph.number_of_nodes():
            dest = 0
            src += 1
    return output
