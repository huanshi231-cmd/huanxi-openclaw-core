# OpenClaw Skill 官方格式

## SKILL.md 必须结构

```yaml
---
name: skill-name
version: 1.0.0
description: "[功能] + Use when: [触发条件] + Key capabilities: [核心能力]"
---

# Title

## When to Use
[何时触发]

## 操作流程
1. 步骤一
2. 步骤二

## Examples（可选）
场景 → 动作 → 结果

## Troubleshooting（可选）
问题 → 原因 → 解决
```

## YAML Frontmatter 规范

| 字段 | 要求 | 示例 |
|------|------|------|
| name | 必须，kebab-case | `soul-md-restructure` |
| description | 必须，<1024字符 | `重构SOUL.md...` |
| version | 推荐，semver | `1.0.0` |

**description 公式**：
```
[我做什么]。Use when: [触发条件1]; [触发条件2]。Key capabilities: [核心能力列表]。
```

## 行数控制

| 文件 | 上限 |
|------|------|
| SKILL.md | <500 行 |
| 单个参考文件 | <200 行 |
| 总 skill 目录 | 尽量小 |

## 三层渐进式披露

1. **YAML frontmatter** — 永远加载，知道何时触发
2. **SKILL.md body** — 技能相关时加载
3. **references/** — 按需加载，不进 context
