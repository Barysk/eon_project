import networkx as nx
from src.data_structures.slots import Slots
from src.data_structures.data_importer import read_graph_from_file

G = nx.DiGraph()

G.add_edge("A", "B", slots = Slots())
G.add_edge("B", "D", slots = Slots())
G.add_edge("A", "C", slots = Slots())
G.add_edge("C", "D", slots = Slots())

POL12 = read_graph_from_file("assets/POL12/pol12.net")

# get all nodes of a graph
for n in POL12.nodes():
    print(f"Node: {n}, type: {type(n)}")

print("----")
# get edges and all their data
for e in POL12.edges.data():
    print(e)

print("----")
# get edges with only the "distance" attribute
for e in POL12.edges.data("distance"):
    print(e)

print("----")
# get edges with only the "slots" attribute
for e in POL12.edges.data("slots"):
    print(e)

