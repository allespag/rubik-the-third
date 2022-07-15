from __future__ import annotations

import copy
from dataclasses import dataclass, field

from rubik.constants import (
    CORNER_COUNT,
    CORNER_ORIENTATION_COUNT,
    CORNER_ORIENTATION_MAX,
    EDGE_COUNT,
    EDGE_ORIENTATION_COUNT,
)
from rubik.cubie import Corner, CornerCubie, Edge, EdgeCubie
from rubik.move import (
    IS_REPLACED_BY_CORNER_MAP,
    IS_REPLACED_BY_EDGE_MAP,
    Move,
    Sequence,
)


@dataclass(slots=True)
class Cube:
    edge_cubies: list[EdgeCubie] = field(
        init=False, default_factory=lambda: [EdgeCubie(edge) for edge in Edge]
    )
    corner_cubies: list[CornerCubie] = field(
        init=False, default_factory=lambda: [CornerCubie(corner) for corner in Corner]
    )

    @classmethod
    def from_sequence(cls, sequence: Sequence) -> Cube:
        cube = Cube()
        cube.apply_sequence(sequence)

        return cube

    @property
    def solved(self) -> bool:
        return (
            self.edge_cubies == SOLVED_CUBE.edge_cubies
            and self.corner_cubies == SOLVED_CUBE.corner_cubies
        )

    # TODO: check if you can replace copy.deepcopy by something faster
    def apply(self, move: Move) -> None:
        new_edge_cubies = IS_REPLACED_BY_EDGE_MAP[move.face]
        new_corner_cubies = IS_REPLACED_BY_CORNER_MAP[move.face]

        for _ in range(move.n):
            edge_cubies_temp = copy.deepcopy(self.edge_cubies)
            for index, edge_cubie in enumerate(new_edge_cubies):
                cubie = edge_cubies_temp[edge_cubie.edge]

                self.edge_cubies[index].edge = cubie.edge
                self.edge_cubies[index].orientation = (
                    cubie.orientation + edge_cubie.orientation
                ) % EDGE_ORIENTATION_COUNT

            corner_cubies_temp = copy.deepcopy(self.corner_cubies)
            for index, corner_cubie in enumerate(new_corner_cubies):
                cubie = corner_cubies_temp[corner_cubie.corner]
                self.corner_cubies[index].corner = cubie.corner
                self.corner_cubies[index].orientation = (
                    cubie.orientation + corner_cubie.orientation
                ) % CORNER_ORIENTATION_COUNT

    def apply_sequence(self, sequence: Sequence) -> None:
        for move in sequence:
            self.apply(move)

    def get_edge_cubies_orientation_coord(self) -> int:
        return sum(
            edge_cubie.orientation * EDGE_ORIENTATION_COUNT ** (EDGE_COUNT - 2 - index)
            for index, edge_cubie in enumerate(self.edge_cubies[:-1])
        )

    def get_corner_cubies_orientation_coord(self) -> int:
        return sum(
            corner_cubie.orientation
            * CORNER_ORIENTATION_COUNT ** (CORNER_COUNT - 2 - index)
            for index, corner_cubie in enumerate(self.corner_cubies[:-1])
        )

    def set_edge_cubies_orientation_coord(self, coord: int) -> None:
        sum_ = 0

        for index, cubie in enumerate(self.edge_cubies[:-1]):
            current = EDGE_ORIENTATION_COUNT ** (EDGE_COUNT - 2 - index)
            cubie.orientation = coord // current
            coord %= current
            sum_ += cubie.orientation

        self.edge_cubies[-1].orientation = (
            EDGE_ORIENTATION_COUNT - (sum_ % EDGE_ORIENTATION_COUNT)
        ) % EDGE_ORIENTATION_COUNT

    def set_corner_cubies_orientation_coord(self, coord: int) -> None:
        sum_ = 0

        for index, cubie in enumerate(self.corner_cubies[:-1]):
            current = CORNER_ORIENTATION_COUNT ** (CORNER_COUNT - 2 - index)
            cubie.orientation = coord // current
            coord %= current
            sum_ += cubie.orientation

        self.corner_cubies[-1].orientation = (
            CORNER_ORIENTATION_COUNT - (sum_ % CORNER_ORIENTATION_COUNT)
        ) % CORNER_ORIENTATION_COUNT


SOLVED_CUBE = Cube()
