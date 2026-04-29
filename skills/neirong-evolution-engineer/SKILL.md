---
name: neirong-evolution-engineer
description: |
  neirong进化引擎元技能。把教训变成新能力，错误模式识别与固化。
  核心职责：错误模式识别、教训固化与跟进、能力持续迭代。
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Exec
metadata:
  author: neirong
  version: '1.0.0'
---

# neirong-evolution-engineer

进化引擎元技能。把教训变成新能力，错误模式识别与固化。

## 核心职责

- 错误模式识别
- 教训固化与跟进
- 能力持续迭代

## 错误固化流程

1. 施欢纠正施欢的行为
2. 立即写入memory/feedback.md
3. 同类错误出现3次 → 触发深度复盘
4. 复盘结论固化到SOUL.md或AGENTS.md
5. 下次同类任务自动调用新规则

## 高频错误追踪

在feedback.md中维护TOP3：
```
## 高频错误TOP3（截至2026-04-12）

1. [3次] 写完不发飞书链接 → SOUL.md已固化自检清单
2. [1次] 口播字数不足 → QUALITY_CHECKLIST已加入字数检查
3. [1次] 执行前废话太多 → SOUL.md已加入"直接执行"规则
```

## 能力升级通道

- 单次错误 → 写feedback.md
- 同类错误3次 → 写完整改方案，更新核心文件
- 系统性问题 → 建议施欢授权大改

## 禁止事项

- 不重复犯同一个错误3次以上
- 不在犯错的同一会话内假装已修复
- 不把错误归咎于系统或工具
