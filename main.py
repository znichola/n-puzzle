import math
import sys
from typing import Optional

import utils as u

class state:
    def __init__(self, id, grid):
        self.id = id
        self.predecessor: Optional[int] = None
        self.cost = 0
        self.grid = grid

    def g(self):
        return self.cost
    
    def set_g(self, g):
        self.cost = g


class board:
    def __init__(self, size, grid) -> None:
        self.target = u.getResult(size)
        self.size = size

        self.current_id = 0
        self.states = [] # each state has an id, which is the index in this list
        self.createState(grid)
        self.algo(0)


    def __repr__(self) -> str:
        return f'Num of state: {self.current_id - 1}\nTarget {self.target}'


    def heuristic(self, selection):
        if len(selection) == 0: raise Exception("Passed empty list to heuristic!")
        return selection[0]


    def algo(self, start_state):
        opened = set(self.expand(start_state))
        closed = set()
        succes = False
        print(opened)
        [u.printGrid(s.grid) for s in self.states]
        exit(1)
        while len(opened) != 0 and self.succes is False:
            e_id = self.heuristic(opened)
            if self.states[e_id].grid == self.target:
                succes = True
            else:
                opened.remove(e_id)
                closed.add(e_id)
                for s_id in self.expand(e_id):
                    if (not s_id in opened) and (not s_id in closed):
                        s_state = self.findOrCreateState(s_id)
                        s_state.predecessor = e_id
                        s_state.set_g(1)
                    else:
                        e_state = self.findOrCreateState(e)
                        if s_state.g() + self.heuristic(s) > 1:
                            s_state = self.findOrCreateState(s_id)
                            s_state.predecessor = e_id
                            s_state.cost = 0
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


    def findOrCreateState(self, grid) -> state | None:
        res = list(filter(lambda s: s.grid == grid, self.states))
        if len(res) == 0:
            self.createState(grid)
            return self.states[self.current_id - 1]
        if len(res) != 1: raise Exception("Duplicate states")
        return res[0]


    def expand(self, state_id):
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
    print(u.printGrid(grid))

    b.printFullState()


if __name__ == "__main__":
    main()
