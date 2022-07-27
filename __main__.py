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
