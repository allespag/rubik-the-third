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


def print_cpp_order(to_test: MoveTable | PruningTable):
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


def main_test() -> None:
    print_cpp_order(not_UD_slice_perm_move_table)


def main() -> None:
    sequence = create_random_sequence(1000)
    # sequence = create_sequence("D2 L' F2 B D D2 U2 F' U' L B2 R2 B F' B' F2 B2 F F2 R")

    cube = Cube.from_sequence(sequence)

    print(sequence_to_readable(sequence))

    solver = Solver()
    solution = solver.run(cube)

    print(sequence_to_readable(solution))


if __name__ == "__main__":
    main_test()
