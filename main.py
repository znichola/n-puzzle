import math


# some parsing



class board:
    def __init__(self) -> None:
        self.board = [4, 1, 8, 7, 0, 3, 2, 5, 6]
        self.size = 3
        self.result = self.getResult()
        print(self.result)


    def getNeighours(self, index) -> list[int]:
        return list(filter(
            lambda v: v >= 0 and v < len(self.board),
            [index-self.size, index+1, index+self.size, index-1]
            ))


    def __repr__(self) -> str:
        lines = [str(self.size)]
        lines.append("board")
        for i in range(0, len(self.board), self.size):
            lines.append(" ".join(map(str, self.board[i:i+self.size])))
        lines.append("\ntarget")
        for i in range(0, len(self.result), self.size):
            lines.append(" ".join(map(str, self.result[i:i+self.size])))

        return "\n".join(lines) + "\n"


    def getResult(self):
        res = [[0 for _ in range(self.size)] for _ in range(self.size)]
        nb_values = int(math.pow(self.size, 2))
        values = list(range(1, nb_values))
        pos = [0, 0]
        up = False
        for val in values:
            # print(pos[0], pos[1], up)
            res[pos[0]][pos[1]] = val
            if not self.isOutOfRange(res, pos[0], pos[1] + 1) and up is False:
                pos[1] += 1
            elif not self.isOutOfRange(res, pos[0] + 1, pos[1]) and up is False:
                pos[0] += 1
            elif not self.isOutOfRange(res, pos[0], pos[1] - 1) and up is False:
                pos[1] -= 1
            elif not self.isOutOfRange(res, pos[0] - 1, pos[1]):
                pos[0] -=1
                up = True
            else:
                pos[1] += 1
                up = False
            # print(val, res)
        return [x for xs in res for x in xs]

    def isOutOfRange(self, tab, x, y):
        try:
            if tab[x][y] == 0:
                return False
            return True
        except:
            return True


def main():
    print("Hello from n-puzzle!")


if __name__ == "__main__":
    b = board()
    print(b, "for index 0, the neighbours are :", b.getNeighours(0))
    main()
