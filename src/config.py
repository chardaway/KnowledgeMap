"""加载项目配置 (config.json)。"""

import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config.json"


def load_config(path: Path | None = None) -> dict:
    """加载并返回配置字典。

    如果 config.json 不存在则抛出 FileNotFoundError。
    """
    p = Path(path) if path else _CONFIG_PATH
    if not p.exists():
        raise FileNotFoundError(f"配置文件不存在: {p}")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def get_vault_path() -> Path:
    """返回 vault 根目录的 Path 对象。"""
    cfg = load_config()
    p = Path(cfg["vault_path"])
    if not p.exists():
        raise FileNotFoundError(f"Vault 目录不存在: {p}")
    return p


def get_output_folder() -> str:
    """返回输出文件夹名称（默认 '认知地图'）。"""
    cfg = load_config()
    return cfg.get("output_folder", "认知地图")


def resolve_output_dir() -> Path:
    """返回完整输出路径: vault_path / output_folder。"""
    return get_vault_path() / get_output_folder()
