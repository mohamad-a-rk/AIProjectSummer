import numpy as np
import pygame
import math

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
ConnectNum = 4


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
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)


def play_game():
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
                    pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = my_font.render("Player 1 wins!", True, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        continue

                # # Ask for Player 2 Input
                else:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
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
