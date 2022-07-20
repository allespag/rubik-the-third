from rubik.cube import Cube
from rubik.cubie import Edge
from rubik.move import create_random_sequence


def test_edge_cubies_orientation_coord() -> None:
    for _ in range(100):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_edge_cubies_orientation_coord()

        other = Cube()
        other.set_edge_cubies_orientation_coord(coord)

        for edge_cubie_1, edge_cubie_2 in zip(cube.edge_cubies, other.edge_cubies):
            assert edge_cubie_1.orientation == edge_cubie_2.orientation


def test_corner_cubies_orientation_coord() -> None:
    for _ in range(100):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_corner_cubies_orientation_coord()

        other = Cube()
        other.set_corner_cubies_orientation_coord(coord)

        for corner_cubie_1, corner_cubie_2 in zip(
            cube.corner_cubies, other.corner_cubies
        ):
            assert corner_cubie_1.orientation == corner_cubie_2.orientation


def test_UD_slice_permutation_coord() -> None:
    UD_slice_edges = [
        Edge.FR,
        Edge.BL,
        Edge.FL,
        Edge.BR,
    ]

    for _ in range(10):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_UD_slice_permutation_coord()

        other = Cube()
        other.set_UD_slice_permutation_coord(coord)

        for edge_cubie_1, edge_cubie_2 in zip(cube.edge_cubies, other.edge_cubies):
            assert (
                edge_cubie_1.edge in UD_slice_edges
                and edge_cubie_2.edge in UD_slice_edges
            ) or (
                edge_cubie_1.edge not in UD_slice_edges
                and edge_cubie_2.edge not in UD_slice_edges
            )


def test_corner_cubies_permutation_coord() -> None:
    for _ in range(100):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_corner_cubies_permutation_coord()

        other = Cube()
        other.set_corner_cubies_permutation_coord(coord)

        for corner_cubie_1, corner_cubie_2 in zip(
            cube.corner_cubies, other.corner_cubies
        ):
            assert corner_cubie_1.corner == corner_cubie_2.corner


def test_exact_UD_slice_permutation_coord() -> None:
    for _ in range(10):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_exact_UD_slice_permuation_coord()

        other = Cube()
        other.set_exact_UD_slice_permuation_coord(coord)

        assert coord == other.get_exact_UD_slice_permuation_coord()


def test_not_UD_slice_permutation_coord() -> None:
    for _ in range(10):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_not_UD_slice_permutation_coord()

        other = Cube()
        other.set_not_UD_slice_permutation_coord(coord)

        assert coord == other.get_not_UD_slice_permutation_coord()
