import numpy as np
import pygame
import math
from Node import Node

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

RED_PLAYER = 1
YELLOW_PLAYER = 2

ROW_COUNT = 6
COLUMN_COUNT = 7
ConnectNum = 4

ONE_VS_ONE = 0
EASY = 2
MEDIUM = 4
HARD = 5


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

############################


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


SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)


def play_game(difficulty=ONE_VS_ONE):
    board = create_board()

    screen = pygame.display.set_mode(size)
    pygame.init()
    game_over = False
    draw_board(screen, board)
    pygame.display.update()

    turn = 0
    my_font = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]

                if turn == 0:
                    if difficulty == ONE_VS_ONE:
                        pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    to_play_col = 0
                    if difficulty == ONE_VS_ONE:
                        pos_x = event.pos[0]
                        to_play_col = int(math.floor(pos_x / SQUARE_SIZE))
                    else:
                        origin = Node(-1000, board, 0)
                        f = alpha_beta(origin, difficulty, -1000, +1000, True)
                        for col in range(len(origin.child)):
                            if origin.child[col].v == f:
                                to_play_col = origin.child[col].col
                                break
                            else:
                                print(origin.child[col].v)
                        print(f'F is {f} and col is {len(origin.child)} and v is {origin.child[to_play_col]}'
                              f'number of leafs is {count_tree(origin)}')
                    if is_valid_location(board, to_play_col):
                        row = get_next_open_row(board, to_play_col)
                        drop_piece(board, row, to_play_col, RED_PLAYER)

                        if winning_move(board, RED_PLAYER):
                            label = my_font.render("Player 1 wins!", True, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        continue

                # Ask for Player 2 Input
                else:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, YELLOW_PLAYER)

                        if winning_move(board, YELLOW_PLAYER):
                            label = my_font.render("Player 2 wins!", True, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        continue

                draw_board(screen, board)
                turn += 1
                turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
                pygame.display.quit()


def alpha_beta(root, depth, a=-1000, b=1000, max_player=True):
    to_play = RED_PLAYER if max_player else YELLOW_PLAYER

    if winning_move(root.board, to_play):
        if to_play == RED_PLAYER:
            return 100
        else:
            return -100

    if depth == 0:
        return heuristic(root.board, RED_PLAYER) - heuristic(root.board, YELLOW_PLAYER)

    if max_player:
        root.v = -1000000
        i = 0
        for col in range(7):
            if is_valid_location(root.board, col):
                row = get_next_open_row(root.board, col)
                b1 = np.copy(root.board)
                drop_piece(b1, row, col, RED_PLAYER)
                # print("Max")
                # print(b1)
                root.add_to_tree(root.v, b1, col)
                root.v = max(root.v, alpha_beta(root.child[i], depth - 1, a, b, False))
                i += 1
                a = max(a, root.v)
            if b <= a:
                break
        return root.v

    else:
        root.v = 1000000
        col = 0
        for i in range(7):
            if is_valid_location(root.board, i):
                row = get_next_open_row(root.board, i)
                b1 = np.copy(root.board)
                drop_piece(b1, row, i, YELLOW_PLAYER)
                # print("Min")
                # print(b1)
                root.add_to_tree(root.v, b1, i)
                root.v = min(root.v, alpha_beta(root.child[col], depth - 1, a, b, True))
                col += 1
                b = min(b, root.v)
            if b <= a:
                break
        return root.v


def count_tree(root):
    if root is None:
        return 0
    if root.child is None:
        return 1
    summation = 0
    for node in root.child:
        summation += count_tree(node)
    return summation + 1