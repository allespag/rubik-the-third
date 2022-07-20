from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Generator

from rubik.cube import Cube
from rubik.move import G0, G1, Group, Move, Sequence, sequence_to_readable
from rubik.move_table import MoveTable
from rubik.pruning_table import (
    PruningTable,
    corner_cubies_perm_exact_UD_slice_pruning,
    cubies_ori_pruning,
    edges_ori_UD_slice_perm_pruning,
    edges_perm_pruning,
)


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
            check = self.move is None or (
                self.move.get_reverse() != move and not self.move.is_opposite(move)
            )
            if check:
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
        return max(
            self.pruning_table_1.table[state.x][state.y],
            self.pruning_table_2.table[state.x][state.z],
        )

    def __search(self, path: deque[State], g: int, bound: int) -> State | None | int:
        current_state = path[-1]
        path_set = set(path)
        h = self.compute_heuristic(current_state)
        f = g + h

        if f > bound:
            return f
        elif current_state.is_goal():
            return current_state

        min_ = float("+inf")
        for successor in current_state.successors(self.state_map, self.group):
            if successor not in path_set:
                path.append(successor)
                path_set.add(successor)

                t = self.__search(path, g + 1, bound)
                if isinstance(t, State):
                    return current_state
                elif isinstance(t, (float, int)) and t < min_:
                    min_ = t
                path.pop()
                path_set.remove(successor)

        if min_ == float("+inf"):
            return None
        else:
            return min_  # type: ignore

    def run(self, cube: Cube) -> Sequence:
        path: deque[State] = deque()
        state = self.state_map.create_state_from_cube(cube)

        bound = self.compute_heuristic(state)

        path.append(state)
        while True:
            print(bound)
            t = self.__search(path, 0, bound)

            if t is None:
                raise NoSolutionError("This cube has no solution.")
            elif isinstance(t, State):
                return [state.move for state in path if state.move is not None]
            else:
                bound = t


# La phase 2 est lente de ouf, peut être que les moves map sont pas ouf
class Solver:
    def __init__(self) -> None:
        self.phase_1 = Phase(cubies_ori_pruning, edges_ori_UD_slice_perm_pruning, G0)
        self.phase_2 = Phase(
            corner_cubies_perm_exact_UD_slice_pruning, edges_perm_pruning, G1
        )

    def run(self, cube: Cube) -> Sequence:
        sequence_to_G1 = self.phase_1.run(cube)
        print(sequence_to_readable(sequence_to_G1))

        cube.apply_sequence(sequence_to_G1)
        sequence_to_solved = self.phase_2.run(cube)

        return sequence_to_G1 + sequence_to_solved
