# RESTORE_GUIDE.md · 恢复指南

> 版本：V1.0  
> 更新时间：2026-04-27  
> 目的：当本地机器人配置丢失、混乱、被覆盖时，用本仓库恢复核心配置。

---

## 1. 恢复原则

恢复时遵守三条原则：

1. **先备份本地，再覆盖。**
2. **只恢复 7 大核心文件，不碰私密记忆库。**
3. **恢复后必须检查机器人是否能正常读取配置。**

---

## 2. GitHub 仓库地址

```text
https://github.com/huanshi231-cmd/huanxi-openclaw-core
```

仓库为私有仓库。

---

## 3. 本地对应关系

| 仓库目录 | 本地工作区 |
|---|---|
| `agents/main-taiyang/` | `~/.openclaw/workspace-main/` |
| `agents/neirong-ruirui-content/` | `~/.openclaw/workspace-neirong/` |
| `agents/shejiguan-duoduo-design/` | `~/.openclaw/workspace-shejiguan/` |
| `agents/lingxi-inspiration/` | `~/.openclaw/workspace-linggangshenghuo/` |
| `agents/xinmeiyunying-tiaotiao-ops/` | `~/.openclaw/workspace-xinmeiyunying/` |
| `agents/system-guangtouqiang-system/` | `~/.openclaw/workspace-system/` |
| `agents/memory-mengmeng-memory/` | `~/.openclaw/workspace-memory/` |

---

## 4. 恢复步骤

### Step 1：拉取最新仓库

```bash
cd ~/.openclaw/workspace-main/repos/huanxi-openclaw-core
git pull --ff-only
```

### Step 2：创建本地备份

```bash
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.openclaw/backups/before-core-restore-$TS
```

恢复前必须把本地旧文件复制到备份目录。

### Step 3：复制 7 大核心文件

仅复制以下文件：

```text
AGENTS.md
SOUL.md
IDENTITY.md
USER.md
TOOLS.md
MEMORY.md
HEARTBEAT.md
```

不要复制：

```text
.env
memory/
daily_log/
.mempalace/
.openclaw/
logs/
cache/
```

### Step 4：恢复后检查

检查内容：

- 文件是否存在
- 标题是否对应正确机器人
- 是否误带敏感信息
- OpenClaw 是否正常读取

---

## 5. 一键恢复脚本原则

可以写脚本，但脚本必须满足：

- 默认只恢复白名单文件
- 自动备份本地旧版
- 恢复前做敏感扫描
- 恢复后输出变更摘要
- 不自动删除任何文件

---

## 6. 出问题怎么回滚？

如果恢复后发现配置错了：

```bash
cd ~/.openclaw/workspace-main/repos/huanxi-openclaw-core
git log --oneline
```

找到上一个正确版本后：

```bash
git checkout <commit_id>
```

然后重新按恢复步骤复制。

注意：不要随意 `git reset --hard` 本地运行工作区。

---

## 7. 验收标准

恢复完成必须满足：

- 7 个机器人目录都存在
- 每个机器人都有 7 大核心文件
- `docs/TEAM_ROLES.md` 与本地团队结构一致
- 没有敏感信息进入仓库
- 太阳能明确说出当前版本号/提交号

