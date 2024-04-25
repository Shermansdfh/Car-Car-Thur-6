import pandas as pd
from collections import defaultdict
import heapq

def find_best_route(filepath, start_node):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(filepath)

    # Create a graph from the DataFrame
    graph = defaultdict(list)
    for _, row in data.iterrows():
        node = row['index']
        for direction, neighbor in row[['North', 'South', 'West', 'East']].dropna().items():
            neighbor = int(neighbor)
            weight = row[f'{direction[0]}D'] 
            graph[node].append((neighbor, weight))

    # Initialize distances and previous nodes for the modified Dijkstra's algorithm
    distances = {node: -float('inf') for node in graph.keys()}
    distances[start_node] = 0
    previous = {node: None for node in graph.keys()}

    # Use a priority queue to get the node with the maximum distance
    pq = [(-distances[start_node], start_node)]

    while pq:
        current_dist, current_node = heapq.heappop(pq) # Get the node with the maximum distance
        current_dist = -current_dist  # Negate the distance to get the maximum

        if current_dist < -distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            new_dist = current_dist + weight
            if new_dist > distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (-new_dist, neighbor))
                previous[neighbor] = current_node

    # Backtrack to get the best route
    best_route = []
    node = max(distances, key=distances.get)
    while node is not None:
        best_route.append(node)
        node = previous[node]

    best_route.reverse()
    return best_route

start_node = 1
best_route = find_best_route(r"C:\Users\88696\Downloads\medium_maze.csv", start_node)
print(best_route)