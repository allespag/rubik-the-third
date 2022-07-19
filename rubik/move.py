from __future__ import annotations

import random
from dataclasses import dataclass

from ordered_set import OrderedSet

from rubik.cubie import Corner, CornerCubie, Edge, EdgeCubie, Face

IS_REPLACED_BY_EDGE_MAP = {
    Face.U: [
        EdgeCubie(Edge.UB, 0),
        EdgeCubie(Edge.UR, 0),
        EdgeCubie(Edge.UF, 0),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.DF, 0),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.DB, 0),
        EdgeCubie(Edge.FR, 0),
        EdgeCubie(Edge.FL, 0),
        EdgeCubie(Edge.BL, 0),
        EdgeCubie(Edge.BR, 0),
    ],
    Face.R: [
        EdgeCubie(Edge.FR, 0),
        EdgeCubie(Edge.UF, 0),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.UB, 0),
        EdgeCubie(Edge.BR, 0),
        EdgeCubie(Edge.DF, 0),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.DB, 0),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.FL, 0),
        EdgeCubie(Edge.BL, 0),
        EdgeCubie(Edge.UR, 0),
    ],
    Face.F: [
        EdgeCubie(Edge.UR, 0),
        EdgeCubie(Edge.FL, 1),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.UB, 0),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.FR, 1),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.DB, 0),
        EdgeCubie(Edge.UF, 1),
        EdgeCubie(Edge.DF, 1),
        EdgeCubie(Edge.BL, 0),
        EdgeCubie(Edge.BR, 0),
    ],
    Face.D: [
        EdgeCubie(Edge.UR, 0),
        EdgeCubie(Edge.UF, 0),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.UB, 0),
        EdgeCubie(Edge.DF, 0),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.DB, 0),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.FR, 0),
        EdgeCubie(Edge.FL, 0),
        EdgeCubie(Edge.BL, 0),
        EdgeCubie(Edge.BR, 0),
    ],
    Face.L: [
        EdgeCubie(Edge.UR, 0),
        EdgeCubie(Edge.UF, 0),
        EdgeCubie(Edge.BL, 0),
        EdgeCubie(Edge.UB, 0),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.DF, 0),
        EdgeCubie(Edge.FL, 0),
        EdgeCubie(Edge.DB, 0),
        EdgeCubie(Edge.FR, 0),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.BR, 0),
    ],
    Face.B: [
        EdgeCubie(Edge.UR, 0),
        EdgeCubie(Edge.UF, 0),
        EdgeCubie(Edge.UL, 0),
        EdgeCubie(Edge.BR, 1),
        EdgeCubie(Edge.DR, 0),
        EdgeCubie(Edge.DF, 0),
        EdgeCubie(Edge.DL, 0),
        EdgeCubie(Edge.BL, 1),
        EdgeCubie(Edge.FR, 0),
        EdgeCubie(Edge.FL, 0),
        EdgeCubie(Edge.UB, 1),
        EdgeCubie(Edge.DB, 1),
    ],
}

IS_REPLACED_BY_CORNER_MAP = {
    Face.U: [
        CornerCubie(Corner.UBR, 0),
        CornerCubie(Corner.URF, 0),
        CornerCubie(Corner.UFL, 0),
        CornerCubie(Corner.ULB, 0),
        CornerCubie(Corner.DFR, 0),
        CornerCubie(Corner.DLF, 0),
        CornerCubie(Corner.DBL, 0),
        CornerCubie(Corner.DRB, 0),
    ],
    Face.R: [
        CornerCubie(Corner.DFR, 2),
        CornerCubie(Corner.UFL, 0),
        CornerCubie(Corner.ULB, 0),
        CornerCubie(Corner.URF, 1),
        CornerCubie(Corner.DRB, 1),
        CornerCubie(Corner.DLF, 0),
        CornerCubie(Corner.DBL, 0),
        CornerCubie(Corner.UBR, 2),
    ],
    Face.F: [
        CornerCubie(Corner.UFL, 1),
        CornerCubie(Corner.DLF, 2),
        CornerCubie(Corner.ULB, 0),
        CornerCubie(Corner.UBR, 0),
        CornerCubie(Corner.URF, 2),
        CornerCubie(Corner.DFR, 1),
        CornerCubie(Corner.DBL, 0),
        CornerCubie(Corner.DRB, 0),
    ],
    Face.D: [
        CornerCubie(Corner.URF, 0),
        CornerCubie(Corner.UFL, 0),
        CornerCubie(Corner.ULB, 0),
        CornerCubie(Corner.UBR, 0),
        CornerCubie(Corner.DLF, 0),
        CornerCubie(Corner.DBL, 0),
        CornerCubie(Corner.DRB, 0),
        CornerCubie(Corner.DFR, 0),
    ],
    Face.L: [
        CornerCubie(Corner.URF, 0),
        CornerCubie(Corner.ULB, 1),
        CornerCubie(Corner.DBL, 2),
        CornerCubie(Corner.UBR, 0),
        CornerCubie(Corner.DFR, 0),
        CornerCubie(Corner.UFL, 2),
        CornerCubie(Corner.DLF, 1),
        CornerCubie(Corner.DRB, 0),
    ],
    Face.B: [
        CornerCubie(Corner.URF, 0),
        CornerCubie(Corner.UFL, 0),
        CornerCubie(Corner.UBR, 1),
        CornerCubie(Corner.DRB, 2),
        CornerCubie(Corner.DFR, 0),
        CornerCubie(Corner.DLF, 0),
        CornerCubie(Corner.ULB, 2),
        CornerCubie(Corner.DBL, 1),
    ],
}


class NotAMoveError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dataclass(slots=True, frozen=True)
class Move:
    face: Face
    n: int

    def __str__(self) -> str:
        modifiers = ["", "2", "'"]
        return f"{self.face.name}{modifiers[self.n - 1]}"

    @classmethod
    def from_string(cls, move_as_string: str) -> Move:
        try:
            return MOVE_MAP[move_as_string]
        except KeyError:
            raise NotAMoveError(f"'{move_as_string}' is not a move.")

    @classmethod
    def from_random(cls) -> Move:
        return random.choice(list(MOVE_MAP.values()))

    def get_reverse(self) -> Move:
        return REVERSE_MOVE_MAP[self]


MOVE_MAP = {
    "U": Move(Face.U, 1),
    "R": Move(Face.R, 1),
    "F": Move(Face.F, 1),
    "D": Move(Face.D, 1),
    "L": Move(Face.L, 1),
    "B": Move(Face.B, 1),
    "U2": Move(Face.U, 2),
    "R2": Move(Face.R, 2),
    "F2": Move(Face.F, 2),
    "D2": Move(Face.D, 2),
    "L2": Move(Face.L, 2),
    "B2": Move(Face.B, 2),
    "U'": Move(Face.U, 3),
    "R'": Move(Face.R, 3),
    "F'": Move(Face.F, 3),
    "D'": Move(Face.D, 3),
    "L'": Move(Face.L, 3),
    "B'": Move(Face.B, 3),
}

REVERSE_MOVE_MAP = {move: Move(move.face, 4 - move.n) for move in MOVE_MAP.values()}

Sequence = list[Move]
Group = OrderedSet[Move]


def create_sequence(sequence_as_string: str) -> Sequence:
    return [
        Move.from_string(move_as_string)
        for move_as_string in sequence_as_string.split(" ")
    ]


def create_reversed_sequence(sequence: Sequence) -> Sequence:
    return [REVERSE_MOVE_MAP[move] for move in sequence][::-1]


def create_random_sequence(length: int = 100) -> Sequence:
    return [Move.from_random() for _ in range(length)]


def create_group(group_as_string: str) -> Group:
    return OrderedSet(
        [
            Move.from_string(move_as_string)
            for move_as_string in group_as_string.split(" ")
        ]
    )


G0 = create_group(" ".join(move_name for move_name in MOVE_MAP))
G1 = create_group("U U' U2 D D' D2 R2 L2 F2 B2")
