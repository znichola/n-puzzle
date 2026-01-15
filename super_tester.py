import subprocess
import argparse

import utils as u

nb_test = {3: 10, 4: 10, 5: 6, 6:4, 7:3}

def setUpArgs():
    parser = argparse.ArgumentParser(description=("N-puzzle solver\n"), add_help=False)
    parser.add_argument(
        "-c",
        default="all",
        type= int or str,
        choices=[3, 4, 5, 6, 7, "all"]
    )
    parser.add_argument(
        "-h",
        type=str,
        default="Manhattan",
        choices=["Euclidean", "Manhattan", "Linear"]
    )
    parser.add_argument(
        "-a",
        type=str,
        default="ASWiki",
        choices=["ASWiki", "ASDocs", "IDA"]
    )
    parser.add_argument(
        "-f",
        type=str,
        default="Default",
        choices=["Default", "Greedy", "UniformCost"],
    )
    parser.add_argument(
        "-r",
        type=int,
        default=3,
        choices=list(range(3, 7))
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="Print progress"
    )
    return parser.parse_args()

def start_process(file, args):
    subprocess.run(["python", "puzzle.py", args, file])

def test(n, args):
    for i in range(nb_test[n]):
        start_process(f"test_cases/{n}x{n}_{i}.txt", args)
    return

def args_to_list(args):
    args_list = ""

    if args.c != "all":
        args_list += ["-c", str(args.c)]

    args_list += ["-h", args.h]
    args_list += ["-a", args.a]
    args_list += ["-f", args.f]
    args_list += ["-r", str(args.r)]

    if args.p:
        args_list.append("-p")

    return args_list

def main():
    args = setUpArgs()
    args_list = args_to_list(args)
    if args.c == "all":
        for n in range(3, 7):
            test(n, args_list)
    else:
        test(args.c, args_list)
    return


if __name__ == "__main__":
    main()
