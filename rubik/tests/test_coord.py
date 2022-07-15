from rubik.cube import Cube
from rubik.move import create_random_sequence


def test_edge_cubies_orientation_coord() -> None:
    for _ in range(10):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_edge_cubies_orientation_coord()

        other = Cube()
        other.set_edge_cubies_orientation_coord(coord)

        for edge_cubie_1, edge_cubie_2 in zip(cube.edge_cubies, other.edge_cubies):
            assert edge_cubie_1.orientation == edge_cubie_2.orientation


def test_corner_cubies_orientation_coord() -> None:
    for _ in range(10):
        sequence = create_random_sequence()
        cube = Cube.from_sequence(sequence)
        coord = cube.get_corner_cubies_orientation_coord()

        other = Cube()
        other.set_corner_cubies_orientation_coord(coord)

        for corner_cubie_1, corner_cubie_2 in zip(
            cube.corner_cubies, other.corner_cubies
        ):
            assert corner_cubie_1.orientation == corner_cubie_2.orientation
