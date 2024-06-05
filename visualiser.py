import matplotlib.pyplot as plt
import networkx as nx
import re


class NetworkVisualizer:
    """A class for parsing network output and visualizing the topology."""

    def __init__(self):
        pass
    def parse_output(text):
        """Parses the provided text output and returns a structured dictionary.

        Args:
            text: The text output to parse.

        Returns:
            A dictionary containing the parsed information.
        """

        # Extract the total CPRI links information
        total_links_match = re.search(r"Total: (\d+) CPRI links \((\d+) OK, (\d+) OKW, (\d+) NOK, (\d+) NT\)", text)
        if total_links_match:
            total_links = {
                "Total": int(total_links_match.group(1)),
                "OK": int(total_links_match.group(2)),
                "OKW": int(total_links_match.group(3)),
                "NOK": int(total_links_match.group(4)),
                "NT": int(total_links_match.group(5))
            }
        else:
            total_links = {}

        # Extract the RRU information
        rrus = []
        for match in re.findall(
                r"^\|\s*(\w+)\s*\|\s*(\w+)\s*(\w+)\s*(\w+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*$",
                text, re.MULTILINE):
            rrus.append({
                "ID": match[0],
                "Band": match[1],
                "O": match[2],
                "D": match[3],
                "RRU_Type": match[4],
                "RRU_Model": match[5],
                "BXP": match[6],
                "SE": match[7],
                "AG": match[8],
                "FDD": match[9],
                "NB": match[10],
                "Status": match[11],
                "Status_Value": match[12],
            })

        # Extract BBU information
        bbu_match = re.search(
            r"\|\s*(UL_BB\s+\w+)\s+\|\s*(BB\d+)\s+\|\s*(\d+)\s*\|", text)
        if bbu_match:
            bbu_id = bbu_match.group(1)
            bbu_name = bbu_match.group(2)
        else:
            bbu_id = None
            bbu_name = None

        # Return the parsed information
        return {
            "Total_Links": total_links,
            "RRUs": rrus,
            "BBU_ID": bbu_id,
            "BBU_Name": bbu_name
        }


    def create_network_graph(parsed_data):
        """Creates a network graph from the parsed data.

        Args:
            parsed_data: The dictionary containing the parsed information.

        Returns:
            A NetworkX graph object representing the network topology.
        """

        # Extract the BBU and RRU information from the parsed data
        bbu_id = parsed_data["BBU_ID"]
        bbu_name = parsed_data["BBU_Name"]

        rrus = [{"name": rru["RRU_Type"], "BXP": rru["BXP"], "link": rru["ID"]} for rru in parsed_data["RRUs"]]

        # Create a graph
        G = nx.Graph()

        # Ensure bbu_id is not None before adding it
        if bbu_id is None:
            raise ValueError("BBU ID could not be found in the parsed data.")

        # Add BBU node
        G.add_node(bbu_id, label=bbu_name)

        # Add RRU nodes and edges
        for rru in rrus:
            G.add_node(rru["name"])
            G.add_edge(bbu_id, rru["name"], label=rru["link"])

        # Set node labels
        node_labels = {node: node for node in G.nodes}

        # Set edge labels
        edge_labels = {(u, v): G[u][v]["label"] for u, v in G.edges}

        return G, node_labels, edge_labels


    def draw_graph(G, node_labels, edge_labels):
        """Draws the network graph.

        Args:
            G: The NetworkX graph object.
            node_labels: The dictionary of node labels.
            edge_labels: The dictionary of edge labels.
        """
        # Set up the plot
        plt.figure(figsize=(12, 8))

        # Define the layout for the graph
        pos = nx.spring_layout(G)

        # Draw the nodes with labels
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='skyblue', edgecolors='black')
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_color='black')

        # Draw the edges with labels
        nx.draw_networkx_edges(G, pos, width=2, edge_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        # Display the plot
        plt.title("Network Topology")
        plt.axis('off')
        plt.show()