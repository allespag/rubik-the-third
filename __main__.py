from rubik.constants import EXACT_UD_SLICE_PERMUTATION_MAX
from rubik.cube import Cube
from rubik.cubie import Edge
from rubik.move import Move, create_random_sequence, create_sequence
from rubik.move_table import (
    UD_slice_perm_move_table,
    corners_perm_move_table,
    exact_UD_slice_perm_move_table,
    not_UD_slice_perm_move_table,
)
from rubik.pruning_table import corner_cubies_perm_exact_UD_slice_pruning
from rubik.solver import Solver


def main_test() -> None:
    pass


def main() -> None:
    sequence = create_random_sequence(20)
    cube = Cube.from_sequence(sequence)

    solver = Solver()
    res = solver.run(cube)
    print(res)


if __name__ == "__main__":
    main()
