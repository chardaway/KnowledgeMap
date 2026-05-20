"""文件名清理与冲突解决。"""

import re
from pathlib import Path

# Windows 文件名非法字符
_ILLEGAL = re.compile(r'[\\/:*?"<>|]')

# 最大文件名长度（不含扩展名）
_MAX_LEN = 100


def sanitize_filename(title: str) -> str:
    """去除 Windows 非法字符并截断过长文件名。"""
    name = _ILLEGAL.sub("", title).strip()
    if len(name) > _MAX_LEN:
        name = name[:_MAX_LEN]
    return name


def unique_path(directory: Path, title: str) -> Path:
    """返回不冲突的文件路径。

    如果 directory/title.md 已存在，依次尝试 title-2.md, title-3.md...
    """
    name = sanitize_filename(title)
    candidate = directory / f"{name}.md"
    if not candidate.exists():
        return candidate

    i = 2
    while True:
        candidate = directory / f"{name}-{i}.md"
        if not candidate.exists():
            return candidate
        i += 1
