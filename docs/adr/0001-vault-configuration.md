# ADR-0001: Vault 路径配置方式

## 状态
已接受

## 日期
2026-05-20

## 背景
技能运行时需要知道目标 Obsidian vault 的路径。需要选择一种配置方式。

## 决策
使用项目根目录下的 `config.json` 文件。

```json
{
  "vault_path": "D:\\iCloudDrive\\iCloud~md~obsidian\\chardaway",
  "output_folder": "认知地图"
}
```

## 理由
- 显式、一目了然，不需要额外工具即可编辑
- 可被 git 追踪（但包含本地路径，各环境可能不同）
- Python 标准库 `json` 零依赖即可解析
- 比环境变量和自动检测更可靠

## 备选方案
- **环境变量**: 跨平台设置方式不统一，不易发现
- **每次询问**: 打断工作流，体验差
- **自动检测**: 用户可能有多个 vault，不可靠

## 影响
- `src/config.py` 负责加载和验证
- 不同环境可能需要不同的 config.json（可加入 .gitignore 的本地覆盖）
