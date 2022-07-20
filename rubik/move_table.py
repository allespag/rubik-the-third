import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from alive_progress import alive_bar  # type: ignore

from rubik.constants import (
    CORNER_ORIENTATION_MAX,
    CORNER_PERMUTATION_MAX,
    EDGE_ORIENTATION_MAX,
    EXACT_UD_SLICE_PERMUTATION_MAX,
    MOVE_COUNT,
    NOT_UD_SLICE_PERMUTATION_MAX,
    UD_SLICE_PERMUTATION_MAX,
)
from rubik.cube import Cube
from rubik.move import MOVE_MAP

MOVE_TABLE_DIRECTORY = "rubik/move_tables"


@dataclass(slots=True)
class MoveTable:
    filename: str
    size: int
    getter: Callable[[Cube], int]
    setter: Callable[[Cube, int], None]
    table: list[list[int]] = field(init=False, default_factory=list, repr=False)
    loaded: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        Path(MOVE_TABLE_DIRECTORY).mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> str:
        return f"{MOVE_TABLE_DIRECTORY}/{self.filename}"

    def load(self) -> None:
        if not self.loaded:
            try:
                with open(self.path, "rb") as f:
                    self.table = pickle.load(f)
                self.loaded = True
            except:
                self.populate()
                self.load()

    def populate(self) -> None:
        cube = Cube()
        table = [[-1 for _ in range(MOVE_COUNT)] for _ in range(self.size)]

        with alive_bar(
            self.size,
            title=self.filename,
            title_length=30,
            spinner="wait3",
            spinner_length=25,
        ) as bar:  # type: ignore
            for i in range(self.size):
                self.setter(cube, i)

                for index, move in enumerate(MOVE_MAP.values()):
                    cube.apply(move)
                    table[i][index] = self.getter(cube)
                    cube.apply(move.get_reverse())
                bar()

        with open(self.path, "wb") as f:
            pickle.dump(table, f)


edges_ori_move_table = MoveTable(
    "edges_orientation.pickle",
    EDGE_ORIENTATION_MAX,
    Cube.get_edge_cubies_orientation_coord,
    Cube.set_edge_cubies_orientation_coord,
)

corners_ori_move_table = MoveTable(
    "corners_orientation.pickle",
    CORNER_ORIENTATION_MAX,
    Cube.get_corner_cubies_orientation_coord,
    Cube.set_corner_cubies_orientation_coord,
)

UD_slice_perm_move_table = MoveTable(
    "UD_slice_permutation.pickle",
    UD_SLICE_PERMUTATION_MAX,
    Cube.get_UD_slice_permutation_coord,
    Cube.set_UD_slice_permutation_coord,
)

corners_perm_move_table = MoveTable(
    "corners_permutation.pickle",
    CORNER_PERMUTATION_MAX,
    Cube.get_corner_cubies_permutation_coord,
    Cube.set_corner_cubies_permutation_coord,
)

exact_UD_slice_perm_move_table = MoveTable(
    "exact_UD_slice_permutation.pickle",
    EXACT_UD_SLICE_PERMUTATION_MAX,
    Cube.get_exact_UD_slice_permuation_coord,
    Cube.set_exact_UD_slice_permuation_coord,
)

not_UD_slice_perm_move_table = MoveTable(
    "not_UD_slice_permutation.pickle",
    NOT_UD_SLICE_PERMUTATION_MAX,
    Cube.get_not_UD_slice_permutation_coord,
    Cube.set_not_UD_slice_permutation_coord,
)
