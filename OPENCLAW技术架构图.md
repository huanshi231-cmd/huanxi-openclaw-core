# OpenClaw 技术架构图

> 版本：v1.0 | 日期：2026-04-23 | 系统：OpenClaw 2026.4.15

---

## 一、系统全貌

```
                        ┌─────────────────────────────┐
                        │       欢喜（用户）            │
                        │   Telegram: 8693424714       │
                        │   飞书群: oc_6c409c73f...    │
                        └──────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │      多路消息通道（复用同一账号） │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          │
 ┌──────────────┐          ┌──────────────┐                 │
 │  OpenClaw    │          │   Hermes     │                 │
 │  (主系统)     │          │  (辅助系统)   │                 │
 │              │          │              │                 │
 │ pid: 19564  │          │ pid: 24283   │                 │
 │ 12 Agents   │          │ Python venv  │                 │
 │ Port: 18789 │          │ Port: ?       │                 │
 └──────┬───────┘          └──────┬───────┘                 │
        │                         │                         │
        │ OpenClaw Gateway        │ Hermes Gateway          │
        │ ws://127.0.0.1:18789    │ 独立进程                │
        └────────────┬────────────┴─────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │    共享消息通道        │
          │  Telegram (同一 Bot)  │
          │  飞书 (同一 App)     │
          └──────────────────────┘
```

---

## 二、OpenClaw 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenClaw Gateway                            │
│                    ws://127.0.0.1:18789                        │
│                      Process: 19564                             │
│                   Version: 2026.4.15                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ session / tool call
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Channels │   │  Agents  │   │  Skills  │
        │          │   │          │   │          │
        │ telegram │   │  12个    │   │ workspace│
        │ feishu   │   │ 独立进程 │   │   +      │
        │          │   │          │   │ 全局     │
        └──────────┘   └──────────┘   └──────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Tools   │   │ Plugins   │   │ Sessions  │
        │          │   │           │   │           │
        │ exec     │   │ feishu    │   │ 134个     │
        │ read     │   │ mem9      │   │ 会话      │
        │ write    │   │ wecom     │   │           │
        │ message  │   │ dingtalk  │   │           │
        │ browser  │   │ volcengine│   │           │
        │ ...      │   │ ...       │   │           │
        └──────────┘   └──────────┘   └──────────┘
```

---

## 三、Agent 体系（12个分身）

```
太阳 (main)  ←────────── 本机 MacBook 核心协调层
  │
  ├── neirong          ~/.openclaw/workspace-neirong/
  ├── linggangshenghuo ~/.openclaw/workspace-linggangshenghuo/
  ├── liaoyuyewu       ~/.openclaw/workspace-liaoyuyewu/
  ├── memory           ~/.openclaw/workspace-memory/
  ├── system           ~/.openclaw/workspace-system/
  ├── xinmeiyunying    ~/.openclaw/workspace-xinmeiyunying/
  ├── shejiguan        ~/.openclaw/workspace-shejiguan/
  ├── kechengcehua     ~/.openclaw/workspace-kechengcehua/
  ├── peixun           ~/.openclaw/workspace-peixun/
  ├── funeng           ~/.openclaw/workspace-funeng/
  └── fuwu             ~/.openclaw/workspace-fuwu/
```

---

## 四、Workspace 目录结构

```
~/.openclaw/
├── openclaw.json              ← 核心配置文件
├── config.json                ← 次要配置
├── agents/                    ← Agent 权限配置
│   └── permissions
├── plugins/                   ← 插件目录
│   ├── feishu/
│   ├── mem9/
│   ├── wecom/
│   └── dingtalk/
├── skills/                    ← 全局 Skills (ClawHub)
│   ├── tarot/
│   ├── wechat-public-auto/
│   └── ...
├── workspace-main/           ← 太阳 (main) 的工作空间
│   ├── AGENTS.md             ← 工作规范
│   ├── SOUL.md               ← 性格定义
│   ├── MEMORY.md             ← 长期记忆
│   ├── HEARTBEAT.md          ← 心跳巡检
│   ├── skills/                ← 专属 Skills
│   │   ├── proactive-agent/
│   │   └── mem9-ai/
│   └── scripts_lib/           ← 本地脚本库
├── workspace-neirong/         ← 内容分身工作空间
├── workspace-*/               ← 其他分身工作空间
├── extensions/                ← 第三方扩展
│   ├── openclaw-lark/        ← 飞书插件
│   └── wecom/                ← 企业微信插件
├── cron/
│   └── jobs.json             ← 定时任务配置
├── sessions/                  ← 会话存储
├── logs/                     ← 日志
│   ├── config-audit.jsonl
│   └── config-health.json
├── media/                    ← 媒体文件
└── backups/                  ← 配置备份
```

---

## 五、OpenClaw 核心进程

```
openclaw-gateway (pid: 19564)
├── WebSocket Server: 127.0.0.1:18789
├── HTTP Server: Dashboard UI
├── Channel Adapters:
│   ├── Telegram Adapter (Bot)
│   └── Feishu Adapter (App: wx5d5a624cfde49bd3)
├── Tool Executor
│   ├── exec (Shell命令)
│   ├── read/write (文件系统)
│   ├── message (跨渠道消息)
│   ├── browser (Playwright)
│   └── ...
├── Plugin Host
│   ├── mem9 (记忆插件)
│   ├── feishu (飞书插件)
│   └── ...
└── Session Manager
    └── 134 active sessions
```

---

## 六、工具链（Tools）

| 工具 | 类型 | 用途 |
|------|------|------|
| exec | Shell | 执行命令、脚本 |
| read/write | 文件系统 | 读写文件 |
| message | 消息 | 跨渠道发送消息 |
| browser | 浏览器 | 网页自动化 |
| pdf | 文档 | PDF 分析 |
| image | 图片 | 图片分析 |
| web_search | 搜索 | 网页搜索 |
| web_fetch | 抓取 | 获取网页内容 |
| feishu_doc | 飞书文档 | 读写飞书云文档 |
| feishu_bitable | 飞书多维表格 | 管理多维表格 |
| feishu_task | 飞书任务 | 管理任务清单 |

---

## 七、Plugins 体系

```
Plugins (allowlist 模式)
├── openclaw-lark     ← 飞书插件
├── feishu            ← 飞书通道
├── wecom             ← 企业微信
├── mem9             ← 长期记忆 (slot: memory)
├── dingtalk         ← 钉钉
├── volcengine       ← 火山引擎
├── moonshot         ← 月之暗面
├── deepseek         ← DeepSeek
├── google           ← Google
├── qwen             ← 通义千问
├── ollama           ← 本地模型
├── browser          ← 浏览器自动化
└── relay            ← Relay 通道
```

---

## 八、消息流转（当前状态）

```
飞书群 oc_6c409c73f6d1bc540d0e54d472ea6bf2
  │
  ├── 欢喜 ──发消息──▶ 太阳（OpenClaw main）
  │                      │
  │                      ├── 太阳直接处理
  │                      └── 委派给分身
  │                            │
  │                            └── neirong ──结果──▶ 飞书群
  │
  └── 小月亮 ──发消息──▶ 腾讯云 OpenClaw（独立实例）
                            │
                            └── 公众号推送（固定IP出口）
```

---

## 九、关键配置文件

| 文件 | 作用 |
|------|------|
| `~/.openclaw/openclaw.json` | 核心配置：agents, plugins, tools, channels |
| `~/.openclaw/config.json` | 次要配置 |
| `~/.openclaw/agent-permissions-generated.json` | Agent权限配置 |
| `~/.openclaw/exec-approvals.json` | exec安全策略 |
| `~/.openclaw/cron/jobs.json` | 定时任务 |
| `~/.openclaw/workspace-*/AGENTS.md` | 各分身工作规范 |

---

## 十、环境变量

| 变量 | 值 | 用途 |
|------|-----|------|
| WECHAT_APPID | wx5d5a624cfde49bd3 | 微信公众号 |
| WECHAT_APPSECRET | 已配置 | 微信公众号密钥 |
| OPENCLAW_VERSION | 2026.4.15 | 系统版本 |

---

*OpenClaw 技术架构 v1.0 · 太阳 · 2026-04-23*
