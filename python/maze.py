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
        
        for ix in range(1, rows): # the first row of csv is string, so for idx of self.nodes, ix = idx + 1
            index = int(self.raw_data[ix, 0])
            node = Node(index)
            self.nodes.append(node)
            self.node_dict[index] = node # add to nd_dict by {key(index): value(corresponding node)}
        
        for ix in range(1, rows):    
            for iy in range(1, cols): # iy stands for NORTH = 1, SOUTH = 2. WEST = 3, EAST = 4
                cell_read = int(self.raw_data[ix,iy])
                
                # adjacency list
                if not (cell_read.isnan()): # if cell_read isn't empty (i.e. NaN) 
                    self.nodes[ix - 1].set_successor(self.nodes[cell_read - 1], iy)        

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored dead end
        return None

    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        return None

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
