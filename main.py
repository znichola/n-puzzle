import math
import sys

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


    def getNeighbours(self, index):
        return list(filter(
            lambda v: v >= 0 and v < len(self.board) and 
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


    def move1(self, void, target):
        #INDEX
        self.board[void], self.board[target] = self.board[target], self.board[void]

    def move2(self, void_idx, target_idx):
        #VALUES
        void = self.board.index(void_idx)
        target = self.board.index(target_idx)
        self.board[void], self.board[target] = self.board[target], self.board[void]


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


if __name__ == "__main__":
    main()
