#!/usr/bin/env python
# coding: utf-8

# In[6]:


import random
import math
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id, x, y, range=100):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.range = range
        self.neighbors = []

    def distance_to(self, other_node):
        return math.sqrt((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2)

    def update_neighbors(self, nodes):
        self.neighbors = [node for node in nodes if node != self and self.distance_to(node) <= self.range]

class Network:
    def __init__(self, num_nodes=10, area_size=500):
        self.num_nodes = num_nodes       # Store the number of nodes
        self.nodes = []                  # List to store all nodes
        self.packet_count = 0            # Counter for total packets sent
        for i in range(num_nodes):
            x = random.randint(0, area_size)
            y = random.randint(0, area_size)
            node = Node(i, x, y)
            self.nodes.append(node)
        self.update_all_neighbors()

    def update_all_neighbors(self):
        for node in self.nodes:
            node.update_neighbors(self.nodes)
            
    def generate_packet(self, src_id, dest_id):
#         """
#         Simulates the generation of a packet between two nodes.
        
#         Args:
#             src_id (int): The source node ID.
#             dest_id (int): The destination node ID.
        
#         Returns:
#             dict: Information about the packet, including source, destination, and a unique ID.
#         """
        self.packet_count += 1  # Increment the packet count for each new packet
        packet = {
            "packet_id": self.packet_count,
            "src_id": src_id,
            "dest_id": dest_id,
            "status": "in_transit"  # Initial status of the packet
        }
        print(f"Packet {packet['packet_id']} generated from Node {src_id} to Node {dest_id}")
        return packet

    def display_network(self):
        for node in self.nodes:
            print(f"Node {node.node_id}: Neighbors -> {[n.node_id for n in node.neighbors]}")
            
    def get_total_packets(self):
#         """
#         Returns the total number of packets generated in the network.
        
#         Returns:
#             int: Total packets sent.
#         """
        return self.packet_count
    
    def move_nodes(self, area_size=500, step_size=5):
#         """
#         Moves each node within the network and updates neighbors accordingly.
        
#         Args:
#             area_size (int): Maximum area size within which nodes can move.
#             step_size (int): Maximum step size for node movement.
#         """
        for node in self.nodes:
            move_node(node, area_size, step_size)
        self.update_all_neighbors()
    

    
    


# In[2]:


import networkx as nx
import matplotlib.pyplot as plt


# In[ ]:




