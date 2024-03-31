import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas 

from node import Direction, Node

log = logging.getLogger(__name__)


class Action(IntEnum):
    # Note that the turn in this context stands for turn and advance till next node
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    # TODO: determine when and where to record explored dead end
    
    def __init__(self, filepath: str):
        """
        # read csv file
        # every node records all its successor
        # store these objects into self.nodes.
        # add to nd_dict by {key(index): value(corresponding node)}
        
        Note:
            For idx of self.nodes, ix = idx
            For real index of node, real_idx - 1 = ix = idx
        """
        
        self.raw_data = pandas.read_csv(filepath).values # read csv file into a numpy array
        self.nodes = [] 
        self.node_dict = dict()  # key: index, value: the correspond node
        self.explored_dead_end_dict = dict()
        
        rows = self.raw_data.shape[0]
        cols = 5; # index, North, South, West, East
        
        for ix in range(rows): 
            index = int(self.raw_data[ix, 0])
            node = Node(index)
            self.nodes.append(node)
            self.node_dict[index] = node # add to nd_dict by {key(index): value(corresponding node)}
        
        for ix in range(rows):    
            for iy in range(1, cols): # iy stands for NORTH = 1, SOUTH = 2. WEST = 3, EAST = 4
                
                # make NaN = 0
                if self.raw_data[ix,iy] == self.raw_data[ix,iy]:
                    cell_read = int(self.raw_data[ix,iy])
                else:
                    cell_read = 0
                
                # adjacency list
                if (cell_read): # if cell_read isn't empty (i.e. NaN) 
                    self.nodes[ix].set_successor(self.nodes[cell_read - 1], iy)        

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict
    
    def backtrace(self, parent: Node, node_from: Node, node_to: Node):
        """ tracks path by finding parents till the start node
            
        Args:
            parent (Node): a dictionary that records every node's parent
            node_from (Node): The current node.
            node_to (Node): The node to move to.

        Returns:
            List[Node]: A list of nodes that tracks the path.
        """
        
        print("backtrace called")
        
        path = [node_to]
        while path[-1] != node_from:
            idx = path[-1].get_index()
            path.append(parent[idx])
            
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
            
            if self.get_node_dict()[now_idx].is_dead_end() & self.get_node_dict()[now_idx] not in self.explored_dead_end_dict: # found
                self.explored_dead_end_dict[now_idx] = self.get_node_dict()[now_idx] # 
                return self.backtrace(parent, node, self.get_node_dict()[now_idx])

            successors = self.get_node_dict()[now_idx].get_successors()
            
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
        # dis = {node_from: 0} if distance is needed, ill write another function for it
        
        # BFS
        while queue:
            now_node = queue.pop(0) # get the first node in the queue
            now_idx = now_node.get_index()
            
            if now_idx == node_to.get_index(): # found
                # return dis[now_node]
                return self.backtrace(parent, node_from, node_to)

            successors = self.get_node_dict()[now_idx].get_successors()
            
            for succ in successors:
                succ_node, _, _ = succ
                if succ_node not in visited:
                    parent[succ_node.get_index()] = now_node
                    queue.append(succ_node)
                    visited.add(succ_node)
                    # dis[succ_node] = dis[now_node] + 1

    def getAction(self, car_dir, node_from: Node, node_to: Node):
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
        
        direction_diff = self.get_node_dict()[node_from_idx].get_direction(self.get_node_dict()[node_to_idx])
        
        if self.get_node_dict()[node_from_idx].is_successor(self.get_node_dict()[node_to_idx]):
            
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
            return 0
        

    def getActions(self, nodes: List[Node]):
        """ Given a sequence of nodes, return the corresponding action sequence.

        Args:
            nodes (List[Node]): A list of nodes representing the path.

        Returns:
            List[Action]: A list of actions required to move along the given path.
        """

        now_direction = self.get_node_dict()[nodes[0].get_index()].get_direction(self.get_node_dict()[nodes[1].get_index()]) # initial direction
        actions = []
        for i in range(len(nodes) - 1):
            action, now_direction = self.getAction(now_direction, nodes[i], nodes[i + 1])
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
            string: command of actions, in which 
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

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)

maze = Maze(r"") # May plug ones filepath of maze into ""
print(maze.actions_to_str(maze.getActions(maze.strategy_2(Node(1),Node(12)))))