import math
import sys
from typing import Optional

import utils as u

class state:
    def __init__(self, id, grid):
        self.id = id
        self.precedent: Optional[int] = None
        self.cost = 0
        self.grid = grid


class board:
    def __init__(self, size, grid) -> None:
        self.target = u.getResult(size)

        self.current_id = 0
        self.states = [] # each state has an id, which is the index in this list
        self.createState(grid)


    def __repr__(self) -> str:
        return f'Num of state: {self.current_id - 1}\nTarget {self.target}'


    def algo(self, start_state):
        opened = set(self.expand(start_state))
        closed = set()
        succes = False
        while len(self.t) != 0 and self.succes is False:
            ...
        if self.succes is True:
            print("Succeed")
        else:
            print("Unsolvable")


    def createState(self, grid):
        self.states.append(state(self.current_id, grid))
        self.current_id += 1


    def getNeighbouringStates(self, state_id):
        def getNeighbours(index):
            return list(filter(
                lambda v: v >= 0 and v < len(self.grid) and 
                (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
                [index-self.size, index+1, index+self.size, index-1]
                ))
        states = []
        current_grid = self.states[state_id].grid
        index = current_grid.index(0)
        neighbours = getNeighbours(index)
        for n in neighbours:
            newState = self.grid.copy()
            newState[n], newState[index] = newState[index], newState[n]
            states.append(newState)
        return states

    def expand(self, state_e):
        
        pass







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
