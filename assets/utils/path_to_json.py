import json
from collections import defaultdict

def load_pat_file(path):
	with open(path, "r") as f:
		lines = f.read().strip().splitlines()
	total_paths = int(lines[0])
	raw_paths = [list(map(int, line.split())) for line in lines[1:]]
	assert len(raw_paths) == total_paths
	return raw_paths

def load_links_from_netjson(path):
	with open(path, "r") as f:
		net = json.load(f)

	links = []
	for link in net["links"]:
		lid = link["id"]
		src = link["src"]
		dst = link["dst"]

		if len(links) <= lid:
			links.extend([None] * (lid - len(links) + 1))

		links[lid] = (src, dst)

	return links, net["name"], len(net["nodes"])

def link_bits_to_node_path(bits, links):
	used_links = [links[i] for i, b in enumerate(bits) if b == 1]

	if not used_links:
		raise ValueError("Empty path detected in .pat file")

	adj = defaultdict(list)
	indeg = defaultdict(int)
	outdeg = defaultdict(int)

	for u, v in used_links:
		adj[u].append(v)
		outdeg[u] += 1
		indeg[v] += 1

	start_candidates = [n for n in outdeg if outdeg[n] == indeg[n] + 1]

	if len(start_candidates) == 1:
		start = start_candidates[0]
	else:
		zero_in = [n for n in adj if indeg[n] == 0]
		if len(zero_in) == 1:
			start = zero_in[0]
		else:
			start = min(u for u, _ in used_links)

	path = [start]
	cur = start
	visited = set()

	while True:
		next_nodes = [v for v in adj[cur] if (cur, v) not in visited]
		if not next_nodes:
			break
		v = next_nodes[0]
		visited.add((cur, v))
		path.append(v)
		cur = v

	return path

def convert_pat_to_routes(pat_path, netjson_path, output_path):
	raw_paths = load_pat_file(pat_path)
	links, net_name, n_nodes = load_links_from_netjson(netjson_path)

	paths_per_pair = 30

	expected = paths_per_pair * n_nodes * (n_nodes - 1)
	if len(raw_paths) != expected:
		raise ValueError(
			f".pat file path count mismatch: expected {expected}, got {len(raw_paths)}"
		)

	routes_json = {
		"name": net_name,
		"alias": net_name,
		"routes": []
	}

	idx = 0

	for src in range(n_nodes):
		for dst in range(n_nodes):
			if src == dst:
				continue


			entry = {"src": src, "dst": dst, "paths": []}

			for _ in range(paths_per_pair):
				bits = raw_paths[idx]
				node_path = link_bits_to_node_path(bits, links)
				entry["paths"].append(node_path)
				idx += 1

			routes_json["routes"].append(entry)

	with open(output_path, "w") as f:
		json.dump(routes_json, f, indent=4)

	print(f"Saved {output_path} (full 30 paths per pair)")

if __name__ == "__main__":
	convert_pat_to_routes(
		pat_path="../POL12/pol12.pat",
		netjson_path="pol12net.json",
		output_path="pol12pat.json"
	)

	convert_pat_to_routes(
		pat_path="../US26/us26.pat",
		netjson_path="us26net.json",
		output_path="us26pat.json"
	)

