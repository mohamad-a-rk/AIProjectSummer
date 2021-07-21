from AI import *
import numpy as np


def alpha_beta(board, depth, a=-1000, b=1000, max_player=True):
    if depth == 0:
        return heuristic(board, 2) - heuristic(board, 1)
    to_play = 2 if max_player else 1
    if winning_move(board, to_play):
        if to_play == 2:
            return 100
        else:
            return -100
    if max_player:
        v = -1000000
        for i in range(7):
            if is_valid_location(board, i):
                row = get_next_open_row(board, i)
                b1 = np.copy(board)
                drop_piece(b1, row, i, 2)
                print("Max")
                print(b1)
                v = max(v, alpha_beta(b1, depth - 1, a, b, False))
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
                v = min(v, alpha_beta(b1, depth - 1, a, b, True))
                b = min(b, v)
            if b <= a:
                break
        return v


brd = create_board()
f = alpha_beta(brd, 8, -1000, +1000, True)
