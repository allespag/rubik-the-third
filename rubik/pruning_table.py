import pickle
from dataclasses import dataclass, field
from pathlib import Path
from queue import Queue

from rubik.constants import MOVE_COUNT
from rubik.cube import Cube
from rubik.move_table import (
    MoveTable,
    UD_slice_perm_move_table,
    corners_ori_move_table,
    edges_ori_move_table,
)

PRUNING_TABLE_DIRECTORY = "rubik/pruning_tables"


@dataclass(slots=True)
class PruningTable:
    filename: str
    move_table_1: MoveTable
    move_table_2: MoveTable
    table: list[list[int]] = field(init=False, default_factory=list, repr=False)
    loaded: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        Path(PRUNING_TABLE_DIRECTORY).mkdir(parents=True, exist_ok=True)
        self.move_table_1.load()
        self.move_table_2.load()

    @property
    def path(self) -> str:
        return f"{PRUNING_TABLE_DIRECTORY}/{self.filename}"

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
        table = [
            [-1 for _ in range(self.move_table_2.size)]
            for _ in range(self.move_table_1.size)
        ]
        queue: Queue[tuple[int, int, int]] = Queue()
        visited: set[tuple[int, int]] = set()

        queue.put((0, 0, 0))

        while not queue.empty():
            i, j, depth = queue.get()
            table[i][j] = depth

            for move_index in range(MOVE_COUNT):
                x = self.move_table_1.table[i][move_index]
                y = self.move_table_2.table[j][move_index]

                if (x, y) not in visited:
                    visited.add((x, y))
                    queue.put((x, y, depth + 1))

        with open(self.path, "wb") as f:
            pickle.dump(table, f)

    def compute(self, cube: Cube) -> int:
        x = self.move_table_1.getter(cube)
        y = self.move_table_2.getter(cube)

        return self.table[x][y]


cubies_ori_pruning = PruningTable(
    "cubies_orientation.pickle",
    edges_ori_move_table,
    corners_ori_move_table,
)

edges_ori_UD_slice_perm_pruning = PruningTable(
    "edges_orientation_UD_slice_permutation.pickle",
    edges_ori_move_table,
    UD_slice_perm_move_table,
)
