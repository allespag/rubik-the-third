import copy
from dataclasses import dataclass, field

from rubik.constants import CORNER_ORIENTATION_COUNT, EDGE_ORIENTATION_COUNT
from rubik.cubie import Corner, CornerCubie, Edge, EdgeCubie
from rubik.move import IS_REPLACED_BY_CORNER_MAP, IS_REPLACED_BY_EDGE_MAP, Move


@dataclass(slots=True)
class Cube:
    edge_cubies: list[EdgeCubie] = field(
        init=False, default_factory=lambda: [EdgeCubie(edge) for edge in Edge]
    )
    corner_cubies: list[CornerCubie] = field(
        init=False, default_factory=lambda: [CornerCubie(corner) for corner in Corner]
    )

    @property
    def solved(self) -> bool:
        return (
            self.edge_cubies == SOLVED_CUBE.edge_cubies
            and self.corner_cubies == SOLVED_CUBE.corner_cubies
        )

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


SOLVED_CUBE = Cube()
