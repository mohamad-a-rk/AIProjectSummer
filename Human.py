from BoardFunctions import *
from random import randint
import math


def play_game_h():
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

                if turn == RED_TURN:
                    pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                # Ask for Player 1 Input
                if turn == RED_TURN:
                    pos_x = event.pos[0]
                    to_play_col = int(math.floor(pos_x / SQUARE_SIZE))
                    if is_valid_location(board, to_play_col):
                        row = get_next_open_row(board, to_play_col)
                        drop_piece(board, row, to_play_col, RED_PLAYER)

                        if winning_move(board, RED_PLAYER):
                            label = my_font.render('Player 1 wins!', True, RED)
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
