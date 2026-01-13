import heapq
import math
from collections import defaultdict

import utils as u
from heuristic import Heuristic

C = 1

class Board:

    def __init__(self, size, heuristic="Manhattan"):
        self.target = tuple(u.getResult(size))
        self.size = size
        self.heuristic = Heuristic(size, heuristic)


    def a_star(self, grid: tuple):
        opened_set = set([grid])
        opened_heap = [] ; heapq.heapify(opened_heap) ; heapq.heappush(opened_heap, (0.0, grid))
        cameFrom = {} ; cameFrom[grid] = "start"
        gScore = defaultdict(lambda: math.inf) ; gScore[grid] = 0.0 # default value of infinity
        fScore = {} ; fScore[grid] = self.heuristic.h(grid)

        totalOpened = 1

        while len(opened_heap):
            f, current = heapq.heappop(opened_heap) ; opened_set.remove(current)
            print(f"fScore {f}")
            if current == self.target:
                return self.reconstruct_path(cameFrom, current, totalOpened, fScore)

            neighbours = self.expand(current)
            for neighbour in neighbours:

                tentative_gScore = gScore[current] + C
                if tentative_gScore < gScore[neighbour]:
                    cameFrom[neighbour] = current
                    gScore[neighbour] = tentative_gScore
                    fScore[neighbour] = tentative_gScore + self.heuristic.h(neighbour)
                    if neighbour not in opened_set:
                        opened_set.add(neighbour) 
                        heapq.heappush(opened_heap, (fScore[neighbour], neighbour))
                        totalOpened += 1
        return None

    def reconstruct_path(self, cameFrom: dict, current, totalOpened, fScore):
        sequence = []
        while current != "start":
            sequence.insert(0, current)
            current = cameFrom[current]


        return {"isSolvable": True, "TotalOpened": totalOpened, "TotalState": len(fScore), "LenSequence": len(sequence), "Sequence": sequence}

    def expand(self, grid: tuple) -> list[tuple]:
        '''returns a list of ids'''
        def getNeighbouringStates(state_hash):
            def getNeighbours(index):
                max_val = pow(self.size, 2)
                return list(filter(
                    lambda v: v >= 0 and v < max_val and 
                    (int(v / self.size) == int(index / self.size) or int(v % self.size) == int(index % self.size)),
                    [index-self.size, index+1, index+self.size, index-1]
                    ))
            states = []
            index = grid.index(0)
            neighbours = getNeighbours(index)
            for n in neighbours:
                newState = list(grid)
                newState[n], newState[index] = newState[index], newState[n]
                states.append(tuple(newState))
            return states
        return getNeighbouringStates(grid)


def main():

    args = u.setUpArgs()
    size, grid = u.getPuzzle(args)

    Puzzle = Board(size)

    result = Puzzle.a_star(tuple(grid))
    if result:
        print("This Puzzle is solvable.")
        print("Complexity in time : total opened states", result["TotalOpened"])
        print("Complexity in size : num states in memory", result["TotalState"])
        print("Number of moves : ", result["LenSequence"])
        print("The ordered sequence : solution.txt")
        print(result["Sequence"])
    else:
        print("This Puzzle is unsolvable.")
        exit(1)
    




if __name__ == "__main__":
    main()
