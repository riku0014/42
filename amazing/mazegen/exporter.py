"""subject 仕様の出力ファイル生成。"""

from pathlib import Path

from .exceptions import ExportError
from .maze import Maze
from .solver import SolveResult


def maze_to_output_string(maze: Maze, solved: SolveResult) -> str:
    """迷路を subject 指定の文字列形式へ変換する。"""
    lines: list[str] = []

    for y in range(maze.height):
        row = "".join(
            format(maze.get_cell(x, y).walls, "X")
            for x in range(maze.width)
        )
        lines.append(row)

    lines.append("")
    lines.append(f"{maze.entry[0]},{maze.entry[1]}")
    lines.append(f"{maze.exit[0]},{maze.exit[1]}")
    lines.append(solved.path_directions)

    return "\n".join(lines) + "\n"


def export_maze(path: str, maze: Maze, solved: SolveResult) -> None:
    """迷路をファイルへ書き出す。"""
    output = maze_to_output_string(maze, solved)
    try:
        Path(path).write_text(output, encoding="utf-8")
    except OSError as exc:
        raise ExportError(f"出力ファイルの書き込みに失敗しました: {path}") from exc
