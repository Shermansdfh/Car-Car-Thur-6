import itertools
from collections import defaultdict
from maze import Maze
from node import Node

class BruteForce:
    def __init__(self, maze_file, start_node_idx: int):
        """ 
        Initializes the BruteForce object.

        Args:
            maze_file (str): The file path of the maze CSV file.
            start_node_idx (int): The index of the starting node.
        """
        self.maze = Maze(maze_file)
        self.start_node = Node(start_node_idx)
        self.dead_ends_list = self.get_dead_end()
        self.distances = self.calculate_distances()
        self.scores = self.calculate_scores()

    def get_dead_end(self):
        """ 
        Finds the dead end nodes in the maze.

        Returns:
            list: A list of dead end nodes.
        """
        dead_ends = []
        for i in self.maze.node_dict.keys():
            if (self.maze.node_dict[i][1]):
                if (i != 5 and i != 0):
                    # print("dead_ends" + str(i))
                    dead_ends.append(self.maze.node_dict[i][0])
        return dead_ends
        
    def calculate_distances(self):
        distances = defaultdict(dict)
        for node1 in self.dead_ends_list:
            for node2 in self.dead_ends_list:
                if node1 != node2:
                    distance = self.maze.BFS_2_distance(node1, node2)
                    node1_index = node1.get_index()
                    node2_index = node2.get_index()
                    distances[node1_index][node2_index] = distance
        return distances

    def calculate_scores(self):
        scores = defaultdict(dict)
        for node in self.dead_ends_list:
            score = self.maze.ManhattanDistance(self.start_node, node)
            scores[node.get_index()] = score
        return scores

    def find_optimal_path(self, maximum_distance: int):
        optimal_path = []
        max_score = 0

        for permutation in itertools.permutations(self.dead_ends_list):
            current_score = 0
            distances = 0
            current_path = []
            start_node = self.start_node

            for node in permutation:
                start_node_index = start_node.get_index()
                node_index = node.get_index()
                if start_node_index == node_index:
                    continue
                try:
                    distance = self.distances[start_node_index][node_index]
                except KeyError:
                    print(f"Warning: Distance between nodes {start_node_index} and {node_index} not found in self.distances.")
                    distance = float('inf')  # Or handle the case in a different way
                distances += distance
                if distances >= maximum_distance:
                    break
                score = self.scores[node_index]
                current_score += score
                current_path.append((start_node_index, node_index, distance))
                start_node = node

            if current_score > max_score:
                max_score = current_score
                optimal_path = current_path

        return optimal_path, max_score

if __name__ == "__main__":
    maze_file = "python/data/big_maze_112.csv"
    brute_force = BruteForce(maze_file, 6)
    optimal_path, max_score = brute_force.find_optimal_path(40)
    print(f"Optimal path: {optimal_path}")
    print(f"Maximum score: {max_score}")