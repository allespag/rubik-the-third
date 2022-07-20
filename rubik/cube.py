from __future__ import annotations

import copy
from dataclasses import dataclass, field
from math import factorial

from rubik.constants import (
    CORNER_COUNT,
    CORNER_ORIENTATION_COUNT,
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
from rubik.utils import binomial


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

    # This is the old apply function, remove it when you want
    def apply_slow__OLD(self, move: Move) -> None:
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

    def apply(self, move: Move) -> None:
        for _ in range(move.n):
            new_edge_cubies: list[EdgeCubie] = []
            for edge_cubie in IS_REPLACED_BY_EDGE_MAP[move.face]:
                cubie = self.edge_cubies[edge_cubie.edge]

                edge = cubie.edge
                orientation = (
                    cubie.orientation + edge_cubie.orientation
                ) % EDGE_ORIENTATION_COUNT
                new_edge_cubies.append(EdgeCubie(edge, orientation))

            new_corner_cubies: list[CornerCubie] = []
            for corner_cubie in IS_REPLACED_BY_CORNER_MAP[move.face]:
                cubie = self.corner_cubies[corner_cubie.corner]

                corner = cubie.corner
                orientation = (
                    cubie.orientation + corner_cubie.orientation
                ) % CORNER_ORIENTATION_COUNT
                new_corner_cubies.append(CornerCubie(corner, orientation))

            self.edge_cubies = new_edge_cubies
            self.corner_cubies = new_corner_cubies

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

    def get_UD_slice_permutation_coord(self) -> int:
        coord = 0
        k = -1

        for n, cubie in enumerate(self.edge_cubies):
            if cubie.edge in [Edge.FR, Edge.FL, Edge.BL, Edge.BR]:
                k += 1
            elif k != -1:
                coord += binomial(n, k)

        return coord

    def get_corner_cubies_permutation_coord(self) -> int:
        coord = 0

        for index, cubie in enumerate(self.corner_cubies):
            higher_corner_count = sum(
                left_cubie.corner > cubie.corner
                for left_cubie in self.corner_cubies[:index]
            )
            coord += higher_corner_count * factorial(index)

        return coord

    def get_exact_UD_slice_permuation_coord(self) -> int:
        edges: list[Edge] = []
        UD_slice_edges = [
            Edge.FR,
            Edge.FL,
            Edge.BL,
            Edge.BR,
        ]

        for cubie in self.edge_cubies:
            if cubie.edge in UD_slice_edges:
                edges.append(cubie.edge)

        coord = 0
        for index, edge in reversed(list(enumerate(edges))):
            if index == 0:
                break
            sum_ = sum(left_edge > edge for left_edge in edges[:index])
            coord = (coord + sum_) * index

        return coord

    def get_not_UD_slice_permutation_coord(self) -> int:
        coord = 0

        for index, cubie in enumerate(self.edge_cubies[: Edge.DB + 1]):
            higher_corner_count = sum(
                left_cubie.edge > cubie.edge for left_cubie in self.edge_cubies[:index]
            )
            coord += higher_corner_count * factorial(index)

        return coord

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

    def set_UD_slice_permutation_coord(self, coord: int) -> None:
        remaining_not_UD_slice_edges = [
            Edge.UR,
            Edge.UF,
            Edge.UL,
            Edge.UB,
            Edge.DR,
            Edge.DF,
            Edge.DL,
            Edge.DB,
        ]
        remaining_UD_slice_edges = [
            Edge.FR,
            Edge.BL,
            Edge.FL,
            Edge.BR,
        ]
        n = EDGE_COUNT - 1
        k = 3

        while coord:
            current = binomial(n, k)

            if current > coord:
                edge = remaining_UD_slice_edges.pop()
                k -= 1
            else:
                edge = remaining_not_UD_slice_edges.pop()
                coord -= current

            self.edge_cubies[n].edge = edge
            n -= 1

        while n >= 0:
            if k >= 0:
                edge = remaining_UD_slice_edges.pop()
                k -= 1
            else:
                edge = remaining_not_UD_slice_edges.pop()

            self.edge_cubies[n].edge = edge
            n -= 1

    def set_corner_cubies_permutation_coord(self, coord: int) -> None:
        remaining_corners = list(Corner)

        for index, cubie in reversed(list(enumerate(self.corner_cubies))):
            higher_corner_count = coord // factorial(index)
            coord %= factorial(index)

            cubie.corner = remaining_corners[
                len(remaining_corners) - higher_corner_count - 1
            ]
            remaining_corners.remove(cubie.corner)

    def set_exact_UD_slice_permuation_coord(self, coord: int) -> None:
        remaining_UD_slice_edges = [
            Edge.FR,
            Edge.FL,
            Edge.BL,
            Edge.BR,
        ]

        for index, cubie in reversed(
            list(enumerate(self.edge_cubies[Edge.FR : Edge.BR + 1]))
        ):
            higher_edge_count = coord // factorial(index)
            coord %= factorial(index)

            cubie.edge = remaining_UD_slice_edges[
                len(remaining_UD_slice_edges) - higher_edge_count - 1
            ]
            remaining_UD_slice_edges.remove(cubie.edge)

    def set_not_UD_slice_permutation_coord(self, coord: int) -> None:
        remaining_corners = list(Edge)[: Edge.DB + 1]

        for index, cubie in reversed(list(enumerate(self.edge_cubies[: Edge.DB + 1]))):
            higher_corner_count = coord // factorial(index)
            coord %= factorial(index)

            cubie.edge = remaining_corners[
                len(remaining_corners) - higher_corner_count - 1
            ]
            remaining_corners.remove(cubie.edge)


SOLVED_CUBE = Cube()
