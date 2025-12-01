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

def read_routes_from_file(filename : str, g : DiGraph):
    """
    Reads route data from file and returns them as an ordered list of lists of nodes, where  each inner list represents a different route.
    :param filename: file to read data from
    :return: a list of lists, where each of the inner lists represents a route
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    lines = lines[1:]

    temp = []
    edge_list = list(g.edges.data("index"))
    edge_list.sort()
    print(edge_list)
    for line in lines[:5]:
        ints = list(map(int, line.split()))
        out_line = ""
        for i in range(len(ints)):
            if ints[i]==1:
                out_line += f"{i}:{str(edge_list[i])}\t"
                #out_line += f"{i} "
        print(out_line)

    return None




if __name__ == "__main__":
    g = read_graph_from_file("../assets/POL12/pol12.net")
    read_routes_from_file("../assets/POL12/pol12.pat", g)