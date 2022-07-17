from dataclasses import dataclass

from rubik.cube import Cube
from rubik.move import Sequence


@dataclass(slots=True, frozen=True)
class Solver:
    def run(self, cube: Cube) -> Sequence:
        raise NotImplementedError
