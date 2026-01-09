import math
import sys
from typing import Optional

import utils as u

C = 1

class state:
    def __init__(self, id, grid):
        self.id = id
        self.predecessor: Optional[int] = None
        self.cost = 0
        self.grid = grid
    def __repr__(self) -> str:
        return u.gridToString(self.grid)
    def g(self):
        return self.cost


class board:
    def __init__(self, size, grid) -> None:
        self.target = u.getResult(size)
        self.size = size
        self.current_id = 0
        self.isSolvable = not self.isNotSolvable(grid)
        self.states = [] # each state has an id, which is the index in this list
        self.createState(grid)

    def __repr__(self) -> str:
        return f'Num of state: {self.current_id - 1}\nTarget {self.target}'


    def isNotSolvable(self, grid):
        parity = 0
        gridWidth = self.size
        row = 0
        blankRow = 0

        for i in range(len(grid)):
            if i % gridWidth == 0:
                row += 1
            if grid[i] == 0:
                blankRow = row
                continue
            for j in range(i+1, len(grid)):
                if grid[i] > grid[j] and grid[j] != 0:
                    parity += 1

        if gridWidth % 2 == 0 and blankRow % 2 != 0:
                return parity % 2 != 0
        return parity % 2 == 0


    def heuristic(self, s_id: int):
        def euclideanDistance(a_idx: int, b_idx: int):
            ax, ay = a_idx // self.size, a_idx % self.size
            bx, by = b_idx // self.size, b_idx % self.size
            # return abs((ax - bx) + (ay - by))
            return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

        def wrongSquares(grid: list[int]):
            return [(i, grid.index(t)) for i, (t, g) in enumerate(zip(self.target, grid)) if t != g ]
        
        return sum(list(euclideanDistance(a, b) for a, b in wrongSquares(self.states[s_id].grid)))


    def select_by_heuristic(self, possible_states: set[int]):
        s_id_with_cost = [(s_id, self.heuristic(s_id)) for s_id in possible_states]
        return min(s_id_with_cost, key=lambda t: t[1])[0]


    def algo(self, start_state):
        opened = set(self.expand(start_state))
        closed = set()
        succes = False
        # print(opened)
        # [u.printGrid(s.grid) for s in self.states]
        while len(opened) != 0 and succes is False:
            e_id = self.select_by_heuristic(opened)
            e_state = self.states[e_id]
            if e_state.grid == self.target:
                succes = True
            else:
                opened.remove(e_id)
                closed.add(e_id)
                ee = self.expand(e_id)
                for s_id in ee:
                    s_state = self.states[s_id]
                    if (not s_id in opened) and (not s_id in closed):
                        opened.add(s_id)
                        s_state.predecessor = e_id
                        s_state.cost = e_state.cost + C
                    else:
                        if s_state.g() + self.heuristic(s_id) > e_state.g() + C + self.heuristic(s_id):
                            s_state.predecessor = e_id
                            s_state.cost = e_state.cost + C
                            if s_id in closed:
                                closed.remove(s_id)
                                opened.add(s_id)

        if succes is True:
            print("Succeed")
        else:
            print("Unsolvable")


    def createState(self, grid):
        self.states.append(state(self.current_id, grid))
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
    #python npuzzle-gen.py n | python main.py
    if not sys.stdin.isatty():
        arg = sys.stdin.read()
        size, grid = u.argParser(arg)
    else:
        size = 3
        grid = [4, 1, 8, 7, 0, 3, 2, 5, 6]

    b = board(size, grid)
    
    if b.isSolvable:
        b.algo(0)
    else:
        print("Is Unsolvable")



if __name__ == "__main__":
    main()
