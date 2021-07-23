import numpy as np
import pygame

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

RED_PLAYER = 1
YELLOW_PLAYER = 2

RED_TURN = 0
YELLOW_TURN = 1

ROW_COUNT = 6
COLUMN_COUNT = 7
ConnectNum = 4

EASY = 2
MEDIUM = 4
HARD = 5

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def is_filled(board):
    filled = True
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                filled = False
    return filled


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            winner = True
            for i in range(4):
                winner = (board[r][c+i] == piece) and winner
                if not winner:
                    break
            if winner:
                return winner

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            winner = True
            for i in range(ConnectNum):
                winner = winner and (board[r+i][c] == piece)
                if not winner:
                    break
            if winner:
                return winner

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            winner = True
            for i in range(ConnectNum):
                winner = winner and (board[r + i][c+i] == piece)
                if not winner:
                    break
            if winner:
                return winner

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ConnectNum-1, ROW_COUNT):
            winner = True
            for i in range(ConnectNum):
                winner = winner and (board[r - i][c + i] == piece)
                if not winner:
                    break
            if winner:
                return winner


def heuristic(board, piece):
    # Check horizontal locations for win
    count = 0
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            winner = True
            for i in range(4):
                winner = (board[r][c+i] == piece or board[r][c+i] == 0) and winner
                if not winner:
                    break
            if winner:
                count += 1

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            winner = True
            for i in range(ConnectNum):
                winner = (winner and (board[r+i][c] == piece or board[r+i][c] == 0))
                if not winner:
                    break
            if winner:
                count += 1

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            winner = True
            for i in range(ConnectNum):
                winner = winner and (board[r + i][c+i] == piece or board[r+i][c+i] == 0)
                if not winner:
                    break
            if winner:
                count += 1

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ConnectNum-1, ROW_COUNT):
            winner = True
            for i in range(ConnectNum):
                winner = winner and (board[r - i][c + i] == piece or board[r - i][c + i] == 0)
                if not winner:
                    break
            if winner:
                count += 1
    return count


def count_tree(root):
    if root is None:
        return 0
    if root.child is None:
        return 1
    summation = 0
    for node in root.child:
        summation += count_tree(node)
    return summation + 1


def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, WHITE, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == RED_PLAYER:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == YELLOW_PLAYER:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def next_move(origin, f):
    to_play_col = 0
    for col in range(len(origin.child)):
        if origin.child[col].v == f:
            to_play_col = origin.child[col].col
            break
    return to_play_col
