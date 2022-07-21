import argparse

from rubik.cube import Cube
from rubik.move import create_random_sequence, create_sequence, sequence_to_readable
from rubik.solver import Solver

__CHECK_PERF = False
if __CHECK_PERF:
    import cProfile
    import pstats

# this sequence takes 11.47s -> 4.75s (dunno why) -> 4.61s
# sequence = create_sequence("F L D2 F2 R2 B2 F R B L2 B F L2 B2 D'")

# this sequence takes 17.07s -> 16.53s
#  F B' F F2 F2 L' L2 L R2 L2 U U' R2 L2 F' F2 L' R' B2 B' R R2 F' B2 F' F U' F D2 U D2 L2 F2 L R2 L2 B2 U U2 L L' B F2 F2 D2 U2 R2 B' L F R2 L R2 U2 U2 L' D2 B U' F U2 F' D2 U2 U' D2 F2 L R2 R2 L D2 D F D' F2 B2 D F L' U B' L F B2 L2 D' L' U' F2 B' F' D2 B2 F' B F' U U' U


def main(args: argparse.Namespace) -> None:
    if args.sequence:
        sequence = create_sequence(args.sequence)
    else:
        sequence = create_random_sequence(args.random)

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
