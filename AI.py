import math
from BoardFunctions import *
import pygame
from Node import Node
from random import randint


def play_game(difficulty=EASY):
    board = create_board()
    screen = pygame.display.set_mode(size)
    pygame.init()
    game_over = False
    draw_board(screen, board)
    pygame.display.update()

    turn = randint(RED_TURN, YELLOW_TURN)
    my_font = pygame.font.SysFont('monospace', 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn == YELLOW_TURN:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if turn == RED_TURN:
                pygame.time.wait(500)
                origin = Node(-1000, board, 0)
                f = alpha_beta(origin, difficulty, np.NINF, np.Inf, True)
                to_play_col = next_move(origin, f)
                if is_valid_location(board, to_play_col):
                    row = get_next_open_row(board, to_play_col)
                    drop_piece(board, row, to_play_col, RED_PLAYER)

                    if winning_move(board, RED_PLAYER):
                        label = my_font.render('Player 1 wins!', True, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                else:
                    continue
                draw_board(screen, board)
                turn += 1
                turn = turn % 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                # Ask for Player 2 Input
                if turn == YELLOW_TURN:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, YELLOW_PLAYER)

                        if winning_move(board, YELLOW_PLAYER):
                            label = my_font.render('Player 2 wins!', True, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        continue

                if is_filled(board):
                    label = my_font.render('Tie!', True, BLUE)
                    screen.blit(label, (width / 2 - 60, 10))
                    game_over = True

                draw_board(screen, board)
                turn += 1
                turn = turn % 2

            if game_over:
                pygame.time.wait(5000)
                pygame.display.quit()


def alpha_beta(root, depth, a=np.NINF, b=np.Inf, max_player=True):
    to_play = RED_PLAYER if max_player else YELLOW_PLAYER

    if winning_move(root.board, to_play):
        if to_play == RED_PLAYER:
            return 100
        else:
            return -100

    if depth == 0:
        return heuristic(root.board, RED_PLAYER) - heuristic(root.board, YELLOW_PLAYER)

    if max_player:
        root.v = np.NINF
        for col in range(7):
            if is_valid_location(root.board, col):
                row = get_next_open_row(root.board, col)
                b1 = np.copy(root.board)
                drop_piece(b1, row, col, RED_PLAYER)
                root.add_to_tree(root.v, b1, col)
                root.v = max(root.v, alpha_beta(root.child[-1], depth - 1, a, b, False))
                a = max(a, root.v)
            if b <= a:
                break
        return root.v

    else:
        root.v = np.Inf
        for col in range(7):
            if is_valid_location(root.board, col):
                row = get_next_open_row(root.board, col)
                b1 = np.copy(root.board)
                drop_piece(b1, row, col, YELLOW_PLAYER)
                root.add_to_tree(root.v, b1, col)
                root.v = min(root.v, alpha_beta(root.child[-1], depth - 1, a, b, True))
                b = min(b, root.v)
            if b <= a:
                break
        return root.v
