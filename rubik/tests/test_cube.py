from rubik.cube import Cube
from rubik.cubie import Face
from rubik.move import Move, create_random_sequence, create_reversed_sequence


def test_apply_simple_moves() -> None:
    cube = Cube()
    simple_moves = [Move.from_string(face.name) for face in Face]

    for move in simple_moves:
        for _ in range(3):
            cube.apply(move)
            assert not cube.solved
        cube.apply(move)
        assert cube.solved


def test_apply_prime_moves() -> None:
    cube = Cube()
    prime_moves = [Move.from_string(f"{face.name}'") for face in Face]

    for move in prime_moves:
        for _ in range(3):
            cube.apply(move)
            assert not cube.solved
        cube.apply(move)
        assert cube.solved


def test_apply_2_moves() -> None:
    cube = Cube()
    prime_moves = [Move.from_string(f"{face.name}2") for face in Face]

    for move in prime_moves:
        cube.apply(move)
        assert not cube.solved
        cube.apply(move)
        assert cube.solved


def test_apply_random_sequence() -> None:
    cube = Cube()
    sequence = create_random_sequence(42)

    cube.apply_sequence(sequence)
    reversed_sequence = create_reversed_sequence(sequence)
    cube.apply_sequence(reversed_sequence)
    assert cube.solved
