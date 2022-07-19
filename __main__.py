from rubik.cube import Cube
from rubik.cubie import Edge, EdgeCubie
from rubik.move import create_random_sequence
from rubik.solver import Solver


def main() -> None:
    sequence = create_random_sequence(20)
    cube = Cube.from_sequence(sequence)

    solver = Solver()
    solver.run(cube)


if __name__ == "__main__":
    main()
