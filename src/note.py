"""笔记的读取与写入（含 YAML frontmatter）。"""

import re
from datetime import datetime
from pathlib import Path

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def create_note(
    path: Path,
    title: str,
    tags: list[str],
    body: str,
    backlinks: list[str] | None = None,
) -> None:
    """创建一个带 frontmatter 和 wikilink 的 md 文件。

    参数:
        path: 目标文件路径
        title: 笔记标题（即 # 标题）
        tags: 标签列表（不含 #）
        body: 正文内容
        backlinks: 底部 wikilink 列表（纯文件名，不含 [[]] 包裹）
    """
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tags_yaml = "\n".join(f"  - {t}" for t in tags)

    lines = [
        "---",
        "tags:",
        tags_yaml,
        f"created: {now}",
        f"modified: {now}",
        "---",
        "",
        f"# {title}",
        "",
        body,
    ]

    if backlinks:
        links = " · ".join(f"[[{b}]]" for b in backlinks)
        lines.extend(["", "---", "", links])

    lines.append("")  # 末尾换行

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def read_frontmatter(path: Path) -> dict:
    """解析并返回笔记的 YAML frontmatter。

    返回空字典表示无 frontmatter 或解析失败。
    """
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}

    raw = m.group(1)
    result = {}
    current_key = None

    for line in raw.split("\n"):
        line = line.rstrip()
        if not line:
            continue

        # YAML 列表项: "  - value"
        if line.startswith("  - "):
            value = line[4:].strip()
            if current_key:
                if current_key not in result or result[current_key] is None:
                    result[current_key] = []
                elif not isinstance(result[current_key], list):
                    result[current_key] = [result[current_key]]
                result[current_key].append(value)
            continue

        # YAML 键值对: "key: value"
        if ": " in line:
            k, v = line.split(": ", 1)
            result[k.strip()] = v.strip()
            current_key = k.strip()
        elif line.endswith(":") and " " not in line:
            # 值为空的键: "tags:"
            current_key = line[:-1].strip()
            result[current_key] = None

    return result


def has_frontmatter(path: Path) -> bool:
    """检查文件是否有有效的 YAML frontmatter。"""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return bool(_FRONTMATTER_RE.match(text))
