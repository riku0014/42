#!/usr/bin/env python3
"""A-Maze-ing のメイン実行ファイル。"""

import sys

from mazegen.config import load_config
from mazegen.exceptions import ConfigError, ExportError, GenerationError, MazeError
from mazegen.exporter import export_maze
from mazegen.generator import MazeGenerator
from mazegen.renderer_ascii import AsciiRenderer
from mazegen.solver import solve_shortest_path


def _build_and_export(config_path: str) -> tuple[AsciiRenderer, MazeGenerator, str]:
    """設定を読み込み、迷路生成・出力・レンダラ初期化を行う。"""
    config = load_config(config_path)
    generator = MazeGenerator(config)
    maze = generator.generate()
    solved = solve_shortest_path(maze)
    export_maze(config.output_file, maze, solved)
    renderer = AsciiRenderer(maze, show_path=config.show_path)
    return renderer, generator, config.output_file


def main() -> int:
    """メイン処理。"""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    config_path = sys.argv[1]

    try:
        renderer, generator, output_file = _build_and_export(config_path)

        while True:
            print(renderer.render())
            print(f"\n出力ファイル: {output_file}")
            choice = input("選択 (1-4): ").strip()

            if choice == "1":
                maze = generator.generate()
                solved = solve_shortest_path(maze)
                export_maze(output_file, maze, solved)
                renderer.update_maze(maze)
            elif choice == "2":
                renderer.show_path = not renderer.show_path
            elif choice == "3":
                renderer.rotate_colors()
            elif choice == "4":
                print("終了します。")
                return 0
            else:
                print("1, 2, 3, 4 のいずれかを入力してください。")

    except (ConfigError, GenerationError, ExportError, MazeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n中断されました。", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
