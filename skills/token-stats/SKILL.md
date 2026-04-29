---
name: token-stats
description: 五维Token统计工具。自动记录每次对话的input/output/cache tokens和费用，支持按日/周/月查询。欢喜说查token、花了多少、看统计时使用。
---

# Token 统计工具

> 基于 Claude Code cost-tracker.ts 五维Token模型设计

## 五维Token分类

| 维度 | 字段 | 说明 |
|------|------|------|
| 输入 | inputTokens | 用户输入的token |
| 输出 | outputTokens | 模型回复的token |
| 缓存读 | cacheReadTokens | 缓存命中（省钱） |
| 缓存写 | cacheWriteTokens | 缓存创建 |

## 使用方式

### 查统计（常用）

```
token today    # 查今天
token week     # 查本周
token month    # 查本月
token by-model # 按模型查看
```

### 手动记录对话

```
token add --input 5000 --output 3000 --cost 0.05 --model MiniMax-M2
```

## 数据存储

~/.openclaw/token-stats/usage.json（保留90天）

## 触发词

查token / 花了多少 / 看统计 / token统计
