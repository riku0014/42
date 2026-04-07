"""最短経路探索。"""

from collections import deque
from dataclasses import dataclass

from .constants import DIR_TO_CHAR
from .maze import Maze


@dataclass
class SolveResult:
    """最短経路探索結果。"""

    path_coords: list[tuple[int, int]]
    path_directions: str


def solve_shortest_path(maze: Maze) -> SolveResult:
    """BFS で入口から出口までの最短経路を求める。"""
    start = maze.entry
    goal = maze.exit

    queue: deque[tuple[int, int]] = deque([start])
    prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break

        for nx, ny, _ in maze.neighbors(x, y):
            if (nx, ny) in prev:
                continue
            if maze.get_cell(nx, ny).is_42:
                continue
            if not maze.can_move(x, y, nx, ny):
                continue
            prev[(nx, ny)] = (x, y)
            queue.append((nx, ny))

    if goal not in prev:
        raise ValueError("ENTRY から EXIT への経路が見つかりません")

    coords: list[tuple[int, int]] = []
    cur: tuple[int, int] | None = goal
    while cur is not None:
        coords.append(cur)
        cur = prev[cur]
    coords.reverse()

    directions: list[str] = []
    for idx in range(len(coords) - 1):
        x1, y1 = coords[idx]
        x2, y2 = coords[idx + 1]
        directions.append(DIR_TO_CHAR[(x2 - x1, y2 - y1)])

    return SolveResult(
        path_coords=coords,
        path_directions="".join(directions),
    )
