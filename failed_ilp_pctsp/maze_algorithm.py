from pulp import *
from maze import Maze
from node import Direction, Node

maze = Maze(r"C:\Users\88696\Downloads\big_maze_112.csv")


# Create the problem instance
prob = LpProblem("PCTSP", LpMaximize)
node_num = maze.get_node_number()
# Define the decision variables
x = LpVariable.dicts("x", ((i, j) for i in range(node_num) for j in range(node_num)), cat="Binary")
y = LpVariable.dicts("y", maze.get_node_dict(), cat="Binary")

# Define the objective function
prob += lpSum(maze.AllManhattanDistance(Node(6))[i] * y[i] for i in maze.get_node_dict()), "Total Prize Collected"

# Add constraints
# Ensure that each visited node has exactly one incoming and one outgoing edge
for i in range(node_num):
    prob += lpSum(x[j, i] for j in range(node_num)) == y[i+1], f"In Degree of Node {i+1}"
    prob += lpSum(x[i, j] for j in range(node_num)) == y[i+1], f"Out Degree of Node {i+1}"

# Ensure tour connectivity
u = LpVariable.dicts("u", maze.get_node_dict(), lowBound=0, cat="Integer")
for i in range(node_num):
    for j in range(node_num):
        if i != j:
            prob += u[i+1] - u[j+1] + (node_num) * x[i, j] <= len(maze.get_node_dict()) - 1, f"Subtour Elimination ({i+1}, {j+1})"

# Add distance constraint (if applicable)
distance_limit = 48
distances = {}
for i in range(node_num):
    for j in range(node_num):
        if i != j:
            distances[i+1, j+1]  = len(maze.BFS_2(Node(i+1), Node(j+1)))
if distance_limit is not None:
    prob += lpSum(distances[i+1, j+1] * x[i, j] for i in range(node_num) for j in range(node_num)) <= distance_limit, "Distance Limit"

# Solve the problem
prob.solve()

# Print the solution
print(f"Status: {LpStatus[prob.status]}")
print(f"Total Prize Collected: {value(prob.objective)}")
visited_nodes = [i for i in nodes if value(y[i+1]) > 0]
print(f"Visited Nodes: {visited_nodes}")
tour = []
for i in visited_nodes:
    for j in visited_nodes:
        if value(x[i][j]) > 0:
            tour.append((i, j))
print(f"Tour: {tour}")