import argparse
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

# 6.87s (from benchmark.py)
# 5.73s (from __main__.py)
# 5.42s (je sais pas pourquoi)
# 2.90s (remove path_set)
# B' L D2 R' F' F L' U2 L B2 B' B R2 B' R' B' F' R U F' D2 B U R D' F2 F2 U' B2 U2 L' D2 R B B' F D2 F U' D L B'

# 8.68s
# L D' B U B' D D2 F' L U2 F' U2 B2 R' D2 U F' L' R2 U B' R2 R U' F' L' B2 D F2 B2 D2 B' U2 R' F' F F2 U' D' F2 R R'

__CHECK_PERF = False
if __CHECK_PERF:
    import cProfile
    import pstats


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

    if __CHECK_PERF:
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

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
