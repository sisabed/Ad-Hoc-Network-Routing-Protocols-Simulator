#!/usr/bin/env python
# coding: utf-8

# In[2]:


class OLSR:
    def __init__(self, network):
        self.network = network
        self.routes = {}

    def update_routes(self):
        # Precompute routes by running BFS from each node
        for node in self.network.nodes:
            self.routes[node.node_id] = self.compute_routing_table(node)

    def compute_routing_table(self, start_node):
        queue = [(start_node.node_id, [start_node.node_id])]
        visited = set()
        routing_table = {}

        while queue:
            current, path = queue.pop(0)
            visited.add(current)
            routing_table[current] = path

            current_node = self.network.nodes[current]
            for neighbor in current_node.neighbors:
                if neighbor.node_id not in visited:
                    queue.append((neighbor.node_id, path + [neighbor.node_id]))

        return routing_table


# In[ ]:




