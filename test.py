import sys
import heapq

import utils as u


class State:
    def __init__(self, grid: tuple):
        self.g = 0
        self.h = 0
        self.f = 0
        self.grid = grid
        self.pred = None

    def __lt__(self, other):
        return self.f > other.f


class Board:

    def __init__(self, size, board: list):
        self.target = tuple(u.getResult(board))
        self.opened = [] ; heapq.heapify(self.states)
        self.size = size
        pass

    
    def algo(self, grid: tuple):
        heapq.heappush(self.opened, State(grid))
        while len(self.opened):
            current_state = heapq.heappop(self.opened)
            if current_state == self.target:
                return True, []
            


        return False, None
    
    def sequence(heritage, final_state):
        return


def main():

    args = u.setUpArgs()
    size, grid = u.getPuzzle(args)

    Puzzle = Board()

    isSolvable, sequence = Puzzle.algo()
    if isSolvable:
        print("This Puzzle is solvable.")
        # print("Total number of states ever selected in the opened set : ", b.totoalStatesOpened)
        # print("Maximum number of states ever represented in memory at the same time during the search : ", len(b.states))
        # print("Number of moves required to transition from the initial state to the final state : ", b.SolutionSequence(grid))
        # print("The ordered sequence of states that make up the solution : solution.txt")
    else:
        print("This Puzzle is unsolvable.")
        exit(1)
    




if __name__ == "__main__":
    main()
