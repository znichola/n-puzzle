import math
import sys
from typing import Literal, Optional

import utils as u

C = 1

class state:
    def __init__(self, id, grid, h):
        self.id = id
        self.predecessor: Optional[int] = None
        self.cost = 0
        self.h = h
        self.grid = grid

    def __repr__(self) -> str:
        return u.gridToString(self.grid)
    def g(self):
        return self.cost


class board:
    def __init__(self, size, grid, h: Literal["Euclidean", "Manhattan", "Parity"] = "Euclidean") -> None:
        self.target = u.getResult(size)
        self.size = size
        self.idx_to_xy = [(i // self.size, i % self.size) for i in range(self.size * self.size)]
        self.current_id = 0
        self.isSolvable = self.parity(grid) % 2 == 0
        self.states = [] # each state has an id, which is the index in this list
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

        def test():
            return []

        if self.h == "Euclidean":
            return sum(list(euclideanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
        elif self.h == "Manhattan":
            return sum(list(manahattanDistance(a, b) for a, b in tilesOutOfPlace(grid)))
        elif self.h == "Parity":
            return sum(list(euclideanDistance(a, b) for a, b in tilesOutOfPlace(grid))) *  1 / self.parity(grid)
        elif self.h == "test":
            return test()
        return 42

    def select_by_heuristic(self, possible_states: set[int]):
        s_id_with_cost = [(s_id, self.states[s_id].h) for s_id in possible_states]
        return min(s_id_with_cost, key=lambda t: t[1])[0]


    def SolutionSequence(self):
        tab = []
        idx = self.last_state_id
        while True:
            tab.append(self.states[idx].grid)
            if idx == 0:
                break
            idx = self.states[idx].predecessor
        tab.reverse()
        u.print_tab_to_file(tab)
        return len(tab)


    def algo(self):
        opened = set([self.current_id-1])
        self.totoalStatesOpened = len(opened)
        closed = set()
        succes = False
        while len(opened) != 0 and succes is False:
            e_id = self.select_by_heuristic(opened)
            e_state = self.states[e_id]
            if e_state.grid == self.target:
                self.last_state_id = e_id
                succes = True
            else:
                opened.remove(e_id)
                closed.add(e_id)
                ee = self.expand(e_id)
                for s_id in ee:
                    s_state = self.states[s_id]
                    if (not s_id in opened) and (not s_id in closed):
                        opened.add(s_id);  self.totoalStatesOpened += 1
                        s_state.predecessor = e_id
                        s_state.cost = e_state.cost + C
                    else:
                        if s_state.g() + self.heuristic(s_state.grid) > e_state.g() + C + self.heuristic(s_state.grid):
                            s_state.predecessor = e_id
                            s_state.cost = e_state.cost + C
                            if s_id in closed:
                                closed.remove(s_id)
                                opened.add(s_id); self.totoalStatesOpened += 1


    def createState(self, grid):
        self.states.append(state(self.current_id, grid, self.heuristic(grid)))
        self.current_id += 1


    def findOrCreateState(self, grid) -> state:
        res = list(filter(lambda s: s.grid == grid, self.states))
        if len(res) == 0:
            self.createState(grid)
            return self.states[self.current_id - 1]
        if len(res) != 1: raise Exception("Duplicate states")
        return res[0]


    def expand(self, state_id) -> list[int]:
        '''returns a list of ids'''
        def getNeighbouringStates(state_id):
            def getNeighbours(index):
                return list(filter(
                    lambda v: v >= 0 and v < pow(self.size, 2) and 
                    (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
                    [index-self.size, index+1, index+self.size, index-1]
                    ))
            states = []
            current_grid = self.states[state_id].grid
            index = current_grid.index(0)
            neighbours = getNeighbours(index)
            for n in neighbours:
                newState = current_grid.copy()
                newState[n], newState[index] = newState[index], newState[n]
                states.append(newState)
            return states
        grids = getNeighbouringStates(state_id)
        return [self.findOrCreateState(g).id for g in grids]



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
        b.algo()
        print(f"h = {b.h}")
        print("Total number of states ever selected in the opened set : ", b.totoalStatesOpened)
        print("Maximum number of states ever represented in memory at the same time during the search : ", len(b.states))
        print("Number of moves required to transition from the initial state to the final state : ", b.SolutionSequence())
        print("The ordered sequence of states that make up the solution : solution.txt")
    else:
        print("This Puzzle is unsolvable.")
        exit(1)



if __name__ == "__main__":
    main()
