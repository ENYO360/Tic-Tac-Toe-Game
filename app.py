from flask import Flask, jsonify, render_template, request

from game import DIFFICULTIES, get_bot_move

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/bot-move")
def bot_move():
    """The browser sends the board; the server replies with the bot's move."""
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    bot = data.get("bot")
    difficulty = data.get("difficulty")

    valid = (
        isinstance(board, list)
        and len(board) == 9
        and all(cell in ("", "X", "O") for cell in board)
        and "" in board
        and bot in ("X", "O")
        and difficulty in DIFFICULTIES
    )
    if not valid:
        return jsonify(error="Invalid request"), 400

    human = "O" if bot == "X" else "X"
    return jsonify(move=get_bot_move(tuple(board), bot, human, difficulty))


if __name__ == "__main__":
    app.run(debug=True)
