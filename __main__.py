import argparse
import cProfile
import pstats
import sys

from rubik.cube import Cube
from rubik.move import (
    NotAMoveError,
    create_random_sequence,
    create_sequence,
    sequence_to_readable,
)
from rubik.report import Report
from rubik.solver import Solver

# plus lent avec benchmark -> n = 1000 ; seed = 42
# 5.15s (from benchmark)
# 4.04s (by removing all frozen=True)
# L' F' B' R2 D' F R L2 U2 L B2 R R' D' F' D B' L2 U2 U' U D D' D2 R2 U F2 R B B2 U' R R D2 D U2 D R' U' D' F' B2


def main(args: argparse.Namespace) -> None:
    try:
        if args.sequence:
            sequence = create_sequence(args.sequence)
        elif args.random:
            sequence = create_random_sequence(args.random)
        else:
            sequence = []
    except NotAMoveError as e:
        sys.exit(f"Error: {e}")

    cube = Cube.from_sequence(sequence)
    report = Report(sequence_to_readable(sequence))
    solver = Solver(cube, report)

    print(f"\nSolving: {sequence_to_readable(sequence)}")

    if args.perf:
        profile = cProfile.Profile()
        solution = profile.runcall(solver.run)
        ps = pstats.Stats(profile)
        ps.print_stats()
    else:
        solution = solver.run()

    print(f"In {solver.report.time_taken_in_s:.2f}s")
    print(f"{sequence_to_readable(solution)} ({len(solution)} moves)")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="rubik")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("sequence", nargs="?")
    group.add_argument("--random", "-r", type=int)

    parser.add_argument("--perf", "-p", action="store_true", default=False)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
