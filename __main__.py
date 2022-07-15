from rubik.cube import Cube
from rubik.move import Move, create_random_sequence


def main() -> None:
    cube = Cube()
    move = Move.from_string("R")
    cube.apply(move)

    seed = cube.get_corner_cubies_orientation_coord()

    other = Cube()
    other.set_corner_cubies_orientation_coord(seed)

    for cubie in other.corner_cubies:
        print(cubie.orientation)


if __name__ == "__main__":
    main()
