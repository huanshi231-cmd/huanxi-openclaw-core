---
name: neirong-quality-auditor
description: |
  neirong质量审计元技能。每次写作发布前必须通过质量门禁，审计输出可靠性和规则有效性。
  核心职责：写作发布前质量自检、cron任务执行结果审计、规则一致性检查。
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Exec
  - message
  - feishu_doc
metadata:
  author: neirong
  version: '1.0.0'
---

# neirong-quality-auditor

质量审计元技能。每次写作发布前必须通过质量门禁，审计输出可靠性和规则有效性。

## 核心职责

- 写作发布前质量自检
- cron任务执行结果审计
- 规则一致性检查

## 自检清单（每次发布前必须执行）

| 检查项 | 标准 | 不通过则 |
|--------|------|----------|
| 字数 | 口播≥300字，公众号≥800字 | 打回重写 |
| 五步结构 | 钩子→共鸣→炸弹→行动→背书 | 打回重写 |
| 飞书链接 | 已发给施欢 | 立即补发 |
| 归档 | 已写入memory | 立即归档 |
| 格式 | 无U53CC等码位字符 | 清洗后发布 |

## cron任务审计

每天08:00自动检查：
1. 昨天的01:00和05:00轮播任务是否success
2. 如有error，立即告警到飞书协作群
3. 记录到HEARTBEAT.md

## 执行时机

- 每次写作完成发布前
- 每天08:00定时审计
- 被施欢质疑质量时

## 告警机制

任务失败 → 立即发飞书通知施欢，附错误摘要
