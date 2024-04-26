from pulp import *
from maze import Maze
from node import Direction, Node

# Load the maze
maze = Maze(r"C:\Users\88696\Downloads\big_maze_112.csv")
node_num = maze.get_node_number()
node_dict = maze.get_node_dict()

# Create the problem instance
prob = LpProblem("PCTSP", LpMaximize)

# Define the decision variables
x = LpVariable.dicts("x", ((i, j) for i in node_dict.keys() for j in node_dict.keys()), cat="Binary")
y = LpVariable.dicts("y", node_dict, cat="Binary")

# Define the objective function
prob += lpSum(maze.AllManhattanDistance(Node(6))[i] * y[i] for i in node_dict.keys()), "Total Prize Collected"

# Add constraints
# Ensure that each visited node has exactly one incoming and one outgoing edge
for i in node_dict.keys():
    prob += lpSum(x[j, i] for j in node_dict.keys()) == y[i], f"In Degree of Node {i}"
    prob += lpSum(x[i, j] for j in node_dict.keys()) == y[i], f"Out Degree of Node {i}"

# Ensure tour connectivity
u = LpVariable.dicts("u", node_dict.keys(), lowBound=0, cat="Integer")
for i in node_dict.keys():
    for j in node_dict.keys():
        if i != j:
            prob += u[i] - u[j] + node_num * x[i, j] <= node_num - 1, f"Subtour Elimination ({i}, {j})"

# Add distance constraint (if applicable)
distances = {}
distance_limit = 48
for i in node_dict.keys():
    for j in node_dict.keys():
        if (node_dict[j][0].is_successor(node_dict[i][0])):
            distances[(i, j)] = maze.BFS_2_distance(node_dict[i][0], node_dict[j][0])
        else:
            distances[(i, j)] = 100

if distance_limit is not None:
    prob += lpSum(distances[i, j] * x[i, j] for i in node_dict.keys() for j in node_dict.keys()) <= distance_limit, "Distance Limit"

# Solve the problem
prob.solve()

# Print the solution
print(f"Status: {LpStatus[prob.status]}")
print(f"Total Prize Collected: {value(prob.objective)}")
visited_nodes = [i for i in node_dict.keys() if value(y[i]) > 0]
print(f"Visited Nodes: {visited_nodes}")
tour = []
for i in visited_nodes:
    for j in visited_nodes:
        if value(x[i, j]) > 0:
            tour.append((i, j))
print(f"Tour: {tour}")