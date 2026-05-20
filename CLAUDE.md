# CLAUDE.md

## 项目概述
认知地图 (Knowledge Map) —— Claude Code 与 Obsidian 交互的技能组。

三个技能：
1. **线性** — 垂直深挖因果链：`问题 → 原因 → 原因的原因 → ...`，逐层追问，每层独立 md + wikilink
2. **解构** — 星形逻辑拆解：`相关问题 ← 核心问题 → 相关问题`，从一篇笔记拆出多层结构
3. **拓展** — 轮辐式横向发散：以任意节点为核心，向外拓展一层相关问题

核心机制：操作 Obsidian vault 目录中的 md 文件，通过 `[[wikilink]]` 建立关系。

## 仓库
- 本地：`D:\KnowledgeMap`
- 远程：`https://github.com/chardaway/KnowledgeMap`
- 自动备份：每 30 分钟自动 commit + push（cron 任务，7 天后需续期）

## 技术栈
- 运行环境：Claude Code skill（Markdown + YAML frontmatter）
- 目标系统：Obsidian vault（本地文件系统，md 文件 + `[[wikilink]]`）
- 辅助脚本：Python（文件操作、链接解析等复杂逻辑）

## 目录约定
```
src/          # Python 辅助脚本
skills/       # Claude Code 技能定义（.md）
tests/        # 测试
docs/adr/     # 架构决策记录
```

## 编码约定
- 优先使用中文撰写文档和注释
- 代码命名使用英文
- 遵循所选用技术栈的社区惯例

## 分支策略
- `master` — 稳定分支，受保护（禁止 force push / 删除）
- `dev` — 开发分支，日常开发在此进行
- 功能分支从 `dev` 拉出，完成后 PR 合入 `dev`
- `dev` 稳定后 PR 合入 `master`

## 工作流
- 所有变更需经 git 追踪
- 自动备份在后台运行，手动提交也应频繁进行
- 提交前 pre-commit hooks 自动运行（trim whitespace, check YAML/JSON, detect private keys 等）
- 重大决策记录在 `docs/adr/` 中
