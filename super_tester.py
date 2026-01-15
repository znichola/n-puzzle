import subprocess
import argparse

import utils as u

nb_test = {3: 10, 4: 10, 5: 6, 6:4, 7:3}

def setUpArgs():
    parser = argparse.ArgumentParser(description=("N-puzzle solver\n"), add_help=False)
    parser.add_argument(
        "-c",
        default="3",
        type= int,
        choices=[3, 4, 5, 6, 7]
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
        "-p",
        action="store_true",
        help="Print progress"
    )
    return parser.parse_args()

def start_process(file, args):
    cmd = ["python", "puzzle.py"]
    cmd += args
    cmd.append(file)
    subprocess.run(cmd)

def test(n, args):
    for i in range(nb_test[n]):
        start_process(f"test_cases/{n}x{n}_{i}.txt", args)

def args_to_list(args):
    args_list = []

    args_list += ["-h", args.h]
    args_list += ["-a", args.a]
    args_list += ["-f", args.f]

    if args.p:
        args_list.append(f"-p")

    return args_list

def main():
    args = setUpArgs()
    args_list = args_to_list(args)
    test(args.c, args_list)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Something went wrong... :(\n{error}")
        exit()