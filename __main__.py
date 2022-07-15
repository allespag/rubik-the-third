import copy

from rubik.cube import Cube
from rubik.cubie import Corner, CornerCubie, Face
from rubik.move import Move


def test_apply_simple_moves() -> None:
    cube = Cube()
    simple_moves = [Move.from_string(face.name) for face in Face]

    for move in simple_moves:
        print(move)
        for _ in range(4):
            cube.apply(move)
        assert cube.solved


def main() -> None:
    cube = Cube()
    move = Move.from_string("U")

    cube.apply(move)
    print(cube.edge_cubies)


if __name__ == "__main__":
    main()
