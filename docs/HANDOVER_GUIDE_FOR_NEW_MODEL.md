# HANDOVER_GUIDE_FOR_NEW_MODEL.md · 新模型/新机器人接手指南

> 版本：V1.0  
> 更新时间：2026-04-27  
> 目的：无论后续使用 MiniMax、豆包、Kimi、GPT，或更换任意机器人，都能按这份说明接手，不误删、不乱传、不跑偏。

---

## 1. 先读什么？

新模型/新机器人接手时，必须按顺序读取：

1. `README.md`：了解仓库用途。
2. `docs/BACKUP_MANUAL.md`：了解备份了什么。
3. `docs/TEAM_ROLES.md`：了解 7 个核心机器人分工。
4. `docs/UPLOAD_BOUNDARY.md`：了解什么绝对不能上传。
5. `docs/RESTORE_GUIDE.md`：了解怎么恢复到本地。
6. `runbooks/SYNC_WORKFLOW.md`：了解怎么同步。
7. 本角色对应目录下的 7 个核心文件。

---

## 2. 先确认自己是谁

根据任务判断自己是哪一个角色：

| 角色 | 目录 |
|---|---|
| 太阳 | `agents/main-taiyang/` |
| 蕊蕊 | `agents/neirong-ruirui-content/` |
| 朵朵 | `agents/shejiguan-duoduo-design/` |
| 灵夕 | `agents/lingxi-inspiration/` |
| 跳跳 | `agents/xinmeiyunying-tiaotiao-ops/` |
| 光头强 | `agents/system-guangtouqiang-system/` |
| 梦梦 | `agents/memory-mengmeng-memory/` |

只读取自己角色文件还不够，必须同时看 `docs/TEAM_ROLES.md`，避免越权。

---

## 3. 本仓库和本地运行区的关系

```text
GitHub 仓库 = 标准备份版
本地 OpenClaw workspace = 实际运行版
```

GitHub 文件改了，不代表机器人已经生效。

要生效，必须按 `docs/RESTORE_GUIDE.md` 同步到本地对应 workspace。

---

## 4. 新模型接手时的标准动作

### Step 1：只读检查

先不要写文件，先检查：

- 仓库是否为私有仓库
- 当前分支是否为 `main`
- 是否有未提交修改
- 是否有敏感内容风险

### Step 2：确认任务类型

判断当前任务属于哪类：

| 类型 | 做法 |
|---|---|
| 查看配置 | 只读，不修改 |
| 修改角色职责 | 改对应 `agents/*` 文件 + `docs/TEAM_ROLES.md` |
| 恢复本地配置 | 按 `RESTORE_GUIDE.md` 执行 |
| 同步 GitHub | 按 `SYNC_WORKFLOW.md` 执行 |
| 头像/视觉 | 改 `design/`，必要时交给朵朵 |
| 系统故障 | 交给光头强/系统官处理 |

### Step 3：执行前备份

任何覆盖本地 workspace 的动作，先备份。

不备份，不覆盖。

### Step 4：执行后汇报

汇报格式：

```text
已完成：xxx
涉及文件：xxx
敏感扫描：通过/未通过
Git 提交号：xxx
是否已同步到本地运行区：是/否
下一步：xxx
```

---

## 5. 严禁动作

新模型/新机器人禁止：

1. 未扫描就上传。
2. 上传整个 `.openclaw` 目录。
3. 上传本地运行数据库、日志、缓存。
4. 把私密资料写进仓库。
5. 未备份就覆盖本地 7 大核心文件。
6. 把 H5 页面仓库和核心配置仓库混用。
7. 以为 GitHub 改了就自动生效。
8. 删除旧文件但不留备份。

---

## 6. 最小可执行恢复流程

如果新模型只需要恢复核心配置，按这个做：

```bash
cd ~/.openclaw/workspace-main/repos/huanxi-openclaw-core
git pull --ff-only
```

然后：

1. 看 `docs/RESTORE_GUIDE.md` 的对应表。
2. 备份本地旧文件。
3. 只复制 7 个核心文件：
   - `AGENTS.md`
   - `SOUL.md`
   - `IDENTITY.md`
   - `USER.md`
   - `TOOLS.md`
   - `MEMORY.md`
   - `HEARTBEAT.md`
4. 不复制任何运行数据目录。
5. 恢复后检查标题是否对应正确角色。

---

## 7. 判断是否成功

成功标准：

- 7 个机器人目录存在。
- 每个机器人有 7 个核心文件。
- `TEAM_ROLES.md` 和各角色文件一致。
- 没有敏感信息进入仓库。
- 本地运行区已按需同步。
- 能说清楚当前 Git 提交号。

---

## 8. 当前仓库定位一句话

这不是聊天记录库，也不是杂物库。

这是欢喜 AI 一人公司的：

> 核心配置备份库 + 新模型接手说明书 + 本地恢复标准件。

