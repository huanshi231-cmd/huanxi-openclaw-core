# AAAK 压缩记忆格式（可选）

来源：MemPalace AAAK 方言规范

## 适用场景

将长记忆压缩为 AAAK 格式，存入 MemPalace 记忆宫殿。

## AAAK 结构

```
SESSION:YYYY-MM-DD|动作.对象|ALC.req:来源|评级
```

## 字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| SESSION | 会话日期 | `2026-04-26` |
| 动作.对象 | 做了什么 | `restructured.soul-md` |
| ALC.req | 来源请求 | `agent.soul-best-practice` |
| 评级 | 重要度 | `★★★☆☆` |

## 示例

```
SESSION:2026-04-26|restructured.soul-md|ALC.req:user.req|★★★★
SESSION:2026-04-26|created.skill-folder|built.soul-md-skill|★★★
```

## 用途

- 存入 MemPalace 后可跨 session 检索
- 每日自动蒸馏时用于快速回顾
- 比自然语言更紧凑（节省 token）

## 何时使用

- 完成重要任务后存入记忆宫殿
- 发现关键教训时记录
- 用户纠正偏好时存入
