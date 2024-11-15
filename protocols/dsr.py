#!/usr/bin/env python
# coding: utf-8

# In[4]:


class DSR:
    def __init__(self, network):
        self.network = network
        self.route_cache = {}

    def find_route(self, src_id, dest_id):
        if (src_id, dest_id) in self.route_cache:
            return self.route_cache[(src_id, dest_id)]  # Return cached path if available

        # Discover route via DFS with path caching
        path = self.dfs_route_discovery(src_id, dest_id)
        
        if path:
            self.cache_route(src_id, dest_id, path)
        return path

    def dfs_route_discovery(self, src_id, dest_id):
        stack = [(src_id, [src_id])]
        visited = set()

        while stack:
            current, path = stack.pop()
            visited.add(current)

            # Check if destination is reached
            if current == dest_id:
                return path

            # Visit neighbors
            current_node = self.network.nodes[current]
            for neighbor in current_node.neighbors:
                if neighbor.node_id not in visited:
                    stack.append((neighbor.node_id, path + [neighbor.node_id]))

        return None

    def cache_route(self, src_id, dest_id, path):
        # Cache route for both directions
        self.route_cache[(src_id, dest_id)] = path
        self.route_cache[(dest_id, src_id)] = path[::-1]


# In[3]:


# class DSR:
#     def __init__(self, network):
#         self.network = network

#     def find_route(self, src_id, dest_id):
#         route_cache = {}

#         def dfs(current, dest, path):
#             if current == dest:
#                 return path
#             route_cache[current] = path
#             current_node = self.network.nodes[current]
#             for neighbor in current_node.neighbors:
#                 if neighbor.node_id not in path:
#                     result = dfs(neighbor.node_id, dest, path + [neighbor.node_id])
#                     if result:
#                         return result
#             return None

#         return dfs(src_id, dest_id, [src_id])


# In[ ]:




