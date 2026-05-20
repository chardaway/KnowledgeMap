"""Obsidian vault 查询工具。"""

from pathlib import Path


def find_note(vault_path: Path, name: str) -> Path | None:
    """在 vault 中按文件名查找笔记（不含 .md 扩展名）。

    如果 name 是纯文件名，则搜索整个 vault。
    如果 name 含有路径分隔符，则在对应子目录查找。
    """
    if "/" in name or "\\" in name:
        parts = Path(name).parts
        target = vault_path.joinpath(*parts)
        candidate = target.with_suffix(".md")
        if candidate.exists():
            return candidate
        # 也可能 name 是不含 .md 的完整路径
        if target.exists() and target.is_file():
            return target
        return None

    # 搜索整个 vault
    for md in vault_path.rglob(f"{name}.md"):
        # 跳过 .obsidian 目录和 _附件 目录
        if ".obsidian" in md.parts:
            continue
        return md
    return None


def list_notes(vault_path: Path, folder: str | None = None) -> list[Path]:
    """列出 vault 中的 .md 文件，可选按文件夹过滤。"""
    search_dir = vault_path / folder if folder else vault_path
    if not search_dir.exists():
        return []

    notes = []
    for md in search_dir.rglob("*.md"):
        if ".obsidian" in md.parts:
            continue
        notes.append(md)
    return sorted(notes)


def resolve_wikilink(vault_path: Path, wikilink_name: str) -> Path | None:
    """将 [[wikilink名称]] 解析为实际文件路径。

    支持:
    - [[笔记名]]
    - [[笔记名|别名]]
    - [[笔记名#标题]]
    - [[笔记名#^block-id]]
    """
    # 去除别名、标题锚点、块引用
    name = wikilink_name
    if "|" in name:
        name = name.split("|")[0]
    if "#" in name:
        name = name.split("#")[0]
    name = name.strip()
    return find_note(vault_path, name)
