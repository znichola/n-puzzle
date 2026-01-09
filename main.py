import math
import sys

class board:
    def __init__(self, size, grid) -> None:
        self.grid = grid
        self.size = size
        self.target = self.getResult()


    def __repr__(self) -> str:
        return f'Size: {self.size}\nGrid   {self.grid}\nTarget {self.target}'




    def printFullState(self):
        def showGrid(g):
            lines = []
            max_width = len(str(max(g)))
            for i in range(0, len(g), self.size):
                row = g[i:i + self.size]
                lines.append(" ".join(f"{num:>{max_width}}" for num in row))
            return lines
        grid = showGrid(self.grid)
        target = showGrid(self.target)
        res = "\n".join( f'{g}  |  {t}' for g, t in zip(grid, target))
        print("Size:", self.size)
        print("Grid", ' ' * len(grid[0]), "Target", sep='')
        print(res)


    def getNeighbours(self, index):
        return list(filter(
            lambda v: v >= 0 and v < len(self.grid) and 
            (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
            [index-self.size, index+1, index+self.size, index-1]
            ))


    def getResult(self):
        res = [[0 for _ in range(self.size)] for _ in range(self.size)]
        values = list(range(1, int(math.pow(self.size, 2))))
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


    def moveByIndex(self, void, target):
        self.grid[void], self.grid[target] = self.grid[target], self.grid[void]

    def moveByValue(self, void_idx, target_idx):
        void = self.grid.index(void_idx)
        target = self.grid.index(target_idx)
        self.grid[void], self.grid[target] = self.grid[target], self.grid[void]


def argParser(arg):
    try:
        args = arg.split()
        size = int(args[5])
        if args[4] == "unsolvable":
            raise Exception("This puzzle is unsolvable")
        if math.pow(size, 2) == len(range(6, len(args))):
            grid = [int(n) for n in args[6:]]
        else:
          raise Exception()
        return size, grid
    except Exception as error:
        print(error)
        exit(1)


## TODO how is the program supposed to be used, with a pipe or passing a file with the grid to use

def main():
    #python npuzzle-gen.py n | python main.py
    if not sys.stdin.isatty():
        arg = sys.stdin.read()
        size, grid = argParser(arg)
    else:
        size = 3
        grid = [4, 1, 8, 7, 0, 3, 2, 5, 6]

    b = board(size, grid)
    print(b)
    print("for index 0, the neighbours are :", b.getNeighbours(0))
    print("for index 4, the neighbours are :", b.getNeighbours(4))
    print("for index 5, the neighbours are :", b.getNeighbours(5))

    b.printFullState()


if __name__ == "__main__":
    main()
