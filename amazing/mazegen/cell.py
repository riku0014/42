"""迷路セル。"""

from dataclasses import dataclass

from .constants import EAST, NORTH, SOUTH, WEST


@dataclass
class Cell:
    """1セル分の情報を持つクラス。

    Attributes:
        walls: 壁のビットマスク。閉じている壁が1。
        is_42: 42パターンに属する閉塞セルかどうか。
    """

    walls: int = NORTH | EAST | SOUTH | WEST
    is_42: bool = False

    def has_wall(self, direction: int) -> bool:
        """指定方向に壁があるか返す。"""
        return (self.walls & direction) != 0

    def close_wall(self, direction: int) -> None:
        """指定方向の壁を閉じる。"""
        self.walls |= direction

    def open_wall(self, direction: int) -> None:
        """指定方向の壁を開く。"""
        self.walls &= ~direction
