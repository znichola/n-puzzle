from collections import defaultdict
import heapq
import math

from heuristic import Heuristic
from fScore import Fscore
import utils as u

C = 1

class Algorithm(Heuristic, Fscore):

    def __init__(self, size, algo, heuristic, f_type) -> None:
        Heuristic.__init__(self, size, heuristic)
        Fscore.__init__(self, f_type)
        self.size = size
        self.solve = {
            "ASWiki": self.a_star_wiki, 
            "ASDocs": self.a_star_docs,
            "IDA": self.ida,
            }[algo]
        self.target = tuple(u.getResult(size))

    def a_star_wiki(self, grid):
        '''graph-search version of A* : see wiki article on A*'''
        opened_set = set([grid])
        opened_heap = [] ; heapq.heapify(opened_heap) ; heapq.heappush(opened_heap, (0.0, grid))
        cameFrom = {} ; cameFrom[grid] = "start"
        gScore = defaultdict(lambda: math.inf) ; gScore[grid] = 0.0 # default value of infinity
        fScore = {} ; fScore[grid] = self.h(grid)

        totalOpened = 1

        while len(opened_heap):
            f, current = heapq.heappop(opened_heap)
            if current not in opened_set:
                continue
            opened_set.remove(current)

            if totalOpened % 1000 == 0:
                self.progress_print(f, current)

            if current == self.target:
                return self.reconstruct_path(cameFrom, current, totalOpened, fScore)

            neighbours = self.expand(current)
            for neighbour in neighbours:

                tentative_gScore = gScore[current] + C
                if tentative_gScore < gScore[neighbour]:
                    cameFrom[neighbour] = current
                    gScore[neighbour] = tentative_gScore
                    fScore[neighbour] = self.f(tentative_gScore, self.h(neighbour))
                    heapq.heappush(opened_heap, (fScore[neighbour], neighbour))
                    if neighbour not in opened_set:
                        opened_set.add(neighbour)
                        totalOpened += 1
        return None

    def a_star_docs(self, grid):
        opened_set = set([grid])
        closed_set = set()
        opened_heap = [] ; heapq.heapify(opened_heap) ; heapq.heappush(opened_heap, (0.0, grid))
        cameFrom = {} ; cameFrom[grid] = "start"
        gScore = defaultdict(lambda: math.inf) ; gScore[grid] = 0.0
        fScore = {} ; fScore[grid] = self.h(grid)
        totalOpened = 1

        while len(opened_heap):
            f, current = heapq.heappop(opened_heap)
            # if current not in opened_set:
            #     continue

            if totalOpened % 1000 == 0:
                self.progress_print(f, current)

            if current == self.target:
                return self.reconstruct_path(cameFrom, current, totalOpened, fScore)

            opened_set.remove(current)
            closed_set.add(current)

            neighbours = self.expand(current)
            for neighbour in neighbours:
                tentative_gScore = gScore[current] + C
                if (not neighbour in opened_set) and (not neighbour in closed_set):
                    cameFrom[neighbour] = current
                    gScore[neighbour] = tentative_gScore
                    fScore[neighbour] = self.f(tentative_gScore, self.h(neighbour))
                    heapq.heappush(opened_heap, (fScore[neighbour], neighbour)); opened_set.add(neighbour); totalOpened += 1
                elif fScore[neighbour] > gScore[current] + self.h(neighbour) + C:
                    gScore[neighbour] = gScore[current] + C
                    cameFrom[neighbour] = current
                    if neighbour in closed_set:
                        closed_set.remove(neighbour)
                        opened_set.add(neighbour)
        return None


    def ida(self, grid):
        bound = self.h(grid)
        path = [grid] # current search path, use like a stack
        stats = {"count": 0}
        stats["max_mem"] = len(path)
        def search(g, bound):
            node: tuple = path[-1]
            f = self.f(g, self.h(node)) ; stats["count"] += 1
            if f > bound:
                return f
            elif node == self.target:
                return "FOUND"
            mmin = math.inf
            if stats["count"] % 1000 == 0:
                self.progress_print(f, node)
            neighbours =  sorted(
                self.expand(node),
                key=lambda n: self.h(n)
            )
            for neighbour in neighbours:
                if neighbour not in path:
                    path.append(neighbour)
                    stats["max_mem"] = len(path) if stats["max_mem"] < len(path) else stats["max_mem"]
                    t = search(g + C, bound)
                    if t == "FOUND":
                        return "FOUND"
                    elif t < mmin:
                        mmin = t
                    path.pop()

            return mmin

        while True:
            t = search(0, bound)
            if t == "FOUND":
                break
            if t == math.inf:
                t = "NOT_FOUND"
                break
            bound = t

        return self.ret_dict(True if t == "FOUND" else False, stats["count"], stats["max_mem"], len(path), path)


    def progress_print(self, fScore, current):
        grid_str = u.gridToString(current)
        lines = self.size + 2  # grid lines + fScore line
        print(
            f"\033[{lines}F"
            f"\n{grid_str}\n"
            f"fScore: {fScore}",
            flush=True
        )

    def expand(self, grid: tuple) -> list[tuple]:
        '''returns a list of ids'''
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


    def reconstruct_path(self, cameFrom: dict, current, totalOpened, fScore):
            sequence = []
            while current != "start":
                sequence.insert(0, current)
                current = cameFrom[current]
            return self.ret_dict(True, totalOpened, len(fScore), len(sequence), sequence)


    def ret_dict(self, isSolvable, totalOpened, totalState, lenSequence, sequence):
        return {"isSolvable": isSolvable, "TotalOpened": totalOpened, "TotalState": totalState, "LenSequence": lenSequence, "Sequence": sequence}
