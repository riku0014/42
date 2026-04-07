"""設定ファイルの読み込みと検証。"""

from dataclasses import dataclass
from pathlib import Path

from .exceptions import ConfigError


@dataclass(frozen=True)
class MazeConfig:
    """迷路生成設定。"""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    show_path: bool = False


def _parse_bool(value: str) -> bool:
    """真偽値文字列を bool に変換する。"""
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ConfigError(f"不正な真偽値です: {value}")


def _parse_point(value: str, key: str) -> tuple[int, int]:
    """x,y 形式の座標をパースする。"""
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} は x,y 形式で指定してください")
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError as exc:
        raise ConfigError(f"{key} は整数座標で指定してください") from exc
    return (x, y)


def load_config(path: str) -> MazeConfig:
    """設定ファイルを読み込んで検証済み MazeConfig を返す。"""
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigError(f"設定ファイルが見つかりません: {path}")

    raw: dict[str, str] = {}

    try:
        lines = cfg_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ConfigError(f"設定ファイルの読み込みに失敗しました: {path}") from exc

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise ConfigError(f"{lineno} 行目: KEY=VALUE 形式ではありません")
        key, value = stripped.split("=", 1)
        key = key.strip().upper()
        value = value.strip()
        if not key:
            raise ConfigError(f"{lineno} 行目: キーが空です")
        raw[key] = value

    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    missing = [key for key in mandatory if key not in raw]
    if missing:
        raise ConfigError(f"必須キー不足: {', '.join(missing)}")

    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])
    except ValueError as exc:
        raise ConfigError("WIDTH と HEIGHT は整数である必要があります") from exc

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH と HEIGHT は正の整数である必要があります")

    entry = _parse_point(raw["ENTRY"], "ENTRY")
    exit_point = _parse_point(raw["EXIT"], "EXIT")

    if entry == exit_point:
        raise ConfigError("ENTRY と EXIT は異なる必要があります")

    ex, ey = entry
    xx, xy = exit_point
    if not (0 <= ex < width and 0 <= ey < height):
        raise ConfigError("ENTRY が迷路範囲外です")
    if not (0 <= xx < width and 0 <= xy < height):
        raise ConfigError("EXIT が迷路範囲外です")

    perfect = _parse_bool(raw["PERFECT"])

    seed: int | None = None
    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError as exc:
            raise ConfigError("SEED は整数である必要があります") from exc

    show_path = False
    if "SHOW_PATH" in raw:
        show_path = _parse_bool(raw["SHOW_PATH"])

    output_file = raw["OUTPUT_FILE"].strip()
    if not output_file:
        raise ConfigError("OUTPUT_FILE は空にできません")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_point,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        show_path=show_path,
    )
