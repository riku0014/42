"""ASCII 表示と簡単な対話 UI。"""

from .maze import Maze
from .solver import SolveResult, solve_shortest_path


class AsciiRenderer:
    """ターミナル用 ASCII レンダラ。"""

    RESET = "\033[0m"
    PALETTES: list[dict[str, str]] = [
        {
            "wall": "\033[97m",
            "entry": "\033[95m",
            "exit": "\033[91m",
            "path": "\033[96m",
            "forty_two": "\033[90m",
        },
        {
            "wall": "\033[92m",
            "entry": "\033[95m",
            "exit": "\033[91m",
            "path": "\033[94m",
            "forty_two": "\033[93m",
        },
        {
            "wall": "\033[93m",
            "entry": "\033[95m",
            "exit": "\033[91m",
            "path": "\033[92m",
            "forty_two": "\033[90m",
        },
    ]

    def __init__(self, maze: Maze, show_path: bool = False) -> None:
        """初期化。"""
        self.maze = maze
        self.show_path = show_path
        self.palette_idx = 0
        self.solved = solve_shortest_path(maze)

    def update_maze(self, maze: Maze) -> None:
        """迷路を更新する。"""
        self.maze = maze
        self.solved = solve_shortest_path(maze)

    def rotate_colors(self) -> None:
        """壁色セットを切り替える。"""
        self.palette_idx = (self.palette_idx + 1) % len(self.PALETTES)

    def _color(self, role: str, text: str) -> str:
        """色付き文字列を返す。"""
        color = self.PALETTES[self.palette_idx][role]
        return f"{color}{text}{self.RESET}"

    def render(self) -> str:
        """迷路全体を ASCII 文字列として返す。"""
        path_set = set(self.solved.path_coords)
        out: list[str] = []

        # 最上段
        top = "+"
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, 0)
            segment = "---" if cell.has_wall(1) else "   "
            top += self._color("wall", segment) + "+"
        out.append(top)

        for y in range(self.maze.height):
            middle = ""
            bottom = ""

            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)

                west_char = "|" if cell.has_wall(8) else " "
                middle += self._color("wall", west_char)

                char = " "
                role: str | None = None

                if (x, y) == self.maze.entry:
                    char = "E"
                    role = "entry"
                elif (x, y) == self.maze.exit:
                    char = "X"
                    role = "exit"
                elif cell.is_42:
                    char = "#"
                    role = "forty_two"
                elif self.show_path and (x, y) in path_set:
                    char = "."
                    role = "path"

                if role is None:
                    middle += f" {char} "
                else:
                    middle += self._color(role, f" {char} ")

                bottom += "+"
                south = "---" if cell.has_wall(4) else "   "
                bottom += self._color("wall", south)

            east_wall = "|" if self.maze.get_cell(self.maze.width - 1, y).has_wall(2) else " "
            middle += self._color("wall", east_wall)
            bottom += "+"
            out.append(middle)
            out.append(bottom)

        out.append("")
        out.append("1. 迷路を再生成")
        out.append("2. 最短経路の表示/非表示")
        out.append("3. 壁色を変更")
        out.append("4. 終了")
        return "\n".join(out)
