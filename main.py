"""
Day 84/100 - Tic Tac Toe
Play against a friend or against a computer opponent.
"""

import random

# Constants
WINNING_LINES = (
    (0, 1, 2),  # Top row
    (3, 4, 5),  # Middle row
    (6, 7, 8),  # Bottom row
    (0, 3, 6),  # Left column
    (1, 4, 7),  # Middle column
    (2, 5, 8),  # Right column
    (0, 4, 8),  # Diagonal
    (2, 4, 6),  # Diagonal
)

# Game display function
def display_board(board):
    """Display the game board."""

    cells = [
        board[i] if board[i] else str(i + 1)
        for i in range(9)
    ]

    print()
    print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]} ")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]} ")
    print()


# Game logic functions
def has_won(board, player):
    """Check whether a player has won."""

    for line in WINNING_LINES:
        if all(board[position] == player for position in line):
            return True

    return False


def is_draw(board):
    """Check whether the board is full."""

    return all(board)


def available_moves(board):
    """Return a list of empty board indexes."""

    return [i for i in range(9) if not board[i]]

# Human player input
def get_move(board, player):
    """Get a valid move from a human player."""

    while True:
        choice = input(
            f"Player {player}, choose a position (1-9): "
        ).strip()

        if not choice.isdigit():
            print("Please enter a number between 1 and 9.")
            continue

        position = int(choice)

        if position < 1 or position > 9:
            print("Invalid position. Choose between 1 and 9.")
            continue

        index = position - 1

        if board[index]:
            print("That position is already occupied.")
            continue

        return index


# Bot logic
def minimax(board, current, bot, human):
    """
    Score a position from the bot's point of view.
    +1 = bot wins, -1 = human wins, 0 = draw.
    """

    if has_won(board, bot):
        return 1
    if has_won(board, human):
        return -1
    if is_draw(board):
        return 0

    next_player = human if current == bot else bot
    scores = []

    for move in available_moves(board):
        board[move] = current
        scores.append(minimax(board, next_player, bot, human))
        board[move] = ""  # undo the move

    return max(scores) if current == bot else min(scores)


# Bot strongest move selection
def best_move(board, bot, human):
    """Pick the strongest move using minimax."""

    best_score = -2
    best_choices = []

    for move in available_moves(board):
        board[move] = bot
        score = minimax(board, human, bot, human)
        board[move] = ""

        if score > best_score:
            best_score = score
            best_choices = [move]
        elif score == best_score:
            best_choices.append(move)

    # Choose randomly among equally good moves so games vary
    return random.choice(best_choices)


# Bot move selection based on difficulty
def get_bot_move(board, bot, human, difficulty):
    """Return the bot's move based on the chosen difficulty."""

    if difficulty == "easy":
        # Easy: mostly random, but still takes a win or blocks a loss
        for player in (bot, human):
            for move in available_moves(board):
                board[move] = player
                won = has_won(board, player)
                board[move] = ""
                if won:
                    return move
        return random.choice(available_moves(board))

    return best_move(board, bot, human)


# Game setup
def choose_mode():
    """Ask whether to play a friend or the computer."""

    print("\nGame mode:")
    print("  1. Two players")
    print("  2. Play against the computer")

    while True:
        choice = input("Choose a mode (1-2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Please enter 1 or 2.")


# Bot difficulty selection
def choose_difficulty():
    """Ask for the bot's difficulty."""

    print("\nDifficulty:")
    print("  1. Easy")
    print("  2. Unbeatable")

    while True:
        choice = input("Choose a difficulty (1-2): ").strip()
        if choice == "1":
            return "easy"
        if choice == "2":
            return "hard"
        print("Please enter 1 or 2.")

# Human symbol selection
def choose_symbol():
    """Let the human choose to be X (goes first) or O."""

    while True:
        choice = input("Do you want to be X or O? (X goes first): ").strip().upper()
        if choice in ("X", "O"):
            return choice
        print("Please enter X or O.")

# Game play function
def play_game():
    """Run one complete game."""

    mode = choose_mode()

    bot_player = None
    human_player = None
    difficulty = None

    if mode == "2":
        difficulty = choose_difficulty()
        human_player = choose_symbol()
        bot_player = "O" if human_player == "X" else "X"

    board = [""] * 9
    current_player = "X"

    print("\nWelcome to Tic Tac Toe!")
    print("Player X goes first.")
    print("Choose a position by entering its number.")

    display_board(board)

    while True:
        if current_player == bot_player:
            print(f"Computer ({bot_player}) is thinking...")
            move = get_bot_move(board, bot_player, human_player, difficulty)
            print(f"Computer chooses position {move + 1}.")
        else:
            move = get_move(board, current_player)

        board[move] = current_player

        display_board(board)

        if has_won(board, current_player):
            if mode == "2":
                if current_player == bot_player:
                    print("The computer wins!")
                else:
                    print("You win!")
            else:
                print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Switch players
        current_player = "O" if current_player == "X" else "X"


# Allow players to play multiple rounds
def main():
    """Allow players to play multiple rounds."""

    while True:
        play_game()

        again = input(
            "Would you like to play again? (y/n): "
        ).strip().lower()

        if again not in ("y", "yes"):
            print("Thanks for playing Tic Tac Toe!")
            break


# Run the Application
if __name__ == "__main__":
    main()