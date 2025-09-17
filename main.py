#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stockfish import Stockfish
import os
import shutil

# === Configure path to Stockfish executable ===
# You can also set STOCKFISH_PATH as an environment variable
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH") or "stockfish/src/stockfish"

if not shutil.which(STOCKFISH_PATH) and not os.path.isfile(STOCKFISH_PATH):
    raise RuntimeError(
        f"Cannot find Stockfish binary at: {STOCKFISH_PATH}\n"
        "• Download from https://stockfishchess.org/download/ and update the path.\n"
        "• Or export STOCKFISH_PATH with the path to the executable."
    )

# Initialize Stockfish engine
engine = Stockfish(
    path=STOCKFISH_PATH,
    depth=16,
    parameters={
        "Threads": 2,
        "Hash": 256,  # MB of hash
        "Minimum Thinking Time": 30,  # ms
        # "Skill Level": 10,  # 0-20 (if your build supports it)
        # "UCI_LimitStrength": True, "UCI_Elo": 1600,
    },
)

moves_history: list[str] = []


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_board() -> None:
    """Display the board in ASCII/Unicode."""
    try:
        print(engine.get_board_visual())
    except Exception:
        print("\nCurrent FEN:\n", engine.get_fen_position())


def apply_move_uci(uci_move: str) -> bool:
    """Validate and apply a UCI move (e.g., 'e2e4', 'g1f3', 'e7e8q')."""
    if not engine.is_move_correct(uci_move):
        return False
    engine.make_moves_from_current_position([uci_move])
    moves_history.append(uci_move)
    return True


def undo_last_halfmove() -> bool:
    """Undo the last half-move from either side."""
    if not moves_history:
        return False
    moves_history.pop()
    engine.set_position(moves_history)
    return True


def engine_reply(ms: int | None = None) -> str | None:
    """Ask the engine for the best move and apply it."""
    best = engine.get_best_move_time(ms) if ms else engine.get_best_move()
    if best is None:
        return None
    engine.make_moves_from_current_position([best])
    moves_history.append(best)
    return best


def help_text() -> str:
    return (
        "\nCommands:\n"
        "  e2e4           -> make a UCI move (examples: e2e4, g1f3, e7e8q)\n"
        "  hint           -> ask engine for best move (does not play)\n"
        "  go             -> engine plays its move\n"
        "  undo           -> undo last half-move\n"
        "  new            -> start new game\n"
        "  fen            -> show current FEN\n"
        "  eval           -> show engine evaluation (if supported)\n"
        "  help           -> show this help\n"
        "  exit           -> quit game\n"
    )


def main():
    clear_screen()
    print("♟ Chess CLI with Stockfish (UCI). White moves first.")
    print(help_text())
    show_board()

    while True:
        try:
            cmd = input("\nYour move/command: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting…")
            break

        if cmd in ("exit", "quit", "q"):
            print("Thanks for playing!")
            break

        if cmd == "help":
            clear_screen()
            print(help_text())
            show_board()
            continue

        if cmd == "new":
            moves_history.clear()
            engine.set_position([])
            clear_screen()
            show_board()
            continue

        if cmd == "undo":
            if undo_last_halfmove():
                clear_screen()
                show_board()
            else:
                print("Nothing to undo.")
            continue

        if cmd == "fen":
            print(engine.get_fen_position())
            continue

        if cmd == "hint":
            suggestion = engine.get_best_move()
            print("Engine suggests:", suggestion or "(no move)")
            continue

        if cmd == "go":
            mv = engine_reply()
            clear_screen()
            if mv:
                print("Engine plays:", mv)
                show_board()
            else:
                print("Engine has no move (game over?).")
            continue

        if cmd == "eval":
            try:
                ev = engine.get_evaluation()  # {'type': 'cp'|'mate', 'value': int}
                print("Evaluation:", ev)
            except Exception:
                print("Your build does not support evaluation output.")
            continue

        # If not a command, try to treat input as a UCI move
        if apply_move_uci(cmd):
            clear_screen()
            show_board()
            mv = engine_reply()
            if mv:
                print("Engine replies:", mv)
                show_board()
            else:
                print("Engine has no reply (checkmate or draw?).")
        else:
            print("Invalid input. Use UCI (e.g., e2e4) or type 'help' for commands.")


if __name__ == "__main__":
    main()

