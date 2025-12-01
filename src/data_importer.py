import os
from traceback import print_exc
from unicodedata import digit

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
    cnt =0
    for i in range(2, len(lines)):
        dists = list(map(int, lines[i].split()))
        for j in range(len(dists)):
            if dists[j] > 0:
                graph.add_edge(i - 2, j, distance=dists[j], slots=Slots(), index=cnt)
                cnt+=1
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

def read_routes_from_file(filename : str, node_count : int):
    """
    Reads route data from file and returns them as an ordered list of dicts of nodes, where  each inner list represents a different route.
    :param filename: file to read data from
    :return: a list of dicts, where each of the inner dicts represents a route
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    lines = lines[1:]

    output = []
    for src in range(node_count):
        for dest in range(node_count):
            if src==dest:
                continue
            for rt_num in range(30):
                line = lines[src*node_count*(node_count-1)+dest+rt_num]
                ints = list(map(int, line.split()))
                route_edges = []
                for edg_index in range(len(ints)):
                    if ints[edg_index]==1:
                        route_edges.append(edg_index)
                route = {"source" : src, "destination" : dest, "edges" : route_edges}
                output.append(route)
    return output




if __name__ == "__main__":
    g = read_graph_from_file("../assets/POL12/pol12.net")
    rt = read_routes_from_file("../assets/POL12/pol12.pat", g.number_of_nodes())
    print(f"There are {len(rt)} routes.")
    print(f"Routes between nodes 0 and 1:")
    for route in filter(lambda c: c["source"] == 0 and c["destination"] == 1, rt):
        out = ""
        for edge_index in route["edges"]:
            edg = list(filter(lambda e: e[2]==edge_index, g.edges.data("index")))[0]
            out += f"{edg[0]} -> {edg[1]}, "
        print(out)