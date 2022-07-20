from rubik.constants import EXACT_UD_SLICE_PERMUTATION_MAX
from rubik.cube import Cube
from rubik.cubie import Edge
from rubik.move import (
    Move,
    create_random_sequence,
    create_sequence,
    sequence_to_readable,
)
from rubik.move_table import (
    MoveTable,
    UD_slice_perm_move_table,
    corners_perm_move_table,
    exact_UD_slice_perm_move_table,
    not_UD_slice_perm_move_table,
)
from rubik.pruning_table import (
    PruningTable,
    corner_cubies_perm_exact_UD_slice_pruning,
    cubies_ori_pruning,
    edges_ori_UD_slice_perm_pruning,
    edges_perm_pruning,
)
from rubik.solver import Solver

# MOVE TABLES
# exact_UD_slice_perm_move_table    [OK]
# corners_perm_move_table           [OK]
# not_UD_slice_perm_move_table      [OK]

# PRUNING TABLES


def print_mt_cpp_order(to_test: MoveTable) -> None:
    order: list[int] = []
    for i in range(6):
        order.append(i)
        order.append(i + 6)
        order.append(i + 12)

    to_test.populate()
    to_test.load()

    for index, elem in enumerate(to_test.table):
        res = " ".join(str(elem[o]) for o in order)
        print(f"#{index}: [{res} ]s")


def print_pt(to_test: PruningTable) -> None:
    to_test.populate()
    to_test.load()

    for elem in to_test.table:
        print(elem)


def main_test() -> None:
    print_pt(corner_cubies_perm_exact_UD_slice_pruning)


def main() -> None:
    sequence = create_random_sequence(20)

    cube = Cube.from_sequence(sequence)

    print(sequence_to_readable(sequence))

    solver = Solver()
    solution = solver.run(cube)

    print(sequence_to_readable(solution))


if __name__ == "__main__":
    main()
