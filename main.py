import math
import sys


# some parsing



class board:

    def __init__(self, size, grid) -> None:
        self.board = grid
        self.size = size
        self.result = self.getResult()


    def __repr__(self) -> str:
        lines = [str(self.size)]
        lines.append("board")
        for i in range(0, len(self.board), self.size):
            lines.append(" ".join(map(str, self.board[i:i+self.size])))
        lines.append("\ntarget")
        for i in range(0, len(self.result), self.size):
            lines.append(" ".join(map(str, self.result[i:i+self.size])))

        return "\n".join(lines) + "\n"


    def getNeighours(self, index) -> list[int]:
        return list(filter(
            lambda v: v >= 0 and v < len(self.board),
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


    def move(self, dir):
        return


def argParser(args):
    print(args)
    
    return 3, [1, 4, 8, 7, 0, 3, 2, 5, 6]


def main():
    #python npuzzle-gen.py n | python main.py
    if not sys.stdin.isatty():
        args = sys.stdin.read()
        size, grid = argParser(args)
    else:
        size = 3
        grid = [4, 1, 8, 7, 0, 3, 2, 5, 6]

    b = board(size, grid)
    print(b)
    print("for index 0, the neighbours are :", b.getNeighours(0))


if __name__ == "__main__":
    main()
