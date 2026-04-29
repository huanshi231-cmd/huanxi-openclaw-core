---
name: neirong-context-curator
description: |
  neirong记忆策展元技能。让neirong的记忆轻盈且精准，高价值信息自动晋升。
  核心职责：记忆分层管理、上下文优化控制、记忆蒸馏与晋升。
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
metadata:
  author: neirong
  version: '1.0.0'
---

# neirong-context-curator

记忆策展元技能。让neirong的记忆轻盈且精准，高价值信息自动晋升。

## 核心职责

- 记忆分层管理
- 上下文优化控制
- 记忆蒸馏与晋升

## 记忆分层

| 类型 | 位置 | 规则 |
|------|------|------|
| 短期记忆 | memory/YYYY-MM-DD.md | 每日对话原始记录 |
| 长期记忆 | MEMORY.md | 精华提炼，偏好/决策/教训 |
| 经验教训 | memory/feedback.md | 施欢的行为纠错 |
| 知识库 | knowledge/*.md | 格式模板/创作公式 |

## 记忆蒸馏规则

每天23:59收口时执行：
1. 扫描当日memory/YYYY-MM-DD.md
2. 提取高价值信息：施欢偏好、纠错、新决策
3. 写入MEMORY.md对应章节
4. 清理过时的短期记忆

## 上下文控制

- 每次写作任务：只加载SOUL.md + USER.md + MEMORY.md
- 施欢问历史 → 查MEMORY.md，不重复加载所有文件
- 避免每次都从头读所有文件

## 记忆晋升通道

feedback.md高频纠错 → 固化到SOUL.md或AGENTS.md

## 禁止事项

- 不把所有文件都塞进上下文
- 不重复加载相同内容
- 不过度依赖短期记忆
