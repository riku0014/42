"""カスタム例外。"""


class MazeError(Exception):
    """迷路関連例外の基底クラス。"""


class ConfigError(MazeError):
    """設定ファイルの読み込み・検証エラー。"""


class GenerationError(MazeError):
    """迷路生成エラー。"""


class ExportError(MazeError):
    """出力ファイル書き込みエラー。"""
