#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt

def visualize_network(network, metrics, protocol_name):
    if network is None or not hasattr(network, 'nodes') or network.nodes is None:
        print("Error: Network or network.nodes is not initialized.")
        return plt.figure()  # Return an empty figure to prevent further errors
#     """
#     Visualizes the network topology with real-time metrics and protocol information.

#     Args:
#         network (Network): The network object containing nodes and neighbors.
#         metrics (dict): Dictionary containing metrics like throughput, delay, PDR, and control overhead.
#         protocol_name (str): Name of the current protocol (AODV, DSR, OLSR).
#     """

    G = nx.Graph()
    
    # Add nodes and positions to the graph
    for node in network.nodes:
        G.add_node(node.node_id, pos=(node.x, node.y))
    
    # Add edges based on neighbors
    for node in network.nodes:
        for neighbor in node.neighbors:
            G.add_edge(node.node_id, neighbor.node_id)

    # Draw the network topology
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_weight='bold', edge_color="gray")

    # Display metrics and protocol information as a text box
    metrics_text = (
        f"Protocol: {protocol_name}\n"
        f"Throughput: {metrics['throughput']}\n"
        f"Avg End-to-End Delay: {sum(metrics['end_to_end_delay']) / len(metrics['end_to_end_delay']) if metrics['end_to_end_delay'] else 0:.2f} s\n"
        f"Packet Delivery Ratio: {metrics['packet_delivery_ratio']:.2f}\n"
        f"Control Overhead: {metrics['control_overhead']}\n"
    )
    
    # Place the metrics information on the plot
    plt.text(
        1.05, 0.5, metrics_text, 
        transform=plt.gca().transAxes, 
        fontsize=12, 
        verticalalignment='center',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
    )

    plt.title("Ad Hoc Network Topology and Metrics Visualization")
    plt.show()


# In[ ]:




