from __future__ import annotations

from dataclasses import dataclass

from ordered_set import OrderedSet

from rubik.cubie import Corner, CornerCubie, Edge, EdgeCubie, Face

MOVE_MAP = {
    "U": (Face.U, 1),
    "R": (Face.R, 1),
    "F": (Face.F, 1),
    "D": (Face.D, 1),
    "L": (Face.L, 1),
    "B": (Face.B, 1),
    "U2": (Face.U, 2),
    "R2": (Face.R, 2),
    "F2": (Face.F, 2),
    "D2": (Face.D, 2),
    "L2": (Face.L, 2),
    "B2": (Face.B, 2),
    "U'": (Face.U, 3),
    "R'": (Face.R, 3),
    "F'": (Face.F, 3),
    "D'": (Face.D, 3),
    "L'": (Face.L, 3),
    "B'": (Face.B, 3),
}

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

    @classmethod
    def from_string(cls, move_as_string: str) -> Move:
        try:
            face, n = MOVE_MAP[move_as_string]
            return cls(face, n)
        except KeyError:
            raise NotAMoveError(f"'{move_as_string}' is not a move.")


Sequence = list[Move]
Group = OrderedSet[Move]


def create_sequence(sequence_as_string: str) -> Sequence:
    return [
        Move.from_string(move_as_string)
        for move_as_string in sequence_as_string.split(" ")
    ]


def create_group(group_as_string: str) -> Group:
    return OrderedSet(
        [
            Move.from_string(move_as_string)
            for move_as_string in group_as_string.split(" ")
        ]
    )
