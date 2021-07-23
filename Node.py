import numpy as np


class Node:
    def __init__(self, data, board, col):
        self.v = data
        self.child = None
        self.board = board
        self.col = col

    def add_to_tree(self, v, board, col):
        if self.child is None:
            self.child = list()
        self.child.append(Node(v, board, col))
