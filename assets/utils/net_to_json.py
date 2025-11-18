import json

def convert_to_json(input_file, alias="NSFNet", name="National Science Foundations Network", slots=320):
	with open(input_file, "r") as f:
		lines = [line.strip() for line in f if line.strip()]

	num_nodes = int(lines[0])
	num_links = int(lines[1])

	matrix_lines = lines[2:]
	matrix = []
	for line in matrix_lines:
		row = [float(x) for x in line.split()]
		matrix.append(row)

	data = {
			"alias": alias,
			"name": name,
			"nodes": [{"id": i} for i in range(num_nodes)],
			"links": []
			}

	link_id = 0

	for i in range(num_nodes):
		for j in range(num_nodes):
			dist = matrix[i][j]
			if dist > 0:
				data["links"].append({
					"id": link_id,
					"src": i,
					"dst": j,
					"length": dist,
					"slots": slots
					})
				link_id += 1

	return data


if __name__ == "__main__":
	input_filename = "../POL12/pol12.net"      # Your original format file
	output_filename = "pol12.json"    # Output JSON file
	json_data = convert_to_json(input_filename, "POL12", "pol12")

	with open(output_filename, "w") as f:
		json.dump(json_data, f, indent=4)

	print("JSON saved to", output_filename)

	input_filename = "../US26/us26.net"      # Your original format file
	output_filename = "us26.json"    # Output JSON file
	json_data = convert_to_json(input_filename, "US26", "us26")

	with open(output_filename, "w") as f:
		json.dump(json_data, f, indent=4)

	print("JSON saved to", output_filename)

