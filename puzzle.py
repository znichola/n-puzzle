from algo import Algorithm
import utils as u

class Puzzle(Algorithm):

    def __init__(self, args, size) -> None:
        Algorithm.__init__(self, size, args.a, args.h, args.f)
        
        self.res_sequence = []

    def print_result(self, result):
        if result:
            print("This Puzzle is solvable.")
            print("Complexity in time : total opened states", result["TotalOpened"])
            print("Complexity in size : num states in memory", result["TotalState"])
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
    result = puzzle.solve(tuple(grid))
    puzzle.print_result(result)
    
if __name__ == "__main__":
    main()