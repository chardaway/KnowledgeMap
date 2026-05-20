"""Obsidian CLI 封装层。

优先使用官方 Obsidian CLI（v1.12+），失败时回退到直接文件 I/O。
"""

import json as _json
import shlex
import subprocess
from pathlib import Path

from .config import get_vault_path, get_output_folder


def _run(*args: str, vault: str | None = None) -> subprocess.CompletedProcess:
    """执行 obsidian CLI 命令，返回 CompletedProcess。

    vault 参数指定目标 vault 名称。
    """
    cmd = ["obsidian", *args]
    if vault:
        cmd.append(f"vault={vault}")

    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
    )


def cli_available() -> bool:
    """检查 obsidian CLI 是否可用。"""
    try:
        result = _run("version")
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


# ── 笔记操作 ────────────────────────────────────────────


def create_note(
    path: str,
    content: str,
    vault: str | None = None,
) -> bool:
    """通过 CLI 创建笔记。返回是否成功。"""
    result = _run("create", f"path={path}", f"content={content}", vault=vault)
    return result.returncode == 0


def read_note(path: str, vault: str | None = None) -> str | None:
    """通过 CLI 读取笔记内容。失败返回 None。"""
    result = _run("read", f"path={path}", vault=vault)
    if result.returncode == 0:
        return result.stdout
    return None


def append_note(path: str, content: str, vault: str | None = None) -> bool:
    """通过 CLI 在笔记末尾追加内容。返回是否成功。"""
    result = _run("append", f"path={path}", f"content={content}", vault=vault)
    return result.returncode == 0


# ── 查询操作 ────────────────────────────────────────────


def search(query: str, vault: str | None = None, limit: int | None = None) -> list[str]:
    """搜索 vault 返回匹配文件路径列表。"""
    args = ["search", f"query={query}", "format=json"]
    if limit:
        args.append(f"limit={limit}")
    result = _run(*args, vault=vault)
    if result.returncode == 0 and result.stdout.strip():
        try:
            data = _json.loads(result.stdout)
            return [item["path"] for item in data]
        except _json.JSONDecodeError:
            return []
    return []


def get_links(path: str, vault: str | None = None) -> list[str]:
    """获取指定笔记的出链列表。"""
    result = _run("links", f"path={path}", "format=json", vault=vault)
    if result.returncode == 0 and result.stdout.strip():
        try:
            return _json.loads(result.stdout)
        except _json.JSONDecodeError:
            return []
    return []


def get_backlinks(path: str, vault: str | None = None) -> list[str]:
    """获取指向指定笔记的反链列表。"""
    result = _run("backlinks", f"path={path}", "format=json", vault=vault)
    if result.returncode == 0 and result.stdout.strip():
        try:
            return _json.loads(result.stdout)
        except _json.JSONDecodeError:
            return []
    return []


# ── 元数据操作 ──────────────────────────────────────────


def get_tags(vault: str | None = None) -> list[str]:
    """获取 vault 中所有标签。"""
    result = _run("tags", "format=json", vault=vault)
    if result.returncode == 0 and result.stdout.strip():
        try:
            return _json.loads(result.stdout)
        except _json.JSONDecodeError:
            return []
    return []


def get_properties(path: str, vault: str | None = None) -> dict:
    """获取笔记的 frontmatter 属性。"""
    result = _run("properties", f"path={path}", "format=json", vault=vault)
    if result.returncode == 0 and result.stdout.strip():
        try:
            return _json.loads(result.stdout)
        except _json.JSONDecodeError:
            return {}
    return {}


# ── 高层操作（供技能使用）───────────────────────────────


def create_map_note(
    skill: str,
    title: str,
    body: str,
    backlinks: list[str] | None = None,
    vault: str | None = None,
    use_cli: bool = True,
) -> str:
    """创建一个认知地图笔记。

    参数:
        skill: 技能名（线性/解构/拓展），决定子目录
        title: 笔记标题
        body: 正文内容
        backlinks: wikilink 链接的文件名列表
        vault: vault 名称
        use_cli: 是否优先使用 CLI

    返回: 创建的文件相对路径（相对于 vault 根）
    """
    from .naming import sanitize_filename

    output = get_output_folder()
    safe_title = sanitize_filename(title)
    rel_path = f"{output}/{skill}/{safe_title}.md"

    lines = [f"# {title}", "", body]
    if backlinks:
        links = " · ".join(f"[[{b}]]" for b in backlinks)
        lines.extend(["", "---", "", links])
    content = "\n".join(lines)

    if use_cli and cli_available():
        ok = create_note(rel_path, content, vault=vault)
        if ok:
            return rel_path

    # 回退：直接文件 I/O
    vault_dir = get_vault_path()
    full_path = vault_dir / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content + "\n", encoding="utf-8")
    return rel_path


def append_links(
    path: str,
    links: list[str],
    vault: str | None = None,
    use_cli: bool = True,
) -> bool:
    """在笔记底部追加 wikilink。

    参数:
        path: 文件相对路径（相对于 vault 根）
        links: 要追加的 wikilink 文件名列表
        vault: vault 名称
        use_cli: 是否优先使用 CLI

    返回: 是否成功
    """
    link_str = "[[{}]]".format("]] · [[".join(links))
    append_content = f"\n{link_str}"

    if use_cli and cli_available():
        ok = append_note(path, append_content, vault=vault)
        if ok:
            return True

    # 回退：直接文件 I/O
    vault_dir = get_vault_path()
    full_path = vault_dir / path
    if full_path.exists():
        current = full_path.read_text(encoding="utf-8")
        full_path.write_text(current.rstrip() + append_content + "\n", encoding="utf-8")
        return True
    return False


def read_map_note(
    path: str,
    vault: str | None = None,
    use_cli: bool = True,
) -> str | None:
    """读取笔记内容。

    返回: 笔记全文，失败返回 None
    """
    if use_cli and cli_available():
        return read_note(path, vault=vault)

    vault_dir = get_vault_path()
    full_path = vault_dir / path
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    return None
