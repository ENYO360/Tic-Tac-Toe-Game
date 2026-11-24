const LINES = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
const $ = (sel) => document.querySelector(sel);

const settings = { mode: "bot", difficulty: "medium", human: "X" };
const state = { board: [], turn: "X", over: false, busy: false, winLine: [], round: 0, error: "" };
let scores = loadScores();

/* ---------- scores (saved in this browser) ---------- */
function loadScores() {
  try { return JSON.parse(localStorage.getItem("ttt-scores")) || { X: 0, O: 0, draw: 0 }; }
  catch { return { X: 0, O: 0, draw: 0 }; }
}
function saveScores() {
  try { localStorage.setItem("ttt-scores", JSON.stringify(scores)); } catch {}
}

/* ---------- helpers ---------- */
const isBotMode = () => settings.mode === "bot";
const isBotTurn = () => isBotMode() && state.turn !== settings.human;

function name(sym) {
  if (!isBotMode()) return `Player ${sym}`;
  return sym === settings.human ? "You" : "Computer";
}
function findWin() {
  return LINES.find(([a, b, c]) => state.board[a] && state.board[a] === state.board[b] && state.board[a] === state.board[c]) || [];
}

/* ---------- drawing ---------- */
const boardEl = $("#board");
const cells = Array.from({ length: 9 }, (_, i) => {
  const btn = document.createElement("button");
  btn.addEventListener("click", () => play(i));
  boardEl.appendChild(btn);
  return btn;
});

function statusText() {
  if (state.error) return state.error;
  if (state.winLine.length) { const n = name(state.turn); return `${n} ${n === "You" ? "win" : "wins"}!`; }
  if (state.over) return "It's a draw.";
  if (state.busy) return "Computer is thinking…";
  return isBotMode() ? `Your turn (${settings.human})` : `${name(state.turn)}’s turn`;
}

function render() {
  cells.forEach((btn, i) => {
    const v = state.board[i];
    btn.textContent = v;
    btn.className = "cell" + (v ? " " + v.toLowerCase() : "") + (state.winLine.includes(i) ? " win" : "");
    btn.disabled = Boolean(v) || state.over || state.busy || isBotTurn();
    btn.setAttribute("aria-label", `Position ${i + 1}, ${v || "empty"}`);
  });
  $("#scoreX").textContent = scores.X;
  $("#scoreO").textContent = scores.O;
  $("#scoreDraw").textContent = scores.draw;
  $("#labelX").textContent = isBotMode() ? (settings.human === "X" ? "You (X)" : "Computer (X)") : "Player X";
  $("#labelO").textContent = isBotMode() ? (settings.human === "O" ? "You (O)" : "Computer (O)") : "Player O";
  $(".settings").classList.toggle("pvp", !isBotMode());
  $("#status").textContent = statusText();
}

/* ---------- game flow ---------- */
function startRound() {
  state.round++;
  Object.assign(state, { board: Array(9).fill(""), turn: "X", over: false, busy: false, winLine: [], error: "" });
  render();
  if (isBotTurn()) botMove();
}

function place(i) {
  state.board[i] = state.turn;
  const line = findWin();
  if (line.length) {
    state.over = true; state.winLine = line; scores[state.turn]++; saveScores();
  } else if (state.board.every(Boolean)) {
    state.over = true; scores.draw++; saveScores();
  } else {
    state.turn = state.turn === "X" ? "O" : "X";
  }
  render();
  if (!state.over && isBotTurn()) botMove();
}

function play(i) {
  if (state.over || state.busy || state.board[i] || isBotTurn()) return;
  place(i);
}

async function botMove() {
  const round = state.round;
  state.busy = true; render();
  try {
    const [res] = await Promise.all([
      fetch("/api/bot-move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board: state.board, bot: state.turn, difficulty: settings.difficulty }),
      }),
      new Promise((r) => setTimeout(r, 450)), // short pause so the move feels natural
    ]);
    if (!res.ok) throw new Error("bad response");
    const { move } = await res.json();
    if (round !== state.round) return; // a new round started meanwhile
    state.busy = false;
    place(move);
  } catch {
    if (round !== state.round) return;
    state.busy = false;
    state.error = "Can’t reach the computer. Check your connection, then start a new round.";
    render();
  }
}

/* ---------- controls ---------- */
document.querySelectorAll(".seg").forEach((seg) => {
  seg.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    seg.querySelectorAll("button").forEach((b) => b.classList.toggle("on", b === btn));
    settings[seg.dataset.key] = btn.dataset.value;
    scores = { X: 0, O: 0, draw: 0 }; saveScores(); // new settings, fresh scoreboard
    startRound();
  });
});
$("#newRound").addEventListener("click", startRound);
$("#resetScores").addEventListener("click", () => { scores = { X: 0, O: 0, draw: 0 }; saveScores(); render(); });

startRound();
