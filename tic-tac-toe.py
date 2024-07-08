import pygame
import random

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define the window dimensions
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 350  # Decreased height after removing the button

# Define the cell dimensions
CELL_SIZE = 100

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Function to draw the Tic-Tac-Toe board with text-based representations
def draw_board(board, outcome=None):
    window.fill(WHITE)

    # Draw vertical lines
    pygame.draw.line(window, BLACK, (CELL_SIZE, 0), (CELL_SIZE, WINDOW_HEIGHT - 50), 4)
    pygame.draw.line(window, BLACK, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, WINDOW_HEIGHT - 50), 4)

    # Draw horizontal lines
    pygame.draw.line(window, BLACK, (0, CELL_SIZE), (WINDOW_WIDTH, CELL_SIZE), 4)
    pygame.draw.line(window, BLACK, (0, CELL_SIZE * 2), (WINDOW_WIDTH, CELL_SIZE * 2), 4)

    # Draw X and O symbols as text with color
    font = pygame.font.Font(None, 120)
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                color = RED if outcome == "X" else BLACK
                text_surface = font.render("X", True, color)
                window.blit(text_surface, (col * CELL_SIZE + 30, row * CELL_SIZE))
            elif board[row][col] == "O":
                color = BLUE if outcome == "O" else BLACK
                text_surface = font.render("O", True, color)
                window.blit(text_surface, (col * CELL_SIZE + 30, row * CELL_SIZE))

    pygame.display.update()

# Function to handle the user's move
def player_move(board, x, y):
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if board[row][col] == " ":
        board[row][col] = "X"  # Player's move
        return True
    return False

# Function to check if the game is over and determine the outcome
def game_over(board):
    # Check for a winning condition
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]  # Return the winning symbol ("X" or "O")
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]  # Return the winning symbol ("X" or "O")
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]  # Return the winning symbol ("X" or "O")
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]  # Return the winning symbol ("X" or "O")

    # Check for a draw condition
    for row in board:
        if " " in row:
            return None  # Game not over yet
    return "Draw"  # Draw condition

# Function to generate all possible moves
def generate_moves(board):
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                moves.append((row, col))
    return moves

# Function to evaluate the score of a board state
def evaluate(board):
    outcome = game_over(board)
    if outcome == "X":
        return 1  # Player wins
    elif outcome == "O":
        return -1  # Computer wins
    return 0  # Draw

# Function to find the best move using the minimax algorithm
def minimax(board, depth, maximizing_player):
    outcome = game_over(board)
    if depth == 0 or outcome:
        if outcome == "O":
            return 10  # Favorable outcome for the computer
        elif outcome == "X":
            return -10  # Unfavorable outcome for the computer
        return 0  # Draw condition

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(board):
            row, col = move
            board[row][col] = "O"  # Computer's move
            eval = minimax(board, depth - 1, False)
            board[row][col] = " "  # Undo the move
            max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = float('inf')
        for move in generate_moves(board):
            row, col = move
            board[row][col] = "X"  # Player's move
            eval = minimax(board, depth - 1, True)
            board[row][col] = " "  # Undo the move
            min_eval = min(min_eval, eval)
        return min_eval

# Function to find the best move using the chosen difficulty level
def computer_move(board, difficulty):
    if difficulty == "easy":
        moves = generate_moves(board)
        if moves:
            return random.choice(moves)
        else:
            return None  # No available moves

    elif difficulty == "medium":
        best_score = float('-inf')
        best_move = None
        for move in generate_moves(board):
            row, col = move
            board[row][col] = "O"  # Computer's move
            score = minimax(board, 4, False)  # Medium depth for medium difficulty
            board[row][col] = " "  # Undo the move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    elif difficulty == "impossible":
        best_score = float('-inf')
        best_move = None
        for move in generate_moves(board):
            row, col = move
            board[row][col] = "O"  # Computer's move
            score = minimax(board, 9, False)  # Higher depth for impossible difficulty
            board[row][col] = " "  # Undo the move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

# Function to start the game
def play_game(difficulty):
    board = [[" " for _ in range(3)] for _ in range(3)]
    outcome = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over(board):
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        if player_move(board, x, y):  # Check if the player made a move
                            outcome = game_over(board)
                            if not outcome:
                                move = computer_move(board, difficulty)
                                if move:
                                    row, col = move
                                    board[row][col] = "O"  # Computer's move
                                    outcome = game_over(board)

        draw_board(board, outcome)

        if outcome:
            running = False

    # Display the result of the game
    result_text = ""
    if outcome == "X":
        result_text = "Player wins!"
    elif outcome == "O":
        result_text = "Computer wins!"
    elif outcome == "Draw":
        result_text = "It's a draw!"

    font = pygame.font.Font(None, 40)
    text_surface = font.render(result_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(text_surface, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Define the button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Function to display the difficulty selection screen
def select_difficulty():
    window.fill(WHITE)

    font = pygame.font.Font(None, 36)
    text_surface = font.render("Select Difficulty", True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(text_surface, text_rect)

    # Adjusted Y-coordinates for the buttons
    easy_button = pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(window, BLUE, easy_button)
    easy_text = font.render("Easy", True, WHITE)
    easy_text_rect = easy_text.get_rect(center=(WINDOW_WIDTH // 2, 175))
    window.blit(easy_text, easy_text_rect)

    medium_button = pygame.Rect(50, 225, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(window, BLUE, medium_button)
    medium_text = font.render("Medium", True, WHITE)
    medium_text_rect = medium_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
    window.blit(medium_text, medium_text_rect)

    impossible_button = pygame.Rect(50, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    impossible_button = pygame.Rect(50, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(window, BLUE, impossible_button)
    impossible_text = font.render("Impossible", True, WHITE)
    impossible_text_rect = impossible_text.get_rect(center=(WINDOW_WIDTH // 2, 325))
    window.blit(impossible_text, impossible_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button.collidepoint(x, y):
                    play_game("easy")
                elif medium_button.collidepoint(x, y):
                    play_game("medium")
                elif impossible_button.collidepoint(x, y):
                    play_game("impossible")

# Start the game by displaying the difficulty selection screen
select_difficulty()
