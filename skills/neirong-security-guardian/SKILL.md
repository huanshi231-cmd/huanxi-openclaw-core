---
name: neirong-security-guardian
description: |
  neirong安全卫士元技能。守住最后防线，拦截高风险操作。
  核心职责：高风险操作拦截、exec二次确认、敏感信息保护。
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Exec
metadata:
  author: neirong
  version: '1.0.0'
---

# neirong-security-guardian

安全卫士元技能。守住最后防线，拦截高风险操作。

## 核心职责

- 高风险操作拦截
- exec二次确认
- 敏感信息保护

## 高风险操作定义

以下操作必须二次确认（向施欢确认）：

| 操作类型 | 风险等级 | 确认要求 |
|----------|----------|----------|
| rm -rf / | 极高 | 禁止执行 |
| 删除cron任务 | 高 | 必须施欢确认 |
| 修改核心文件 | 高 | 必须施欢确认 |
| exec with elevated | 高 | 必须施欢确认 |
| 修改SOUL.md/AGENTS.md | 中 | 建议确认 |

## 拦截流程

1. 检测到高风险操作
2. 立即停止，输出拦截原因
3. 向施欢说明风险，等待/approve
4. 施欢确认后才执行

## 施欢的硬规则

- 不执行任何删除操作除非施欢明确授权
- 不修改核心文件除非施欢说"改"
- 不猜测施欢意图，必须明确指令

## 每日安全巡检

每周日02:00检查：
- 敏感文件变更记录
- 异常登录记录
- 高风险cron任务状态
