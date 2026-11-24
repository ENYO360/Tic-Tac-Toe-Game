"""Tic Tac Toe game logic and bot players (no Flask code in here)."""

import random
from functools import lru_cache

WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
)

DIFFICULTIES = ("easy", "medium", "hard")


def winner(board):
    """Return 'X' or 'O' if someone has won, otherwise None."""
    for a, b, c in WINNING_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if not cell]


@lru_cache(maxsize=None)
def minimax(board, current, bot, human):
    """Score a position for the bot: +1 bot wins, -1 human wins, 0 draw.
    `board` is a tuple so results can be cached (makes the bot instant)."""
    won = winner(board)
    if won == bot:
        return 1
    if won == human:
        return -1
    if all(board):
        return 0

    next_player = human if current == bot else bot
    scores = [
        minimax(board[:m] + (current,) + board[m + 1:], next_player, bot, human)
        for m in available_moves(board)
    ]
    return max(scores) if current == bot else min(scores)


def best_move(board, bot, human):
    """Pick a perfect move; ties are broken randomly so games vary."""
    best_score, choices = -2, []
    for m in available_moves(board):
        child = board[:m] + (bot,) + board[m + 1:]
        score = minimax(child, human, bot, human)
        if score > best_score:
            best_score, choices = score, [m]
        elif score == best_score:
            choices.append(m)
    return random.choice(choices)


def easy_move(board, bot, human):
    """Take a win or block a loss if possible, otherwise play randomly."""
    for player in (bot, human):
        for m in available_moves(board):
            if winner(board[:m] + (player,) + board[m + 1:]) == player:
                return m
    return random.choice(available_moves(board))


def get_bot_move(board, bot, human, difficulty):
    """board is a tuple of 9 values: '', 'X' or 'O'."""
    if difficulty == "easy":
        return easy_move(board, bot, human)
    if difficulty == "medium":
        # 50% perfect play, 50% completely random
        if random.random() < 0.5:
            return best_move(board, bot, human)
        return random.choice(available_moves(board))
    return best_move(board, bot, human)
