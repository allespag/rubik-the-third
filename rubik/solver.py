from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Generator

from rubik.cube import Cube
from rubik.move import G0, Group, Move, Sequence
from rubik.move_table import MoveTable
from rubik.pruning_table import (
    PruningTable,
    cubies_ori_pruning,
    edges_ori_UD_slice_perm_pruning,
)


# L'idée c'est de pouvoir trouver les successors à l'aide des MoveTable.
# Exemple:
#   x' = mt_1[state.x][move]
#   y' = mt_2[state.y][move]
#   z' = mt_3[state.z][move]
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
        for move_index, move in enumerate(group):
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


# @dataclass(slots=True)
# class Node:
#     state: State
#     g: int = 0
#     h: int = 0
#     parent: Node | None = None

#     @property
#     def f(self) -> int:
#         return self.g + self.h

#     def is_goal(self) -> bool:
#         return self.state.is_goal()

#     def successors(self) -> Generator[St]


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
            self.pruning_table_1.move_table_1,  # xs
            self.pruning_table_1.move_table_2,  # ys
            self.pruning_table_2.move_table_2,  # zs
        )

    # Warning: pruning_table_1 and pruning_table_2 MUST have the same move_table_1
    def compute_heuristic(self, state: State) -> int:
        return max(
            self.pruning_table_1.table[state.x][state.y],
            self.pruning_table_2.table[state.x][state.z],
        )

    def __search(
        self, path: deque[State], g: int, bound: int
    ) -> State | None | int | float:
        current_state = path[-1]
        h = self.compute_heuristic(current_state)
        f = g + h

        if f > bound:
            return f
        elif current_state.is_goal():
            return current_state

        min_ = float("+inf")
        for successor in current_state.successors(self.state_map, self.group):
            if not any(n == successor for n in path):
                path.append(successor)

                t = self.__search(path, g + 1, bound)
                if isinstance(t, State):
                    return current_state
                elif isinstance(t, (float, int)) and t < min_:
                    min_ = t
                path.pop()

        if min_ == float("+inf"):
            return None
        else:
            return min_

    def run(self, cube: Cube) -> None:
        path: deque[State] = deque()
        state = self.state_map.create_state_from_cube(cube)
        bound = self.compute_heuristic(state)

        path.append(state)
        while True:
            t = self.__search(path, 0, bound)

            # Found
            if isinstance(t, State) or t is None:
                for elem in path:
                    print(str(elem.move))

                return
            else:
                bound = t


class Solver:
    def __init__(self) -> None:
        self.phase_1 = Phase(cubies_ori_pruning, edges_ori_UD_slice_perm_pruning, G0)

    def run(self, cube: Cube) -> Sequence:
        self.phase_1.run(cube)
