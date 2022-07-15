from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto


class Face(IntEnum):
    U = 0
    R = auto()
    F = auto()
    D = auto()
    L = auto()
    B = auto()

    @classmethod
    def from_string(cls, face_as_string: str) -> Face:
        return cls([label.name for label in Face].index(face_as_string))


class Edge(IntEnum):
    UR = 0
    UF = auto()
    UL = auto()
    UB = auto()
    DR = auto()
    DF = auto()
    DL = auto()
    DB = auto()
    FR = auto()
    FL = auto()
    BL = auto()
    BR = auto()


class Corner(IntEnum):
    URF = 0
    UFL = auto()
    ULB = auto()
    UBR = auto()
    DFR = auto()
    DLF = auto()
    DBL = auto()
    DRB = auto()


@dataclass(slots=True)
class EdgeCubie:
    edge: Edge
    orientation: int = 0


@dataclass(slots=True)
class CornerCubie:
    corner: Corner
    orientation: int = 0
