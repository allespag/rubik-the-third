import logging
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from queue import Queue

from alive_progress import alive_bar  # type: ignore

from rubik.cube import Cube
from rubik.move import G0, Group
from rubik.move_table import MoveTable

PRUNING_TABLE_DIRECTORY = "rubik/pruning_tables"

logging.basicConfig(format="%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(slots=True)
class PruningTable:
    filename: str
    move_table_1: MoveTable
    move_table_2: MoveTable
    group: Group = G0
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
                    logger.info(f"Loading: {self.path}")
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
        visited.add((0, 0))
        with alive_bar(
            self.move_table_1.size * self.move_table_2.size,
            title=self.filename,
            title_length=30,
            spinner="wait3",
            spinner_length=25,
        ) as bar:  # type: ignore
            while not queue.empty():
                i, j, depth = queue.get()
                table[i][j] = depth
                bar()

                for move in self.group:
                    move_index = move.coord
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
