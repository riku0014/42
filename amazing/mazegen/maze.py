"""迷路本体データ構造。"""

from dataclasses import dataclass, field

from .cell import Cell
from .constants import DIRS, OPPOSITE


@dataclass
class Maze:
    """迷路全体を表すクラス。"""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool
    seed: int | None = None
    cells: list[list[Cell]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """セルを初期化する。"""
        if not self.cells:
            self.cells = [
                [Cell() for _ in range(self.width)]
                for _ in range(self.height)
            ]

    def in_bounds(self, x: int, y: int) -> bool:
        """座標が迷路内か返す。"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        """指定座標のセルを返す。"""
        return self.cells[y][x]

    def neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        """隣接セルを direction 付きで返す。"""
        result: list[tuple[int, int, int]] = []
        for direction, (dx, dy) in DIRS.items():
            nx = x + dx
            ny = y + dy
            if self.in_bounds(nx, ny):
                result.append((nx, ny, direction))
        return result

    def open_between(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        """隣接2セル間の壁を開く。"""
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay

        direction: int | None = None
        for candidate, (cx, cy) in DIRS.items():
            if (dx, dy) == (cx, cy):
                direction = candidate
                break

        if direction is None:
            raise ValueError("隣接していないセルです")

        self.get_cell(ax, ay).open_wall(direction)
        self.get_cell(bx, by).open_wall(OPPOSITE[direction])

    def close_between(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        """隣接2セル間の壁を閉じる。"""
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay

        direction: int | None = None
        for candidate, (cx, cy) in DIRS.items():
            if (dx, dy) == (cx, cy):
                direction = candidate
                break

        if direction is None:
            raise ValueError("隣接していないセルです")

        self.get_cell(ax, ay).close_wall(direction)
        self.get_cell(bx, by).close_wall(OPPOSITE[direction])

    def can_move(self, x: int, y: int, nx: int, ny: int) -> bool:
        """隣接セルへ移動可能か返す。"""
        dx = nx - x
        dy = ny - y
        for direction, (cx, cy) in DIRS.items():
            if (dx, dy) == (cx, cy):
                return not self.get_cell(x, y).has_wall(direction)
        return False

    def validate_wall_coherence(self) -> bool:
        """隣接セル間の壁整合性を検査する。"""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                for nx, ny, direction in self.neighbors(x, y):
                    other = self.get_cell(nx, ny)
                    if cell.has_wall(direction) != other.has_wall(OPPOSITE[direction]):
                        return False
        return True
