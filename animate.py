import argparse
import math
import os
import time

import utils as u


def parse_solution(path):
    states = []

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip() != ""]

    i = 0
    while i < len(lines):
        _ = int(lines[i]) # ignore step count
        i += 1

        board = []
        while i < len(lines) and not lines[i].isdigit():
            board.extend(list(map(int, lines[i].split())))
            i += 1
        states.append(board)

    return states


def gridToString(grid, target):
    size = int(math.sqrt(len(grid)))
    max_width = len(str(max(grid)))
    lines = []

    for i in range(0, len(grid), size):
        row = grid[i:i + size]
        target_row = target[i:i + size]
        row_str = []
        for g, t in zip(row, target_row):
            s = f"{g:>{max_width}}"
            if g == t and g != 0:  # green if matches target
                s = f"\033[92m{s}\033[0m"
            row_str.append(s)
        lines.append(" ".join(row_str))
    return "\n".join(lines)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def animate_solution(solution_path, delay):
    states = parse_solution(solution_path)
    target = u.getResult(int(math.sqrt(len(states[0]))))
    for step, grid in enumerate(states):
        clear_screen()
        print(f"Step {step}/{len(states) - 1}\n")
        print(gridToString(grid, target))
        time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Animate an N-Puzzle solution")
    parser.add_argument(
        "solution_path",
        nargs="?",
        default="solution.txt"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1
    )

    args = parser.parse_args()
    animate_solution(args.solution_path, args.delay)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Something went wrong... :(\n{error}")
        exit()