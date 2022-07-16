import pickle
from dataclasses import dataclass, field
from operator import mod
from pathlib import Path
from queue import Queue

from rubik.constants import MOVE_COUNT
from rubik.move_table import MoveTable, corners_ori_move_table, edges_ori_move_table

PRUNING_TABLE_DIRECTORY = "rubik/pruning_tables"


@dataclass(slots=True)
class PruningTable:
    filename: str
    move_table_1: MoveTable
    move_table_2: MoveTable
    table: list[list[int]] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        Path(PRUNING_TABLE_DIRECTORY).mkdir(parents=True, exist_ok=True)
        self.move_table_1.load()
        self.move_table_2.load()

    @property
    def path(self) -> str:
        return f"{PRUNING_TABLE_DIRECTORY}/{self.filename}"

    def load(self) -> None:
        try:
            with open(self.path, "rb") as f:
                self.table = pickle.load(f)
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
            print(f"added: {i} {j} @ {depth}")

            for move_index in range(MOVE_COUNT):
                x = self.move_table_1.table[i][move_index]
                y = self.move_table_2.table[j][move_index]

                if (x, y) not in visited:
                    visited.add((x, y))
                    queue.put((x, y, depth + 1))


cubies_orientation_pruning = PruningTable(
    "cubies_orientation.pruning", edges_ori_move_table, corners_ori_move_table
)
