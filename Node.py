import numpy as np


class Node:
    def __init__(self, data, board, col, a=np.NINF, b=np.PINF):
        self.v = data
        self.child = None
        self.board = board
        self.col = col
        self.a = a
        self.b = b

    def add_to_tree(self, v, board, col, a, b):
        if self.child is None:
            self.child = list()
        self.child.append(Node(v, board, col, a, b))
