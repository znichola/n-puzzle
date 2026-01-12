import math
import sys
import heapq
from typing import Literal, Optional

import utils as u

C = 1

class state:
    def __init__(self, grid, h):
        self.predecessor: Optional[int] = None
        self.cost = 0
        self.h = h
        self.grid = grid

    def __repr__(self) -> str:
        return u.gridToString(self.grid)

    def g(self):
        return self.cost

    def id(self):
        return str(self.grid)


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
            return abs(ax - ay) + abs(bx - by)

        def tilesOutOfPlace(grid: list[int]):
            return [(i, grid.index(t)) for i, (t, g) in enumerate(zip(self.target, grid)) if t != g ]

        if self.h == "Euclidean":
            test = sum(list(euclideanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
            return test
        elif self.h == "Manhattan":
            test = sum(list(manahattanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
            return test
        return 42

    def select_by_heuristic(self, possible_states: set[str]):
        # s_hash_with_cost = [(s_hash, self.states[s_hash].h) for s_hash in possible_states]
        # return min(s_hash_with_cost, key=lambda t: t[1])[0]
        return min(
            possible_states,
            key=lambda s_hash: self.states[s_hash].h
        )


    # def SolutionSequence(self):
    #     tab = []
    #     idx = self.last_state_id
    #     while True:
    #         tab.append(self.states[idx].grid)
    #         if idx == 0:
    #             break
    #         idx = self.states[idx].predecessor
    #     tab.reverse()
    #     u.print_tab_to_file(tab)
    #     return len(tab)


    def algo(self, grid):
        opened =[(0, str(grid))]
        self.totoalStatesOpened = 1
        closed = set()

        succes = False
        while len(opened) != 0 and succes is False:
            _, e_hash = heapq.heappop(opened) # Select state by minimum heuristic
            e_state = self.states[e_hash]
            if e_state.grid == self.target:
                self.last_state_id = e_state.id ###
                succes = True
            else:
                # opened.remove((h, e_hash))
                closed.add(e_hash)
                ee_hash = self.expand(e_hash)
                for s_hash in ee_hash:
                    s_state = self.states[s_hash]
                    if (not s_hash in opened) and (not s_hash in closed):
                        heapq.heappush(opened, (s_state.h, s_hash));  self.totoalStatesOpened += 1
                        s_state.predecessor = e_hash
                        s_state.cost = e_state.cost + C
                    else:
                        if s_state.g() + s_state.h > e_state.g() + C + s_state.h:
                            s_state.predecessor = e_hash
                            s_state.cost = e_state.cost + C
                            if s_hash in closed:
                                closed.remove(s_hash)
                                heapq.heappush(opened, (s_state.h, s_hash)); self.totoalStatesOpened += 1


    def createState(self, grid):
        self.states[str(grid)] = state(grid, self.heuristic(grid))
        self.current_id += 1


    def findOrCreateState(self, grid) -> state:
        g_hash = str(grid)
        s = self.states.get(g_hash)
        if s == None:
            self.createState(grid)
            return self.states[g_hash]
        return s


    def expand(self, state_hash: str) -> list[str]:
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
                newState = current_grid.copy()
                newState[n], newState[index] = newState[index], newState[n]
                states.append(newState)
            return states
        grids = getNeighbouringStates(state_hash)
        return [str(self.findOrCreateState(g).grid) for g in grids]



## TODO how is the program supposed to be used, with a pipe or passing a file with the grid to use
## TODO     self.isSolved()
##          do we make a seperate state/grid/board class, with the grid, it's predeccssor and the cumulated cost

def main():
    args = u.setUpArgs()

    #python npuzzle-gen.py n | python main.py
    if args.puzzle_path is None or args.puzzle_path == "-":
        arg = sys.stdin.read()
        size, grid = u.puzzleParser(arg)
    else:
        with open(args.puzzle_path) as f:
            puzzle_data = f.read()
            size, grid = u.puzzleParser(puzzle_data)


    b = board(size, grid, args.heuristic)
    
    if b.isSolvable:
        b.algo(grid)
        # print(f"h = {b.h}")
        print("Total number of states ever selected in the opened set : ", b.totoalStatesOpened)
        print("Maximum number of states ever represented in memory at the same time during the search : ", len(b.states))
        # print("Number of moves required to transition from the initial state to the final state : ", b.SolutionSequence())
        # print("The ordered sequence of states that make up the solution : solution.txt")
    else:
        print("This Puzzle is unsolvable.")
        exit(1)



if __name__ == "__main__":
    main()
