# memory_reference.md · 外部系统指针

> 类型：reference | 更新：2026-04-28 | 维护：太阳
> 存放：GitHub仓库路径、工作区路径、外部系统地址、重要文件位置

---

## 本地路径

| 名称 | 路径 |
|------|------|
| OpenClaw配置 | `/Users/huanxi/.openclaw/openclaw.json` |
| 太阳工作区 | `/Users/huanxi/.openclaw/workspace-taiyang/` |
| 主工作区（规则文档）| `/Users/huanxi/.openclaw/workspace-main/` |
| GitHub本地仓库 | `/Users/huanxi/.openclaw/workspace-main/repos/huanxi-openclaw-core/` |
| 网关plist | `/Users/huanxi/Library/LaunchAgents/ai.openclaw.gateway.plist` |

## GitHub仓库

- **仓库名**：huanxi-openclaw-core
- **用途**：7个核心分身的所有MD文档备份，GitHub可见才算完成

## 外部服务

- **飞书**：主要协作平台，消息推送目标
  - 卡片消息有HTTP 400问题，改用普通文本消息
  - Cron任务必须配置defaultTarget（chatId或user:openId）

## 网关操作命令

```bash
# 停网关（改配置前必须先停）
launchctl bootout gui/501/ai.openclaw.gateway

# 启网关
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 查网关状态
launchctl list | grep openclaw
```

## 重要文件清单

| 文件 | 用途 |
|------|------|
| `BOOTSTRAP.md` | 分身启动自检清单 |
| `AGENTS.md` | 太阳执行规范 |
| `MEMORY.md` | 记忆索引 |
| `错误库.md` | 历史错误，启动必读 |
| `NATURAL_LANGUAGE_DECODER.md` | 口语解码表 |
| `复盘模板.md` | 任务复盘格式 |
| `UPLOAD_BOUNDARY.md` | 敏感数据上传边界 |
| `HEARTBEAT.md` | 心跳巡检规则 |
