import math
import utils as u


class Heuristic:
    def __init__(self, size, type="Manhattan") -> None:
        self.size = size
        self.target = u.getResult(size)

        # index -> (row, col)
        self.idx_to_xy = [(i // size, i % size) for i in range(size * size)]

        # tile -> goal index
        self.goal_index = {tile: i for i, tile in enumerate(self.target)}

       # tile -> (goal_row, goal_col)
        self.goal_pos = {
            tile: self.idx_to_xy[i]
            for tile, i in self.goal_index.items()
        }

        self._h = {
            "Manhattan": self._manhattan,
            "Euclidean": self._euclidean,
            "Linear": self._linear,
        }[type]

        self.cache = {}

    def h(self, grid: tuple) -> float:
        if grid not in self.cache:
            self.cache[grid] = self._h(grid)
        return self.cache[grid]

    def _manhattan(self, grid: tuple):
        total = 0
        for i, g in enumerate(grid):
            if g == 0:
                continue
            x, y = self.idx_to_xy[i]
            gx, gy = self.goal_pos[g]
            total += abs(x - gx) + abs(y - gy)
        return total

    def _euclidean(self, grid: tuple):
        total = 0
        for i, g in enumerate(grid):
            if g == 0:
                continue
            x, y = self.idx_to_xy[i]
            gx, gy = self.goal_pos[g]
            total += math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
        return total
    
    def _linear(self, grid):
        return self._manhattan(grid) + self._linearConflicts(grid)


    def euclideanDistance(self, a_idx: int, b_idx: int):
        ax, ay = self.idx_to_xy[a_idx]
        bx, by = self.idx_to_xy[b_idx]
        return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

    def manahattanDistance(self, a_idx: int, b_idx: int):
        ax, ay = self.idx_to_xy[a_idx]
        bx, by = self.idx_to_xy[b_idx]
        return abs(ax - bx) + abs(ay - by)

    def _linearConflicts(self, grid):
        conflict = 0

        for row in range(self.size):
            row_tiles = grid[row*self.size:(row+1)*self.size]
            for i in range(self.size):
                for j in range(i+1, self.size):
                    a, b = row_tiles[i], row_tiles[j]
                    if a == 0 or b == 0:
                        continue

                    goal_a = self.goal_index[a]
                    goal_b = self.goal_index[b]

                    if goal_a // self.size == row and goal_b // self.size == row:
                        if goal_a > goal_b:
                            conflict += 2

        for col in range(self.size):
            col_tiles = grid[col::self.size]
            for i in range(self.size):
                for j in range(i+1, self.size):
                    a, b = col_tiles[i], col_tiles[j]
                    if a == 0 or b == 0:
                        continue

                    goal_a = self.goal_index[a]
                    goal_b = self.goal_index[b]

                    if goal_a % self.size == col and goal_b % self.size == col:
                        if goal_a > goal_b:
                            conflict += 2

        return conflict