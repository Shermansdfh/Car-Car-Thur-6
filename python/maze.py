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
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath: str):
        """
        # read csv file
        # every node records all its successor
        # store these objects into self.nodes.
        # add to nd_dict by {key(index): value(corresponding node)}
        """
        
        self.raw_data = pandas.read_csv(filepath).values # read csv file into a numpy array
        self.nodes = [] 
        self.node_dict = dict()  # key: index, value: the correspond node
        
        rows = self.raw_data.shape[0]
        cols = 5; # index, North, South, West, East
        
        # for idx of self.nodes, ix = idx
        # for real index - 1 = ix = idx
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
        print("backtrace called")
        path = [node_to]
        while path[-1] != node_from:
            idx = path[-1].get_index()
            path.append(parent[idx])
        path.reverse()
        return path

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored dead end
        return None

    def BFS_2(self, node_from: Node, node_to: Node):
        # BFS with fixed start point and end point
        # return a sequence of nodes of the shortest path
        
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

            successors = self.node_dict[now_idx].get_successors()
            
            for succ in successors:
                succ_node, _, _ = succ
                if succ_node not in visited:
                    parent[succ_node.get_index()] = now_node
                    queue.append(succ_node)
                    visited.add(succ_node)
                    # dis[succ_node] = dis[now_node] + 1

    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0
        return None

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        return None

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
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

maze = Maze(r"C:\Users\88696\Downloads\maze.csv")
seq = maze.strategy_2(Node(1),Node(8))
for i in range(len(seq)):
    print(seq[i].get_index())