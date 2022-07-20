import argparse

from rubik.cube import Cube
from rubik.move import create_random_sequence, create_sequence, sequence_to_readable
from rubik.solver import Solver

__CHECK_PERF = True
if __CHECK_PERF:
    import cProfile
    import pstats

# this sequence takes 11.47s
# sequence = create_sequence("F L D2 F2 R2 B2 F R B L2 B F L2 B2 D'")


def main(args: argparse.Namespace) -> None:
    if args.sequence:
        sequence = create_sequence(args.sequence)
    else:
        sequence = create_random_sequence(args.random)

    sequence = create_sequence("F L D2 F2 R2 B2 F R B L2 B F L2 B2 D'")

    cube = Cube.from_sequence(sequence)
    solver = Solver()

    print(f"\nSolving: {sequence_to_readable(sequence)}")

    if __CHECK_PERF:
        profile = cProfile.Profile()
        solution = profile.runcall(solver.run, cube)
        ps = pstats.Stats(profile)
        ps.print_stats()
    else:
        solution = solver.run(cube)

    print(f"{sequence_to_readable(solution)} ({len(solution)} moves)")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="rubik")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("sequence", nargs="?")
    group.add_argument("--random", type=int)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
