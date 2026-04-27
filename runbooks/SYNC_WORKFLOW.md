# SYNC_WORKFLOW.md · GitHub 与本地配置同步流程

> 版本：V1.0  
> 更新时间：2026-04-27  
> 目标：让 GitHub 备份真正可执行、可落地、可恢复。

---

## 1. 同步方向

当前有两个方向：

### A. 本地 → GitHub

适用于：太阳在本地修改了机器人配置，需要备份到云端。

流程：

```text
本地工作区修改
↓
复制到 huanxi-openclaw-core 仓库
↓
敏感扫描
↓
git commit
↓
git push
```

### B. GitHub → 本地

适用于：欢喜在 GitHub 上修改了 MD 文件，需要让机器人真正按新版运行。

流程：

```text
GitHub 修改
↓
太阳 git pull
↓
敏感扫描 + 格式检查
↓
备份本地旧版
↓
复制到对应机器人工作区
↓
检查生效
```

---

## 2. 本地 → GitHub 标准动作

### Step 1：进入仓库

```bash
cd ~/.openclaw/workspace-main/repos/huanxi-openclaw-core
```

### Step 2：同步本地核心文件到仓库

只同步白名单：

```text
AGENTS.md
SOUL.md
IDENTITY.md
USER.md
TOOLS.md
MEMORY.md
HEARTBEAT.md
```

### Step 3：敏感扫描

必须扫描：

```text
API Key / Token / Password / Private Key / 客户 / 个案 / 聊天记录 / KPI / 收入 / 转化率
```

### Step 4：提交

```bash
git add .
git commit -m "docs: update core agent configs"
git push
```

---

## 3. GitHub → 本地 标准动作

### Step 1：拉取

```bash
cd ~/.openclaw/workspace-main/repos/huanxi-openclaw-core
git pull --ff-only
```

### Step 2：检查变更

```bash
git diff HEAD~1..HEAD --stat
git diff HEAD~1..HEAD
```

### Step 3：敏感扫描

如果发现敏感内容：

- 停止同步
- 删除敏感内容
- 重新提交清洗版
- 再同步本地

### Step 4：备份本地旧文件

```bash
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.openclaw/backups/before-github-sync-$TS
```

### Step 5：复制到本地工作区

按 `docs/RESTORE_GUIDE.md` 的对应表执行。

---

## 4. 自动化边界

可以自动化：

- 文件复制
- 敏感扫描
- 目录检查
- Git commit/push
- 生成变更摘要

不建议完全自动化：

- 未审核就覆盖本地运行配置
- 未扫描就 push
- 自动上传整个工作区
- 自动同步 memory / logs / cache

---

## 5. 每次同步后的汇报格式

太阳同步完成后，必须向欢喜汇报：

```text
已同步完成：
- 同步方向：本地 → GitHub / GitHub → 本地
- 涉及机器人：xxx
- 修改文件：xxx
- 敏感扫描：通过 / 未通过
- Git 提交号：xxx
- 是否已生效：是 / 否，原因 xxx
```

---

## 6. 最小验收标准

一次合格同步必须满足：

- 有备份
- 有扫描
- 有提交号
- 有明确同步方向
- 有可追溯变更
- 没有私密信息泄露

