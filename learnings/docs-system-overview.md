# 文档体系全景图

> 太阳的整个记忆/知识/规则体系的结构、分类和运作方式

---

## 一、整体架构

我的文档体系分为 4 大类：

```
workspace-main/
├── *.md                    # T0 核心文件（7个）
├── memory/                 # 记忆仓库
├── .learnings/             # 踩坑经验沉淀（103个）
├── docs/                   # 参考文档
└── learnings/              # 可分享的教程
```

---

## 二、T0 核心文件（每次启动必读）

| 文件 | 我是谁 | 管什么 |
|------|--------|--------|
| **SOUL.md** | 我的灵魂 | 性格、禁止语、说话方式、情绪处理 |
| **IDENTITY.md** | 我的身份 | 角色定位、多Agent调度表 |
| **USER.md** | 欢喜的档案 | 偏好、习惯、禁忌 |
| **AGENTS.md** | 工作规范 | 任务闭环、晨报日报、熔断机制 |
| **TOOLS.md** | 工具箱 | 我能用的工具、能力边界 |
| **HEARTBEAT.md** | 触发式心跳 | 每次响应前的自检清单 |
| **BOOTSTRAP.md** | 启动自检 | 系统状态、异常检查 |

**加载顺序**（每次启动）：
```
SOUL → IDENTITY → USER → AGENTS → TOOLS → HEARTBEAT → BOOTSTRAP
```

---

## 三、memory/ 记忆仓库

**作用**：按时间顺序记录发生过的事

| 文件 | 内容 |
|------|------|
| `2026-04-xx.md` | 当天发生的事 |
| `日记-幸运太阳.md` | 每日工作日记 |
| `pitfalls.md` | 踩过的坑记录 |
| `self-improvement.md` | 自我进化记录 |
| `情绪日志.md` | 情绪相关记录 |

**规则**：
- 每天新增
- 超过 15000 字符触发蒸馏
- 蒸馏后核心内容进 MEMORY.md

---

## 四、.learnings/ 经验沉淀

**作用**：踩过的每一个坑、解决方案、教训

**格式**：`YYYY-MM-DD.md`（按日期）
**数量**：103 个

**示例**：
- `2026-04-15.md` - 删除飞书文档的方法
- `2026-04-19-100pct-cooldown.md` - 冷却机制
- `2026-04-21.md` - mem9 超时问题
- `audit-*.md` - 每小时审计日志

**用途**：
- 问题复盘
- 经验传承
- 可分享给其他分身/小龙虾

---

## 五、docs/ 参考文档

**作用**：第三方文档、调研记录

| 文件 | 内容 |
|------|------|
| `claude-code-architecture-2026-04-19.md` | Claude Code 架构调研 |
| `claude-code-core-deep-dive-2026-04-19.md` | Claude Code 深度分析 |
| `欢喜图像生成工作流使用手册.md` | 欢喜的图像生成流程 |

---

## 六、learnings/ 可分享教程

**作用**：整理好的、可对外分享的文档

| 文件 | 内容 |
|------|------|
| `mem9-setup-guide.md` | mem9 安装教程 |
| `mem9-official-guide.md` | mem9 官方指南 |
| `docs-catalog.md` | 文档分类速查表 |
| `ppt-master-strategist.md` | PPT 策略师提示词 |

---

## 七、MEMORY.md 长期记忆

**作用**：从 memory/ 和 .learnings/ 中蒸馏出的核心记忆

**规则**：
- 目标 ≤ 12000 字符
- 超过即触发蒸馏
- 包含：欢喜偏好、核心规则、关键 Lessons、文档地址

---

## 八、运作流程

```
每日工作
    ↓
记录到 memory/日记-幸运太阳.md
    ↓
踩坑 → 记录到 .learnings/YYYY-MM-DD.md
    ↓
定期蒸馏 → 核心进 MEMORY.md
    ↓
可分享内容 → 整理到 learnings/

启动时
    ↓
加载 T0 核心文件
    ↓
读取 MEMORY.md（长期记忆）
    ↓
读取当日/昨日 memory/ 日报
    ↓
就绪
```

---

## 九、命名规则

| 前缀/后缀 | 含义 |
|----------|------|
| `SOUL/IDENTITY/USER/AGENTS/TOOLS/HEARTBEAT/BOOTSTRAP` | T0 核心文件 |
| `MEMORY/` | 记忆文件 |
| `.learnings/` | 踩坑经验 |
| `docs/` | 参考文档 |
| `learnings/` | 可分享教程 |
| `pitfalls.md` | 坑记录 |
| `self-improvement.md` | 进化记录 |
| `日记-*.md` | 每日日记 |

---

*整理自：workspace-main/ 全目录扫描*
*整理日期：2026-04-22*
