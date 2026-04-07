"""迷路生成ロジック。"""

import random
from collections import deque

from .config import MazeConfig
from .exceptions import GenerationError
from .maze import Maze
from .solver import solve_shortest_path


class MazeGenerator:
    """再利用可能な迷路生成器。"""

    def __init__(self, config: MazeConfig) -> None:
        """設定から生成器を初期化する。"""
        self.config = config
        self.rng = random.Random(config.seed)

    def generate(self) -> Maze:
        """条件を満たす迷路を生成する。"""
        maze = Maze(
            width=self.config.width,
            height=self.config.height,
            entry=self.config.entry,
            exit=self.config.exit,
            perfect=self.config.perfect,
            seed=self.config.seed,
        )

        reserved = self._place_42_pattern(maze)
        self._generate_perfect_maze(maze, reserved)

        if not self._all_walkable_connected(maze):
            raise GenerationError("迷路が連結になっていません")

        if not self.config.perfect:
            self._add_extra_openings(maze, reserved)

        if self._has_forbidden_3x3_open_area(maze):
            raise GenerationError("3x3 の開放領域が存在します")

        if not maze.validate_wall_coherence():
            raise GenerationError("壁情報の整合性が壊れています")

        try:
            solve_shortest_path(maze)
        except ValueError as exc:
            raise GenerationError("ENTRY から EXIT に到達できません") from exc

        return maze

    def _generate_perfect_maze(
        self,
        maze: Maze,
        reserved: set[tuple[int, int]],
    ) -> None:
        """DFS バックトラッカーで perfect maze を生成する。"""
        walkable = [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if (x, y) not in reserved
        ]

        if maze.entry in reserved or maze.exit in reserved:
            raise GenerationError("42 パターンが ENTRY または EXIT と重なっています")

        if not walkable:
            raise GenerationError("歩行可能セルがありません")

        start = maze.entry
        visited: set[tuple[int, int]] = {start}
        stack: list[tuple[int, int]] = [start]

        while stack:
            x, y = stack[-1]
            candidates = [
                (nx, ny)
                for nx, ny, _ in maze.neighbors(x, y)
                if (nx, ny) not in reserved and (nx, ny) not in visited
            ]
            if not candidates:
                stack.pop()
                continue

            nx, ny = self.rng.choice(candidates)
            maze.open_between((x, y), (nx, ny))
            visited.add((nx, ny))
            stack.append((nx, ny))

        if len(visited) != len(walkable):
            raise GenerationError("DFS が全歩行可能セルに到達していません")

    def _place_42_pattern(self, maze: Maze) -> set[tuple[int, int]]:
        """閉じたセルで 42 パターンを置く。"""
        pattern = [
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        ]
        ph = len(pattern)
        pw = len(pattern[0])

        if maze.width < pw + 4 or maze.height < ph + 4:
            print("迷路が小さすぎるため '42' パターンは省略します。")
            return set()

        ox = (maze.width - pw) // 2
        oy = (maze.height - ph) // 2
        reserved: set[tuple[int, int]] = set()

        for py, row in enumerate(pattern):
            for px, char in enumerate(row):
                if char != "1":
                    continue
                x = ox + px
                y = oy + py
                if (x, y) in (maze.entry, maze.exit):
                    raise GenerationError("42 パターンが ENTRY または EXIT と重なっています")
                maze.get_cell(x, y).is_42 = True
                reserved.add((x, y))

        return reserved

    def _all_walkable_connected(self, maze: Maze) -> bool:
        """42 セル以外が全連結か調べる。"""
        blocked = {
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if maze.get_cell(x, y).is_42
        }

        walkable = [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if (x, y) not in blocked
        ]
        if not walkable:
            return False

        start = maze.entry
        seen: set[tuple[int, int]] = {start}
        queue: deque[tuple[int, int]] = deque([start])

        while queue:
            x, y = queue.popleft()
            for nx, ny, _ in maze.neighbors(x, y):
                if (nx, ny) in blocked or (nx, ny) in seen:
                    continue
                if not maze.can_move(x, y, nx, ny):
                    continue
                seen.add((nx, ny))
                queue.append((nx, ny))

        return len(seen) == len(walkable)

    def _add_extra_openings(
        self,
        maze: Maze,
        reserved: set[tuple[int, int]],
    ) -> None:
        """PERFECT=False 用に安全な範囲で少しだけ追加開通する。"""
        candidates: list[tuple[tuple[int, int], tuple[int, int]]] = []

        for y in range(maze.height):
            for x in range(maze.width):
                if (x, y) in reserved:
                    continue
                for nx, ny, _ in maze.neighbors(x, y):
                    if (nx, ny) in reserved:
                        continue
                    if (x, y) >= (nx, ny):
                        continue
                    if maze.can_move(x, y, nx, ny):
                        continue
                    candidates.append(((x, y), (nx, ny)))

        self.rng.shuffle(candidates)
        target = max(1, len(candidates) // 20)
        opened = 0

        for a, b in candidates:
            if opened >= target:
                break
            maze.open_between(a, b)
            if self._has_forbidden_3x3_open_area(maze):
                maze.close_between(a, b)
                continue
            opened += 1

    def _has_forbidden_3x3_open_area(self, maze: Maze) -> bool:
        """3x3 の完全開放領域があるか返す。"""
        for y in range(maze.height - 2):
            for x in range(maze.width - 2):
                coords = [
                    (x + dx, y + dy)
                    for dy in range(3)
                    for dx in range(3)
                ]
                if any(maze.get_cell(cx, cy).is_42 for cx, cy in coords):
                    continue
                if self._is_open_3x3_block(maze, x, y):
                    return True
        return False

    def _is_open_3x3_block(self, maze: Maze, x: int, y: int) -> bool:
        """3x3 ブロック内部が完全に開いているか返す。"""
        for dy in range(3):
            for dx in range(3):
                cx = x + dx
                cy = y + dy
                if dx < 2 and not maze.can_move(cx, cy, cx + 1, cy):
                    return False
                if dy < 2 and not maze.can_move(cx, cy, cx, cy + 1):
                    return False
        return True
