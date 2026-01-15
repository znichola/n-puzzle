from algo import Algorithm
import utils as u
import time

class Puzzle(Algorithm):

    def __init__(self, args, size) -> None:
        Algorithm.__init__(self, size, args.a, args.h, args.f, args.p)
        
        self.res_sequence = []

    def print_result(self, result):
        if result:
            print("This Puzzle is solvable.")
            print("Complexity in time : total opened states", result["TotalOpened"])
            print("Complexity in size : num states in memory", result["TotalStateMem"])
            print("Number of moves : ", result["LenSequence"])
            u.print_tab_to_file(result["Sequence"])
            print("The ordered sequence : solution.txt")
        else:
            print("This Puzzle is unsolvable.")
            exit(1)


def main():

    args = u.setUpArgs()
    size, grid = u.getPuzzle(args)
    
    puzzle = Puzzle(args, size)
    start = time.perf_counter()
    result = puzzle.solve(tuple(grid))
    end = time.perf_counter()
    puzzle.print_result(result)
    print(f"Solve time: {end - start:.6f} seconds")

if __name__ == "__main__":
    main()