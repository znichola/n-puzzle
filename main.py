import math
import sys
import heapq
from typing import Literal, Optional

import utils as u

C = 1

class state:
    def __init__(self, grid: tuple, h):
        self.predecessor: Optional[int] = None
        self.g = 0
        self.f = 0
        self.h = h
        self.grid = grid

    def __repr__(self) -> str:
        return u.gridToString(self.grid)
    
    def __lt__(self, other):
        return self.f > other.f
    
    def updateFScore(self):
        self.f = self.g + self.h


class board:
    def __init__(self, size, grid, h: Literal["Euclidean", "Manhattan", "Parity", "test"] = "Euclidean") -> None:
        self.target = u.getResult(size)
        self.size = size
        self.idx_to_xy = [(i // self.size, i % self.size) for i in range(self.size * self.size)]
        self.current_id = 0
        self.isSolvable = self.parity(grid) % 2 == 0
        self.states = {}
        self.h = h
        self.createState(grid)
        self.totoalStatesOpened = 0
        self.solutionSequence = 0


    def __repr__(self) -> str:
        return f'Num of state: {self.current_id - 1}\nTarget {self.target}'


    def parity(self, grid):
        grid_size = int(math.pow(self.size, 2))
        parity = 0
        tmp = [0] * grid_size

        for i in self.target:
            tmp[i - 1] = grid[self.target.index(i)]

        for i, val in enumerate(tmp):
            parity += len(list(filter(lambda v: v < val and v != 0, tmp[i:])))
        return parity


    def heuristic(self, grid: list[int]):
        def euclideanDistance(a_idx: int, b_idx: int):
            ax, ay = self.idx_to_xy[a_idx]
            bx, by = self.idx_to_xy[b_idx]
            return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

        def manahattanDistance(a_idx: int, b_idx: int):
            ax, ay = self.idx_to_xy[a_idx]
            bx, by = self.idx_to_xy[b_idx]
            return abs(ax - bx) + abs(ay - by)

        def tilesOutOfPlace(grid: list[int]):
            return [(i, grid.index(t)) for i, (t, g) in enumerate(zip(self.target, grid)) if t != g and t != 0]

        def getNeighbours(index):
            return list(filter(
                lambda v: v >= 0 and v < pow(self.size, 2) and 
                (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
                [index-self.size, index+1, index+self.size, index-1]
                ))

        def smarts(grid: list[int]):
            total = 0
            for i, value in enumerate(grid):
                for n_index in getNeighbours(i):
                    if n_index > i and (grid[n_index] == value + 1 or grid[n_index] == value - 1):
                        total += 1
            max_connections = 2*(self.size-1)*self.size # see A046092 from oeis
            dist = sum(list(manahattanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
            return dist * (total / max_connections)
        
        def manahattan_snake_cost(grid: list[int]):
            tmp = tilesOutOfPlace(grid)
            max_tile = self.size ** 2
            foo = list(manahattanDistance(a, b) * ((((max_tile - grid[a] + 1) /  max_tile)) if grid[a] < (max_tile - 8) else 1) for a, b in tmp)
            return sum(foo)

        def linear(grid):
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



        if self.h == "Euclidean":
            return sum(list(euclideanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
        elif self.h == "Manhattan":
            return sum(list(manahattanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
        elif self.h == "Smart":
            return smarts(grid)
        elif self.h == "Linear":
            return sum(list(manahattanDistance(a, b) for a, b in tilesOutOfPlace(grid))) + linear(grid)
        elif self.h == "UniformCost":
            return 0
        elif self.h == "ManhattanSnakeCost":
            return manahattan_snake_cost(grid)
        return 42

    def select_by_heuristic(self, possible_states: set[str]):
        # s_hash_with_cost = [(s_hash, self.states[s_hash].h) for s_hash in possible_states]
        # return min(s_hash_with_cost, key=lambda t: t[1])[0]
        return min(
            possible_states,
            key=lambda s_hash: self.states[s_hash].h
        )


    def SolutionSequence(self, grid):
        tab = []
        idx = self.last_state_id
        while True:
            tab.append(self.states[idx].grid)
            if idx == str(grid):
                break
            idx = str(self.states[idx].predecessor)
        tab.reverse()
        u.print_tab_to_file(tab)
        return len(tab)


    def algo(self, grid: tuple):
        opened = [grid] ; heapq.heapify(opened)
        opened_set = set([grid])
        self.totoalStatesOpened = 1
        closed = set()

        succes = False
        while len(opened) != 0 and succes is False:
            e_hash = heapq.heappop(opened); opened_set.remove(e_hash) # Select state by minimum heuristic
            e_state = self.states[e_hash]
            if e_state.grid == self.target:
                self.last_state_id = e_state.grid
                succes = True
            else:
                closed.add(e_hash)
                ee_hash = self.expand(e_state.grid)
                for s_hash in ee_hash:
                    s_state = self.states[s_hash]
                    if (not s_hash in opened_set) and (not s_hash in closed):
                        opened_set.add(s_hash); heapq.heappush(opened, (s_state.h, s_hash)); self.totoalStatesOpened += 1
                        s_state.predecessor = e_hash
                        s_state.g = e_state.g + C
                    else:
                        if s_state.g + s_state.h > e_state.g + C + s_state.h:
                            s_state.predecessor = e_hash
                            s_state.g = e_state.g + C
                            if s_hash in closed:
                                closed.remove(s_hash)
                                opened_set.add(s_hash); heapq.heappush(opened, (s_state.h, s_hash)); self.totoalStatesOpened += 1

    # def algo2(self, grid):
    #     opened =[(0, str(grid))]
    #     opened_set = set([str(grid)])
    #     self.totoalStatesOpened = 1
    #     closed = set()
    #     succes = False
    #     while len(opened) != 0 and succes is False:
    #         h, e_hash = heapq.heappop(opened) # Select state by minimum heuristic
    #         # print(h, e_hash)
    #         # print(h)
    #         if self.states[e_hash].grid == self.target:
    #             self.last_state_id = str(self.states[e_hash].grid)
    #             succes = True
    #         if e_hash in closed:
    #             continue
    #         ee_hash = self.expand(e_hash)
    #         for s_hash in ee_hash:
    #             heapq.heappush(opened, (self.states[s_hash].cost + self.states[s_hash].h, s_hash)); self.totoalStatesOpened += 1
    #         closed.add(e_hash)


    def createState(self, grid: tuple):
        self.states[grid] = state(grid, self.heuristic(grid))
        self.current_id += 1


    def findOrCreateState(self, grid: tuple) -> state:
        g_hash = grid
        s = self.states.get(g_hash)
        if s == None:
            self.createState(grid)
            return self.states[g_hash]
        return s


    def expand(self, state: tuple) -> list[tuple]:
        '''returns a list of ids'''
        def getNeighbouringStates(state_hash):
            def getNeighbours(index):
                return list(filter(
                    lambda v: v >= 0 and v < pow(self.size, 2) and 
                    (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
                    [index-self.size, index+1, index+self.size, index-1]
                    ))
            states = []
            current_grid = self.states[state_hash].grid
            index = current_grid.index(0)
            neighbours = getNeighbours(index)
            for n in neighbours:
                newState = list(current_grid)
                newState[n], newState[index] = newState[index], newState[n]
                states.append(tuple(newState))
            return states
        grids = getNeighbouringStates(state)
        return [self.findOrCreateState(g).grid for g in grids]



## TODO how is the program supposed to be used, with a pipe or passing a file with the grid to use
## TODO     self.isSolved()
##          do we make a seperate state/grid/board class, with the grid, it's predeccssor and the cumulated cost

def main():
    args = u.setUpArgs()
    if args.puzzle_path is None or args.puzzle_path == "-":
        arg = sys.stdin.read()
        size, grid = u.puzzleParser(arg)
    else:
        with open(args.puzzle_path) as f:
            puzzle_data = f.read()
            size, grid = u.puzzleParser(puzzle_data)

    b = board(size, tuple(grid), args.heuristic)
    
    if b.isSolvable:
        if args.alt_algo:
            b.algo2(grid)
        else:
            b.algo(tuple(grid))
        print(f"h = {b.h}")
        print("Total number of states ever selected in the opened set : ", b.totoalStatesOpened)
        print("Maximum number of states ever represented in memory at the same time during the search : ", len(b.states))
        # print("Number of moves required to transition from the initial state to the final state : ", b.SolutionSequence(grid))
        # print("The ordered sequence of states that make up the solution : solution.txt")
    else:
        print("This Puzzle is unsolvable.")
        exit(1)

    # except Exception as error:
    #     print(f"Error: {error}")
    #     exit(1)



if __name__ == "__main__":
    main()
