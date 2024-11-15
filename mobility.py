#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math
def move_node(node, area_size=500, step_size=5):
    node.x = min(max(node.x + random.randint(-step_size, step_size), 0), area_size)
    node.y = min(max(node.y + random.randint(-step_size, step_size), 0), area_size)

def random_waypoint(node, area_size=500, pause_time=2, max_speed=10):
    """
    Random Waypoint model: moves node towards a random waypoint with pause in between.
    
    Args:
        node (Node): The node to move.
        area_size (int): The maximum area size for movement.
        pause_time (int): Pause time before moving to a new waypoint.
        max_speed (int): Maximum movement speed per step.
    """
    if not hasattr(node, 'target_x') or not hasattr(node, 'target_y'):
        # Set a new random target
        node.target_x = random.randint(0, area_size)
        node.target_y = random.randint(0, area_size)
    
    dx = node.target_x - node.x
    dy = node.target_y - node.y
    dist = math.sqrt(dx ** 2 + dy ** 2)

    if dist < max_speed:
        # Reached the target; pause and choose a new target
        node.x, node.y = node.target_x, node.target_y
        node.target_x = random.randint(0, area_size)
        node.target_y = random.randint(0, area_size)
    else:
        # Move towards target
        node.x += max_speed * dx / dist
        node.y += max_speed * dy / dist

def random_direction(node, area_size=500, max_speed=10):
    """
    Random Direction model: moves node in a random direction until it hits boundary.
    
    Args:
        node (Node): The node to move.
        area_size (int): The maximum area size for movement.
        max_speed (int): Maximum movement speed per step.
    """
    if not hasattr(node, 'direction'):
        # Set a new random direction in radians
        node.direction = random.uniform(0, 2 * math.pi)

    # Calculate new position
    node.x += max_speed * math.cos(node.direction)
    node.y += max_speed * math.sin(node.direction)

    # Check if node hits boundary
    if node.x <= 0 or node.x >= area_size or node.y <= 0 or node.y >= area_size:
        # Change direction
        node.direction = random.uniform(0, 2 * math.pi)

    


# In[ ]:




