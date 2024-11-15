#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random

class AODV:
    def __init__(self, network):
        self.network = network
        self.routing_table = {}
        self.sequence_number = 0  # Sequence number for freshness of routes

    def find_route(self, src_id, dest_id):
        if dest_id in self.routing_table.get(src_id, {}):
            return self.routing_table[src_id][dest_id]['path']  # Return cached path if available

        # Initialize RREQ
        self.sequence_number += 1
        path = self.broadcast_rreq(src_id, dest_id)

        if path:
            self.update_routing_table(src_id, dest_id, path)
        return path

    def broadcast_rreq(self, src_id, dest_id):
        queue = [(src_id, [src_id])]
        visited = set()

        while queue:
            current, path = queue.pop(0)
            visited.add(current)

            # Check if we reached the destination
            if current == dest_id:
                return path

            # Forward RREQ to neighbors
            current_node = self.network.nodes[current]
            for neighbor in current_node.neighbors:
                if neighbor.node_id not in visited:
                    queue.append((neighbor.node_id, path + [neighbor.node_id]))

        return None

    def update_routing_table(self, src_id, dest_id, path):
        # Update routing table for both source and destination with bidirectional path
        if src_id not in self.routing_table:
            self.routing_table[src_id] = {}
        if dest_id not in self.routing_table:
            self.routing_table[dest_id] = {}

        self.routing_table[src_id][dest_id] = {'path': path, 'sequence_number': self.sequence_number}
        self.routing_table[dest_id][src_id] = {'path': path[::-1], 'sequence_number': self.sequence_number}


# In[3]:


# class AODV:
#     def __init__(self, network):
#         self.network = network

#     def find_route(self, src_id, dest_id):
#         visited = set()
#         queue = [(src_id, [src_id])]

#         while queue:
#             current, path = queue.pop(0)
#             if current == dest_id:
#                 return path
#             visited.add(current)

#             current_node = self.network.nodes[current]
#             for neighbor in current_node.neighbors:
#                 if neighbor.node_id not in visited:
#                     queue.append((neighbor.node_id, path + [neighbor.node_id]))

#         return None  # No route found


# In[ ]:




