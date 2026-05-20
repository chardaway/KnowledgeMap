# ADR-0003: Obsidian CLI 集成

## 状态
已接受

## 日期
2026-05-20

## 背景

Obsidian 从 v1.12（2026-02）起内置了官方 CLI，提供 `obsidian create`、`obsidian read`、`obsidian append`、`obsidian search`、`obsidian links`、`obsidian backlinks` 等命令。用户系统已安装 Obsidian 1.12.7。

CLI 的优势：
- 自动处理索引更新
- 移动/重命名时自动更新 `[[wikilink]]`
- 官方维护，与 Obsidian 内部逻辑一致
- 可通过 `vault=<name>` 精确定位目标 vault

## 决策

采用 **CLI 优先、直接文件 I/O 回退** 的双路径策略：

1. 所有创建/读取/追加操作优先使用 `obsidian` CLI
2. 当 CLI 不可用时（例如 Obsidian 未运行），自动回退到 `src/note.py` 直接文件操作
3. 封装层统一放在 `src/cli.py`，对技能侧透明

## 理由

- CLI 能正确处理 Obsidian 的内部缓存和索引，避免直接文件操作可能导致的 Obsidian 数据不同步
- 回退机制确保在无头环境或 CI 中仍可工作
- 封装层对上层技能隐藏实现细节

## 影响

- `src/cli.py` 作为核心封装，提供 `create_map_note()`、`append_links()`、`read_map_note()` 等高层函数
- `config.json` 新增 `vault_name` 字段（用于 CLI 的 `vault=` 参数）
- 所有三个技能的 SKILL.md 通过 cli.py 操作 vault
