class Node:
    def __init__(self, data, board, col):
        self.v = data
        self.child = None
        self.board = board
        self.col = col
    def addToTree(self, v, board, col):
        if self.child is None:
            self.child = list()
        self.child.append(Node(v, board, col))
