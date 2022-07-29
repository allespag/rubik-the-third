from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Generator

from rubik.constants import (
    CORNER_ORIENTATION_MAX,
    CORNER_PERMUTATION_MAX,
    EDGE_ORIENTATION_MAX,
    EXACT_UD_SLICE_PERMUTATION_MAX,
    NOT_UD_SLICE_PERMUTATION_MAX,
    UD_SLICE_PERMUTATION_MAX,
)
from rubik.cube import Cube
from rubik.move import G0, G1, Group, Move, Sequence
from rubik.move_table import MoveTable
from rubik.pruning_table import PruningTable
from rubik.report import Report, ReportManager


class NoSolutionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dataclass(slots=True, frozen=True)
class State:
    x: int
    y: int
    z: int
    move: Move | None = None

    def __hash__(self) -> int:
        return (self.x, self.y, self.z).__hash__()

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, State)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def is_goal(self) -> bool:
        return self.x == 0 and self.y == 0 and self.z == 0

    def successors(self, map_: StateMap, group: Group) -> Generator[State, None, None]:
        for move in group:
            if self.move is None or (
                self.move.face != move.face and not self.move.is_opposite(move)
            ):
                move_index = move.coord
                yield State(
                    map_.xs.table[self.x][move_index],
                    map_.ys.table[self.y][move_index],
                    map_.zs.table[self.z][move_index],
                    move,
                )


@dataclass(slots=True, frozen=True)
class StateMap:
    xs: MoveTable
    ys: MoveTable
    zs: MoveTable

    def create_state_from_cube(self, cube: Cube) -> State:
        return State(self.xs.getter(cube), self.ys.getter(cube), self.zs.getter(cube))


@dataclass(slots=True)
class Phase:
    pruning_table_1: PruningTable
    pruning_table_2: PruningTable
    group: Group
    state_map: StateMap = field(init=False)

    def __post_init__(self) -> None:
        self.pruning_table_1.load()
        self.pruning_table_2.load()
        self.state_map = StateMap(
            self.pruning_table_1.move_table_1,
            self.pruning_table_1.move_table_2,
            self.pruning_table_2.move_table_2,
        )

    # Warning: pruning_table_1 and pruning_table_2 MUST have the same move_table_1
    def compute_heuristic(self, state: State) -> int:
        a = self.pruning_table_1.table[state.x][state.y]
        b = self.pruning_table_2.table[state.x][state.z]

        if a > b:
            return a
        else:
            return b

    def __search(self, path: deque[State], g: int, bound: int) -> int | float:
        current_state = path[-1]
        h = self.compute_heuristic(current_state)
        f = g + h

        if f > bound:
            return f
        elif current_state.is_goal():
            return 0

        min_ = float("+inf")
        successors = list(current_state.successors(self.state_map, self.group))
        successors.sort(
            key=lambda successor: self.compute_heuristic(successor) + g + 1,
        )
        # for successor in current_state.successors(self.state_map, self.group):
        for successor in successors:
            path.append(successor)

            t = self.__search(path, g + 1, bound)
            if t == 0:
                return 0
            elif t < min_:
                min_ = t

            path.pop()

        return min_

    def run(self, cube: Cube, bound: int | None = None) -> Sequence:
        path: deque[State] = deque()
        state = self.state_map.create_state_from_cube(cube)

        if bound is None:
            bound = self.compute_heuristic(state)

        path.append(state)

        while 1:
            # print(bound)
            t = self.__search(path, 0, bound)  # type: ignore

            if t == float("+inf"):
                raise NoSolutionError("This cube has no solution.")
            elif t == 0:
                return [state.move for state in path if state.move is not None]
            else:
                bound = t  # type: ignore

        return []


class Solver:
    def __init__(self, cube: Cube, report: Report) -> None:
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

        corner_cubies_perm_exact_UD_slice_pruning = PruningTable(
            "corner_cubies_permutation_exact_UD_slice_pruning.pickle",
            exact_UD_slice_perm_move_table,
            corners_perm_move_table,
            group=G1,
        )

        edges_perm_pruning = PruningTable(
            "edges_permutation.pickle",
            exact_UD_slice_perm_move_table,
            not_UD_slice_perm_move_table,
            group=G1,
        )

        self.phase_1 = Phase(cubies_ori_pruning, edges_ori_UD_slice_perm_pruning, G0)
        self.phase_2 = Phase(
            corner_cubies_perm_exact_UD_slice_pruning, edges_perm_pruning, G1
        )
        self.cube = cube
        self.report = report

    @ReportManager.time
    @ReportManager.as_result(len)
    def run(self) -> Sequence:
        sequence_to_G1 = self.phase_1.run(self.cube)
        # print(sequence_to_G1)

        self.cube.apply_sequence(sequence_to_G1)
        sequence_to_solved = self.phase_2.run(self.cube)
        # print(sequence_to_solved)

        return sequence_to_G1 + sequence_to_solved
