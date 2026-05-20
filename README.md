# 认知地图 (Knowledge Map)

Claude Code 与 Obsidian 交互的技能组。通过三种思维模式辅助构建知识图谱。

## 三个技能

| 技能 | 模式 | 拓扑 |
|------|------|------|
| **线性** | 垂直因果链深挖 | `Q → C1 → C2 → ...` |
| **解构** | 星形逻辑拆解 | `相关 ← 核心 → 相关` |
| **拓展** | 轮辐式横向发散 | `核心 → 相关×N` |

每个技能操作 Obsidian vault 中的 md 文件，通过 `[[wikilink]]` 建立关系。

## 快速开始

1. 编辑 `config.json` 设置 vault 路径和名称
2. 确保 Obsidian ≥ 1.12 已安装（CLI 优先模式）
3. 在 Claude Code 中使用：

```
/线性    为什么天空是蓝色的？
/解构    忠诚的悖论
/拓展    文明6时代之熵
```

## 目录结构

```
├── src/              # Python 工具（零外部依赖）
│   ├── cli.py        # Obsidian CLI 封装
│   ├── config.py     # 配置加载
│   ├── note.py       # 笔记读写
│   ├── naming.py     # 文件名处理
│   └── vault.py      # Vault 查询
├── skills/           # Claude Code 技能定义
│   ├── 线性/SKILL.md
│   ├── 解构/SKILL.md
│   └── 拓展/SKILL.md
├── tests/            # 单元测试和集成测试
├── docs/adr/         # 架构决策记录
├── config.json       # 项目配置
└── CLAUDE.md         # Claude 项目上下文
```

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 许可

MIT
