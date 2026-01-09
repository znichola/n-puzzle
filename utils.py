import math

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

def argParser(arg):
    try:
        args = arg.split()
        size = int(args[5])
        # if args[4] == "unsolvable":
        #     raise Exception("This puzzle is unsolvable")
        if math.pow(size, 2) == len(range(6, len(args))):
            grid = [int(n) for n in args[6:]]
        else:
          raise Exception()
        return size, grid
    except Exception as error:
        print(error)
        exit(1)