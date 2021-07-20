from AI import *
import numpy as np


def alphabeta(board, depth, a=-1000, b=1000, maxPlayer=True):
    if depth == 0:
        return (hurestic(board, 2) - hurestic(board, 1))
    toPlay = 2 if maxPlayer else 1
    if winning_move(board, toPlay):
        if(toPlay == 2):
            return 100
        else:
            return -100
    if maxPlayer:
        v = -1000000
        for i in range(7):
            if is_valid_location(board, i):
                row = get_next_open_row(board, i)
                b1 = np.copy(board)
                drop_piece(b1, row, i, 2)
                print("Max")
                print(b1)
                v = max(v, alphabeta(b1, depth-1, a, b, False))
                a = max(a, v)
            if b <= a:
                break
        return v
    else:
        v = 1000000
        for i in range(7):
            if is_valid_location(board, i):
                row = get_next_open_row(board, i)
                b1 = np.copy(board)
                drop_piece(b1, row, i, 1)
                print("Min")
                print(b1)
                v = min(v, alphabeta(b1, depth-1, a, b, True))
                b = min(b, v)
            if b <= a:
                break
        return v


brd = create_board()
f = alphabeta(brd, 8, -1000, +1000, True)

