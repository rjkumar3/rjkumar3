import pygame
import numpy as np
import sys

try:
    pygame.init()
except pygame.error as e:
    print(f"Failed to initialize Pygame: {e}") #error handling
    sys.exit()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (180, 180, 180)
GREEN = (0, 255, 0)

WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe Minmax')
except pygame.error as e:
    print(f"Failed to set up display: {e}") #error handling
    pygame.quit()
    sys.exit()

screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 1:
                pygame.draw.line(screen, RED, (column * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (column * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (column * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (column * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, column, player):
    board[row][column] = player

def available_square(row, column):
    return board[row][column] == 0

def is_board_full(check_board=board):
    return not np.any(check_board == 0)

def check_win(player, check_board=board):
    for column in range(BOARD_COLUMNS):
        if np.all(check_board[:, column] == player):
            return True
    for row in range(BOARD_ROWS):
        if np.all(check_board[row, :] == player):
            return True
    if np.all(np.diag(check_board) == player):
        return True
    if np.all(np.diag(np.fliplr(check_board)) == player):
        return True
    return False

def minmax(minmax_board, depth, is_maximizing):
    if check_win(2, minmax_board):
        return 1
    elif check_win(1, minmax_board):
        return -1
    elif is_board_full(minmax_board):
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if minmax_board[row][column] == 0:
                    minmax_board[row][column] = 2
                    score = minmax(minmax_board, depth + 1, False)
                    minmax_board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if minmax_board[row][column] == 0:
                    minmax_board[row][column] = 1
                    score = minmax(minmax_board, depth + 1, True)
                    minmax_board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def find_best_move():
    best_move = (-1, -1)
    best_value = -float('inf')
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 0:
                board[row][column] = 2
                move_value = minmax(board, 0, False)
                board[row][column] = 0
                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, column)
    return best_move

def display_message(message, color):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

def main():
    global board
    draw_lines()
    pygame.display.update()

    while True:
        board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
        draw_lines()
        pygame.display.update()

        player_turn = True
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE
                    if available_square(mouseY, mouseX):
                        mark_square(mouseY, mouseX, 1)
                        if check_win(1):
                            game_over = True
                        elif is_board_full():
                            game_over = True
                        else:
                            player_turn = False

                if not player_turn and not game_over:
                    move = find_best_move()
                    if move != (-1, -1):
                        mark_square(move[0], move[1], 2)
                        if check_win(2):
                            game_over = True
                        elif is_board_full():
                            game_over = True
                    player_turn = True

                draw_figures()
                pygame.display.update()

            if game_over:
                screen.fill(GREY)
                draw_lines()
                draw_figures()
                if check_win(1):
                    display_message("Player X wins!", GREEN)
                elif check_win(2):
                    display_message("Player O wins!", RED)
                else:
                    display_message("It's a draw!", WHITE)
                pygame.time.wait(2000)

                screen.fill(BLACK)
                draw_lines()
                pygame.display.update()

if __name__ == "__main__":
    main()
