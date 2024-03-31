from enum import IntEnum


# You can get the enumeration based on integer value, or make comparison
# ex: d = Direction(1), then d would be Direction.NORTH
# ex: print(Direction.SOUTH == 1) should return False
class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


# Construct class Node and its member functions
# You may add more member functions to meet your needs
class Node:
    def __init__(self, index: int = 0):
        self.index = index
        # successor is a list with tuple (Node, direction to node, distance)
        self.successors = [] 

    def get_index(self):
        return self.index

    def get_successors(self):
        return self.successors

    def set_successor(self, successor, direction, length=1):
        self.successors.append((successor, Direction(direction), int(length)))
        # print(f"For Node {self.index}, a successor {self.successors[-1]} is set.") what does the [-1] means
        print(f"For Node {self.index}, a successor Node {self.successors[-1][0].get_index()} is set.") 
        return

    def get_direction(self, node):
        """
        # if node is adjacent to the present node, return the direction of node from the present node
        # For example, if the direction of node from the present node is EAST, then return Direction.EAST = 4
        # However, if node is not adjacent to the present node, print error message and return 0
        """
        
        for succ in self.successors:
            if succ[0] == node:
                return succ[1]
        print(f"Error: Node {node.index} is not adjacent to Node {self.index}.")
        return 0

    def is_successor(self, node):
        for succ in self.successors:
            if succ[0] == node:
                return True
        return False
    
    def is_dead_end(self, node):
        if len(node.get_successors()) == 1:
            return True
        else:
            return False
    
    def successor_print(self):
        for succ in self.successors:
            print(succ[0].get_index())

"""
# Test cases
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

# Set successors for node1
node1.set_successor(node2, 4)
node1.set_successor(node3, 2)


# print the successors' idx
node1.successor_print()

# check successors
print(node1.get_successors()[1][2])

# Check if node4 is a successor of node1
print(node1.is_successor(node4))  # Output: False

# Get the direction of node2 from node1
direction = node1.get_direction(node2)
print(direction)  # Output: Direction.EAST

# Get the direction of node4 from node1 (not a successor)
direction = node1.get_direction(node4)
# Output: Error: Node 4 is not adjacent to Node 1.
#         0

# Check Direction enumeration values
print(Direction.SOUTH == 1)  # Output: False
print(Direction.SOUTH == 2)  # Output: True
"""