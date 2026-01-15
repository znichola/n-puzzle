import argparse
import math
import sys

from npuzzlegen import make_puzzle

def setUpArgs():
    parser = argparse.ArgumentParser(description=("N-puzzle solver\n"), add_help=False)
    parser.add_argument(
        "puzzle_path",
        nargs="?",
        default=None,
        help="Path to puzzle file (reads from stdin if omitted)",
        type=str
    )
    parser.add_argument(
        "-h",
        type=str,
        default="Manhattan",
        choices=["Euclidean", "Manhattan", "Linear"]
    )
    parser.add_argument(
        "-a",
        type=str,
        default="ASWiki",
        choices=["ASWiki", "ASDocs", "IDA"]
    )
    parser.add_argument(
        "-f",
        type=str,
        default="Default",
        choices=["Default", "Greedy", "UniformCost"],
    )
    parser.add_argument(
        "-r",
        type=int,
        default=3,
        choices=list(range(3, 7))
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="Print progress"
    )
    parser.add_argument(
        "--help",
        action="help",
        help="show this help message and exit"
    )
    return parser.parse_args()


def parity(grid, size):
    grid_size = len(grid)
    parity = 0
    tmp = [0] * grid_size

    target = getResult(size)
    for i in target:
        tmp[i - 1] = grid[target.index(i)]

    for i, val in enumerate(tmp):
        parity += len(list(filter(lambda v: v < val and v != 0, tmp[i:])))
    return parity


def getPuzzle(args):
    if args.puzzle_path:
        with open(args.puzzle_path) as f:
            puzzle_data = f.read()
            size, grid = puzzleParser(puzzle_data)
    elif args.r:
        size = args.r
        grid = make_puzzle(s=size, solvable=True, iterations=10000)
    else:
        arg = sys.stdin.read()
        size, grid = puzzleParser(arg)

    if parity(grid, size) % 2 != 0:
        print("This puzzle is not solvable.")
        exit(0)

    return size, grid


def getResult(size):
    res = [[0 for _ in range(size)] for _ in range(size)]
    values = list(range(1, int(math.pow(size, 2))))
    pos = [0, 0]
    up = False

    def isOutOfRange(tab, x, y):
        try:
            if tab[x][y] == 0:
                return False
            return True
        except:
            return True

    for val in values:
        res[pos[0]][pos[1]] = val
        if not isOutOfRange(res, pos[0], pos[1] + 1) and up is False:
            pos[1] += 1
        elif not isOutOfRange(res, pos[0] + 1, pos[1]) and up is False:
            pos[0] += 1
        elif not isOutOfRange(res, pos[0], pos[1] - 1) and up is False:
            pos[1] -= 1
        elif not isOutOfRange(res, pos[0] - 1, pos[1]):
            pos[0] -=1
            up = True
        else:
            pos[1] += 1
            up = False
    return [x for xs in res for x in xs]


def gridToString(grid):
    size = int(math.sqrt(len(grid)))
    lines = []
    max_width = len(str(max(grid)))
    for i in range(0, len(grid), size):
        row = grid[i:i + size]
        lines.append(" ".join(f"{num:>{max_width}}" for num in row))
    return "\n".join(lines)


def printGrid(grid):
    print("Grid\n", gridToString(grid), sep='')


def print_tab_to_file(tab, filename: str = "solution.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, row in enumerate(tab):
            f.write(f"{i}\n{gridToString(list(row))}\n\n")


def puzzleParser(input: str) -> tuple[int, list[int]]:
    print(input)
    lines = input.split('\n')
    size = None
    grid = []
    for line in lines:
        l = line.split("#")[0]
        if len(l) == 0:
            continue
        if size == None:
            size = int(l)
        else:
            nums = l.split()
            [grid.append(int(n)) for n in nums]
    if size and math.pow(size, 2) != len(grid):
        raise Exception("Bad input puzzle dimentions")
    g2 = grid.copy()
    g2.sort()
    if len([1 for a, e in zip(g2, list(range(0, len(grid)))) if a != e]) != 0:
        print(f"{grid=} {g2=}")
        raise Exception("Input must be only consecutive numbers")
    if size == None:
        raise Exception("Size cannot be none!")
    return size, grid
