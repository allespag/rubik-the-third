import logging
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from alive_progress import alive_bar  # type: ignore

from rubik.constants import MOVE_COUNT
from rubik.cube import Cube
from rubik.move import MOVE_MAP

MOVE_TABLE_DIRECTORY = "rubik/move_tables"

# logging.basicConfig(format="%(message)s")
logger = logging.getLogger("rubik")
# logger.setLevel(logging.INFO)


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
                    logger.info(f"Loading: {self.path}")
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
            spinner="wait",
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
