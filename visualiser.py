import re
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def extract_network_data(input_text):
    """Extracts network data from the provided input text.

    Args:
        input_text (str): The input text containing the network diagram.

    Returns:
        dict: A dictionary containing the extracted network data.
    """

    # Find the starting and ending points of the diagram
    start_index = input_text.find("+--------+")
    end_index = input_text.find(
        "=====================================================================================================================================")

    # Extract the relevant text
    diagram_text = input_text[start_index:end_index]

    # Extract the BBU information
    bbu_match = re.search(r"BB(\d+)\s+", diagram_text)
    bbu = bbu_match.group(0) if bbu_match else None

    # Extract the RRU information
    rrus = []
    for line in diagram_text.splitlines():
        match = re.search(r"RRU_([A-Za-z0-9_ -]+)", line)
        if match:
            rrus.append(match.group(0))

    # Extract the BXP information
    bxp_info = []
    for line in diagram_text.splitlines():
        match = re.search(r"BXP_(\w+)", line)
        if match:
            bxp_info.append(match.group(0))

    # Construct the data dictionary
    data = {
        "BBU": bbu,
        "RRUs": [],
    }

    # Add RRU information based on the available data
    links = ["A", "B", "C", "D", "E", "F"]
    for i in range(len(rrus)):
        if i < len(rrus):
            data["RRUs"].append({"name": rrus[i], "BXP": bxp_info[i], "link": links[i]})

    return data

def draw_network_diagram(data):
    """Draws a network diagram based on the provided data, grouping RRUs by sector.

    Args:
        data (dict): A dictionary containing the network data.
    """

    # Create a graph
    G = nx.Graph()

    # Add BBU node
    G.add_node(data["BBU"])

    # Add RRU nodes and edges, grouping by sector
    for rru in data["RRUs"]:
        G.add_node(rru["name"])
        G.add_edge(data["BBU"], rru["name"], label=rru["link"])

    # Set node labels
    node_labels = {node: node for node in G.nodes}

    # Set edge labels
    edge_labels = {(u, v): G[u][v]["label"] for u, v in G.edges}

    # Define positions for nodes, grouping by sector
    pos = {}
    sector_angles = {
        "S1": 0,
        "S2": 120,
        "S3": 240,
    }
    sector_radius = 0.8  # Adjust for sector spacing
    item_spacing = 8  # Degrees between items in a sector
    for i, node in enumerate(G.nodes):
        if node == data["BBU"]:
            pos[node] = (0, 0)  # Center the BBU
        else:
            sector = node.split("-")[-1].strip()
            angle = sector_angles[sector]
            angle += i * item_spacing  # Adjust angle for spacing within sector
            x = sector_radius * np.cos(np.deg2rad(angle))
            y = sector_radius * np.sin(np.deg2rad(angle))
            pos[node] = (x, y)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, labels=node_labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.show()

# Example usage:
with open("output.txt", "r") as file:
    input_text = file.read()
network_data = extract_network_data(input_text)
draw_network_diagram(network_data)