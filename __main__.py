from rubik.cube import Cube
from rubik.cubie import Edge, EdgeCubie
from rubik.move import create_random_sequence
from rubik.pruning_table import cubies_ori_pruning, edges_ori_UD_slice_perm
from rubik.solver import Solver


def main() -> None:
    sequence = create_random_sequence(20)
    cube = Cube.from_sequence(sequence)

    solver = Solver()
    solver.run(cube)


if __name__ == "__main__":
    main()
