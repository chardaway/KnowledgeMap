# CLAUDE.md

## 项目概述
认知地图 (Knowledge Map) —— Claude Code 技能组项目。从零开始构建。

## 仓库
- 本地：`D:\KnowledgeMap`
- 远程：`https://github.com/chardaway/KnowledgeMap`
- 自动备份：每 30 分钟自动 commit + push（cron 任务，7 天后需续期）

## 技术栈
待定。

## 目录约定
待定。确定后在下方补充。

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
