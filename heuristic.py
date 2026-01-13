import math

import utils as u

idx_to_xy = []


class Heuristic:
    def __init__(self, size, heuristic="Manhattan") -> None:
        tab = {
            "Euclidean": self.euclidean, 
            "Manhattan": self.manhattan,
            "Linear": self.linear,
            "UniformCost": self.uniformCost,
            }
        self.idx_to_xy = [(i // size, i % size) for i in range(size * size)]
        self.h = tab[heuristic]
        self.target = u.getResult(size)
        self.size = size

    def manhattan(self, grid: tuple):
        return sum(list(self.manahattanDistance(a, b) for a, b in self.tilesOutOfPlace(grid)))
    
    def euclidean(self, grid: tuple):
        return sum(list(self.euclideanDistance(a, b) for a, b in self.tilesOutOfPlace(grid)))
    
    def linear(self, grid):
        return self.manhattan(grid) + self.linearConflicts(grid)

    def uniformCost(self, grid):
        return 0

    def tilesOutOfPlace(self, grid: tuple):
        return [(i, grid.index(t)) for i, (t, g) in enumerate(zip(self.target, grid)) if t != g and t != 0]


    def euclideanDistance(self, a_idx: int, b_idx: int):
        ax, ay = self.idx_to_xy[a_idx]
        bx, by = self.idx_to_xy[b_idx]
        return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

    def manahattanDistance(self, a_idx: int, b_idx: int):
        ax, ay = self.idx_to_xy[a_idx]
        bx, by = self.idx_to_xy[b_idx]
        return abs(ax - bx) + abs(ay - by)

    def linearConflicts(self, grid):
        conflict = 0

        for row in range(self.size):
            row_tiles = grid[row*self.size:(row+1)*self.size]
            for i in range(self.size):
                for j in range(i+1, self.size):
                    a, b = row_tiles[i], row_tiles[j]
                    if a == 0 or b == 0:
                        continue

                    goal_a = self.target.index(a)
                    goal_b = self.target.index(b)

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

                    goal_a = self.target.index(a)
                    goal_b = self.target.index(b)

                    if goal_a % self.size == col and goal_b % self.size == col:
                        if goal_a > goal_b:
                            conflict += 2

        return conflict