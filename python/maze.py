import csv
import logging
import math
from enum import IntEnum
from typing import Dict, List, Tuple

import numpy as np
import pandas 

from node import Direction, Node

log = logging.getLogger(__name__)


class Action(IntEnum):
    # The turn in this context includes turn and advance till next node.
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    """ Class to represent a data structure for nodes and their successors.

        Args:
            filepath (str): The path to the CSV file containing node data.
    """
    def __init__(self, filepath: str):
        """ Initializes the node data structure.

            Args:
                filepath (str): The path to the CSV file containing node data.
        """
        
        self.raw_data = pandas.read_csv(filepath).values # Read CSV file into a numpy array
        self.total_node_count = self.raw_data.shape[0] # Total number of nodes (starting from 1)
        self.node_dict = {}  # key: index, value: (node, is_dead_end?(bool), explored_dead_end?(bool))
        
        # Initialize node_dict.
        for ix in range(self.total_node_count): 
            index = int(self.raw_data[ix, 0])
            node = Node(index)
            self.node_dict[index] = (node, False, False) # (Node, is_dead_end?, explored_dead_end?)
        
        
        # Initialize adjacency list with successors
        for ix in range(self.total_node_count):    
            for iy in range(1, 5): # index = 0, North = 1, South = 2, West = 3, East = 4
                cell_read = int(self.raw_data[ix, iy]) if not pandas.isna(self.raw_data[ix, iy]) else 0
                idx = ix + 1
                
                # Adjacency list
                if (cell_read): # If cell_read isn't empty (i.e., NaN)
                    self.node_dict[idx][0].set_successor(self.node_dict[cell_read][0], iy)        

        for idx in range(1, self.total_node_count + 1):
            self.node_dict[idx] = (self.node_dict[idx][0],
                                   self.node_dict[idx][0].is_dead_end(),
                                   self.node_dict[idx][2])
        
    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_number(self):
        return self.total_node_count

    def get_node(self, index: int):
        return self.node_dict[index][0]
    
    def get_node_dict(self):
        return self.node_dict
    
    def find_maze_height(self) -> int:
        """ Finds the height of the maze.

        Returns:
            int: The height of the maze.
        """
        visited = set()
        min_height = float('inf')
        max_height = float('-inf')
        
        def DFS(node: Node, height: int):
            nonlocal min_height, max_height
            
            if node in visited:
                return
            
            visited.add(node)
            min_height = min(min_height, height)
            max_height = max(max_height, height)
            
            succ = node.get_successors()
            neighbors = [i[0] for i in succ]
            directions = [i[1] for i in succ]
                
            if Direction.NORTH in directions:
                DFS(neighbors[directions.index(Direction.NORTH)], height - 1)
            if Direction.SOUTH in directions:
                DFS(neighbors[directions.index(Direction.SOUTH)], height + 1)
            if Direction.WEST in directions:
                DFS(neighbors[directions.index(Direction.WEST)], height)
            if Direction.EAST in directions:
                DFS(neighbors[directions.index(Direction.EAST)], height)
        
        DFS(self.get_start_point()[0], 1)
        
        maze_height = max_height - min_height + 1
        
        return maze_height                
        
    def backtrace(self, parent_map: Dict[int, Node], node_from: Node, node_to: Node) -> List[Node]:
        """ Tracks path by finding parents till the start node
            
        Args:
            parent (Node): a dictionary that records every node's parent
            node_from (Node): The current node.
            node_to (Node): The node to move to.

        Returns:
            List[Node]: A list of nodes that tracks the path.
        """
        
        path = [node_to]
        while path[-1] != node_from:
            idx = path[-1].get_index()
            path.append(parent_map[idx])
            
        path.reverse()
        return path

    def BFS(self, node: Node):
        """ BFS that finds the nearest unexplored node and return the path.
            Records the explored dead end.

        Args:
            node (Node): The current node.

        Returns:
            List[Node]: A list of nodes of the shortest path.
        """
        
        parent = {} # key: index, value: the correspond parent node
        queue = [node] # push start node into queue
        visited = set()
        visited.add(node)
        
        # BFS
        while queue:
            now_node = queue.pop(0) # get the first node in the queue
            now_idx = now_node.get_index()
            
            if (
                self.get_node_dict()[now_idx][1] 
                & (now_idx != node.get_index()) 
                & (self.get_node_dict()[now_idx][2])
            ): # found
                self.mark_dead_end_explored()
                return self.backtrace(parent, node, self.get_node(now_idx))

            successors = self.get_node(now_idx).get_successors()
            
            for succ in successors:
                succ_node, _, _ = succ
                if succ_node not in visited:
                    parent[succ_node.get_index()] = now_node
                    queue.append(succ_node)
                    visited.add(succ_node)

    def BFS_2(self, node_from: Node, node_to: Node):
        """ BFS with fixed start point and end point

        Args:
            node_from (Node): The current node.
            node_to (Node): The node to move to.

        Returns:
            List[Node]: A list of nodes of the shortest path.
        """
        
        parent = {} # key: index, value: the correspond parent node
        queue = [node_from] # push start node into queue
        visited = set()
        visited.add(node_from)
        
        # BFS
        while queue:
            now_node = queue.pop(0) # get the first node in the queue
            now_idx = now_node.get_index()
            
            if now_idx == node_to.get_index(): # found
                return self.backtrace(parent, node_from, node_to)

            successors = self.get_node(now_idx).get_successors()
            
            for succ in successors:
                succ_node, _, _ = succ
                if succ_node not in visited:
                    parent[succ_node.get_index()] = now_node
                    queue.append(succ_node)
                    visited.add(succ_node)

    def BFS_2_distance(self, node_from: Node, node_to: Node):
        """ BFS with fixed start point and end point

        Args:
            node_from (Node): The current node.
            node_to (Node): The node to move to.

        Returns:
            List[Node]: A list of nodes of the shortest path.
        """
        
        queue = [node_from] # push start node into queue
        visited = set()
        visited.add(node_from)
        dis = {node_from: 0} 
        
        # BFS
        while queue:
            now_node = queue.pop(0) # get the first node in the queue
            now_idx = now_node.get_index()
            
            if now_idx == node_to.get_index(): # found
                return dis[now_node]

            successors = self.get_node(now_idx).get_successors()
            
            for succ in successors:
                succ_node, _, _ = succ
                if succ_node not in visited:
                    queue.append(succ_node)
                    visited.add(succ_node)
                    dis[succ_node] = dis[now_node] + 1

    def ManhattanDistance(self, node_from: Node, node_to: Node):
            """ Calculate Manhattan distance between two nodes.

            Args:
                node_from (Node): The current node.
                node_to (Node): The node to move to.

            Returns:
                int: The Manhattan distance between the two nodes.
            """
            
            maze_height = self.find_maze_height()
            
            node_from_idx = node_from.get_index()
            node_to_idx = node_to.get_index()
            
            x1 = (node_from_idx - 1) // maze_height + 1
            y1 = (node_from_idx - 1) % maze_height + 1
            x2 = (node_to_idx - 1) // maze_height + 1
            y2 = (node_to_idx - 1) % maze_height + 1
            
            return abs(x1 - x2) + abs(y1 - y2)

    def AllManhattanDistance(self, node_marked: Node):
        """ Calculate Manhattan distance between a node and all other nodes.

        Args:
            node_marked (Node): The node we want to calculate the Manhattan distance for.

        Returns:
            list: A list of all Manhattan distances with respect to the given node.
        """
                     
        manhattan_distance_dict = {}
        for i in range(self.total_node_count):
            idx = i + 1
            manhattan_distance_dict[idx] = self.ManhattanDistance(node_marked, self.get_node(idx))
        return manhattan_distance_dict
            
    def get_action(self, car_dir, node_from: Node, node_to: Node) -> Tuple[Action, Direction]:
        """ Get the action required to move from node_from to node_to, given the current car direction.

        Args:
            car_dir (Direction): The current direction the car is facing.
            node_from (Node): The current node.
            node_to (Node): The node to move to.

        Returns:
            Tuple[Action, Direction]: A tuple containing the required action and the new direction after taking the action.
            If node_to is not a valid successor of node_from, returns (None, None).
            
        Note:
            The "turn of Action" in this context stands for turn and advance till next node.
        """
        node_from_idx = node_from.get_index()
        node_to_idx = node_to.get_index()
        
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        
        direction_diff = self.get_node(node_from_idx).get_direction(self.get_node(node_to_idx))
        
        if self.get_node(node_from_idx).is_successor(self.get_node(node_to_idx)):
            
            right_turn_cnt = directions.index(direction_diff) - directions.index(car_dir)
            
            if right_turn_cnt < 0:
                right_turn_cnt += 4  
            
            if right_turn_cnt == 0:
                return Action.ADVANCE, Direction(direction_diff)
            elif right_turn_cnt == 1:
                return Action.TURN_RIGHT, Direction(direction_diff)
            elif right_turn_cnt == 2:
                return Action.U_TURN, Direction(direction_diff)
            elif right_turn_cnt == 3:
                return Action.TURN_LEFT, Direction(direction_diff)
             
        else: 
            log.error(f"Error: Node {node_from_idx} is not adjacent to Node {node_to_idx}.") 
            return None
        
    def get_actions(self, nodes: List[Node]):
        """ Given a sequence of nodes, return the corresponding action sequence.

        Args:
            nodes (List[Node]): A list of nodes representing the path.

        Returns:
            List[Action]: A list of actions required to move along the given path.
        """

        now_direction = self.get_node(nodes[0].get_index()).get_direction(self.get_node(nodes[1].get_index())) # initial direction
        actions = []
        for i in range(len(nodes) - 1):
            action, now_direction = self.get_action(now_direction, nodes[i], nodes[i + 1])
            if action is not None:
                actions.append(action)
            else:
                log.error(f"Error: Could not find action to move from Node {nodes[i].get_index()} to Node {nodes[i + 1].get_index()}")
                break
        return actions

    def actions_to_str(self, actions):
        """ Turn a list of action into a string like "fbrl....", used as the input of BFS checklist #1

        Args:
            actions (List[Action]): A list of actions

        Returns:
            String: command of actions, in which 
                f for advance forward, 
                b for u turn and advance, 
                r for right turn and advance, and
                l for left turn and advance. 
        """
        
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action - 1]
        log.info(cmds)
        return cmds

    def mark_dead_end_explored(self, explored_node: Node):
        """ Changes the explored_dead_end attribute in node_dict to True if the given node is a dead end and is explored.

        Args:
            explored_node (Node): The node detected.
        """
        idx = explored_node.get_index()
        if explored_node.is_dead_end():
            node_obj, is_dead_end, _ = self.node_dict[idx]
            self.node_dict[idx] = (node_obj, is_dead_end, True)
        else:
            log.error("Error: The node is not a dead end.")
        
    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)

if __name__ == "__main__":
    maze = Maze(r"D:\NTU\車車課\Car-Car-Thur-6\python\data\medium_maze.csv") # May plug ones filepath of maze into ""
    print(maze.actions_to_str(maze.get_actions(maze.strategy_2(Node(1), Node(12)))))
    print((maze.BFS_2_distance(Node(6), Node(12))))
    print(maze.AllManhattanDistance(Node(6)))
    print
    '''
    node_num = maze.get_node_number()
    node_dict = maze.get_node_dict()
    for i in node_dict.keys():    
        print(i)
    '''