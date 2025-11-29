import networkx as nx
from slots import Slots

G = nx.DiGraph()

G.add_edge("A", "B", slots = Slots())
G.add_edge("B", "D", slots = Slots())
G.add_edge("A", "C", slots = Slots())
G.add_edge("C", "D", slots = Slots())

cur_slots : Slots = G["A"]["B"]["slots"]

print(cur_slots.is_spectrum_free(0, 9))
cur_slots.reserve_slots(0, 9)
print(cur_slots.is_spectrum_free(0, 9))

for n in G:
    print(f"Node: {n}, type: {type(n)}")

print("----")
for n in G:
    for e in G[n]:
        print(f"Edge from {n} to {e}: {G[n][e]}, type: {type(G[n][e])}")