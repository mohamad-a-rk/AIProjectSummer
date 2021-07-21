from AI import *
import numpy as np


def alpha_beta(board, depth, a=-1000, b=1000, max_player=True):
    if depth == 0:
        return heuristic(board, RED_PLAYER) - heuristic(board, YELLOW_PLAYER)
    to_play = RED_PLAYER if max_player else YELLOW_PLAYER
    if winning_move(board, to_play):
        if to_play == RED_PLAYER:
            return 100
        else:
            return -100
    if max_player:
        v = -1000000
        for i in range(7):
            if is_valid_location(board, i):
                row = get_next_open_row(board, i)
                b1 = np.copy(board)
                drop_piece(b1, row, i, RED_PLAYER)
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
                drop_piece(b1, row, i, YELLOW_PLAYER)
                print("Min")
                print(b1)
                v = min(v, alpha_beta(b1, depth - 1, a, b, True))
                print(v)
                b = min(b, v)
            if b <= a:
                break
        return v


brd = create_board()
# origin = Node(-1000, brd)
f = alpha_beta(brd, 4, -1000, +1000, True)
i = 0
print("f is {0}".format(f))
# for i in range(len(origin.child)):
#     if origin.child[i].v == f:
#         break
# print(" I is")
# print(i)
# for c in origin.child:
#     print(c.v)

