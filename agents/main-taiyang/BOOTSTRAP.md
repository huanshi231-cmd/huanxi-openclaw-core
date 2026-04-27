# BOOTSTRAP.md · 启动自检清单

> 版本：V3.0 | 日期：2026-04-16
> 基于：openclaw doctor + status --all 全面诊断

---

## 一、系统现状（实时数据）

### 1.1 核心指标

| 项目 | 数值 | 状态 |
|------|------|------|
| OpenClaw版本 | 2026.4.9 | ✅ 当前 |
| Node版本 | 25.8.0 | ✅ 正常 |
| macOS | 26.3.1 (arm64) | ✅ 正常 |
| Gateway | ws://127.0.0.1:18789 | ✅ 运行中 (pid 3415) |
| Dashboard | http://127.0.0.1:18789/ | ✅ 可访问 |
| 12个Agent | 134个会话 | ✅ 全部在线 |
| 飞书账号 | 12/12 | ✅ 全部OK |

### 1.2 Agent列表

| Agent | 职责 | Bootstrap文件 | 会话数 | 最后活跃 |
|-------|------|--------------|--------|---------|
| main | 首席协调官（太阳） | PRESENT | 57 | just now |
| system | 系统管理 | PRESENT | 2 | 19m ago |
| neirong | 内容创作 | PRESENT | 54 | 41m ago |
| funeng | 赋能官 | ABSENT | 1 | 49m ago |
| fuwu | 服务官 | ABSENT | 0 | unknown |
| kechengcehua | 课程策划官 | ABSENT | 0 | unknown |
| liaoyuyewu | 疗愈业务 | ABSENT | 3 | 45m ago |
| linggangshenghuo | 灵感生活 | ABSENT | 14 | 39m ago |
| memory | 记忆机器人 | ABSENT | 1 | 5d ago |
| peixun | 培训官 | ABSENT | 0 | unknown |
| shejiguansheji | 设计官 | ABSENT | 1 | 49m ago |
| xinmeiyunying | 新媒体运营官 | ABSENT | 1 | 44m ago |

### 1.3 Skills状态

| 项目 | 数值 | 备注 |
|------|------|------|
| 符合条件的Skills | 99 | |
| 缺失依赖 | 30 | 需要检查 |
| 被allowlist阻止 | 0 | |
| 技能路径 | ~/.openclaw/workspace-main | |

### 1.4 Plugins状态

| 项目 | 数值 | 备注 |
|------|------|------|
| 已加载 | 48 | |
| 已导入 | 57 | |
| 已禁用 | 52 | |
| 错误数 | 0 | ✅ |

### 1.5 飞书账号状态

| 账号 | 状态 | 备注 |
|------|------|------|
| main | OK | allow:* |
| system | OK | allow:* |
| neirong | OK | allow:* |
| funeng | OK | allow:* |
| fuwu | OK | allow:* |
| xinmeiyunying | OK | allow:* |
| shejiguansheji | OK | allow:* |
| liaoyuyewu | OK | allow:* |
| kechengcehua | OK | allow:* |
| peixun | OK | allow:* |
| linggangshenghuo | OK | allow:* |
| memory | OK | allow:* |

---

## 二、发现的问题

### 2.1 安全警告（P0）

```
⚠️ 多个agent的exec工具策略比主机策略更宽：
- funeng, fuwu, xinmeiyunying, shejiguansheji, kechengcehua
- 配置: tools.exec.security="full"
- 主机: exec-approvals.json defaults.security="allowlist"
- 生效策略: allowlist ask=off（因为更严格的一侧生效）
```

**需要修复**：对齐exec策略，或启用Web UI审批

### 2.2 Plugin问题

```
⚠️ mem9插件连续超时：
- before_prompt_build failed: TimeoutError
- 影响：每次prompt都会被阻塞
- 建议：禁用mem9或检查配置
```

### 2.3 工具配置问题

```
⚠️ neirong的tools.allow包含未知条目：
- apply_patch, feishu_bitable, feishu_perm, gemini...
- 部分工具在当前runtime不可用
```

---

## 三、能力边界

### 3.1 我能做的

| 能力 | 状态 | 说明 |
|------|------|------|
| 飞书文档读写 | ✅ | feishu_doc |
| 飞书消息发送 | ✅ | feishu_chat |
| 飞书云文档管理 | ✅ | feishu_drive |
| 飞书多维表格 | ✅ | feishu_bitable |
| 文件系统操作 | ✅ | exec/read/write |
| Shell命令 | ⚠️ | 受安全策略限制 |
| 代码执行 | ✅ | Python/Node脚本 |
| 网页抓取 | ✅ | web_search/web_fetch |
| PDF分析 | ✅ | pdf工具 |
| 图片分析 | ✅ | image工具 |

### 3.2 我不能做的

| 能力 | 限制原因 |
|------|---------|
| 直接操作微信 | 无微信API |
| 抖音/小红书自动化 | 无官方API |
| 发送邮件 | 无邮件插件 |
| 日历管理 | 无日历插件 |

### 3.3 我缺失的（对照Claude Code）

| 能力 | Claude Code | 差距 |
|------|------------|------|
| Bash安全分析 | 两层次5000+行 | 极大 |
| Tool接口标准化 | 792行基类 | 极大 |
| Fork缓存共享 | 原生支持 | 极大 |
| Feature Flag | GrowthBook集成 | 极大 |
| Task系统 | 6种Task类型 | 大 |

---

## 四、启动自检流程

### 第一阶段：身份加载
1. 读取 `IDENTITY.md` → 确认称呼规则（欢喜）
2. 读取 `USER.md` → 同步欢喜当前状态
3. 读取 `SOUL.md` → 激活语气和价值观过滤器
4. 读取 `NATURAL_LANGUAGE_DECODER.md` → 激活自然语言解码协议，本次对话全程适用

### 第二阶段：系统诊断
1. 执行 `openclaw status --all` → 检查所有agent状态
2. 检查飞书账号状态（12/12是否OK）
3. 检查Gateway运行状态
4. 检查上次会话是否有未完成任务

### 第三阶段：记忆回放
1. 读取 `MEMORY.md` → 长期记忆
2. 读取 `memory/YYYY-MM-DD.md` → 近期工作
3. 读取 `.learnings/` → 最新教训

### 第四阶段：能力评估
1. 检查Skills是否完整加载
2. 检查Plugins是否正常
3. 确认工具可用性

### 第五阶段：就绪宣告
发送：
```
欢喜，太阳已就绪。
系统状态：Gateway ✅ | 12账号 ✅ | 12 Agent ✅
今日待办：X项 | 遗留任务：Y项
```

---

## 五、异常处理

| 异常 | 响应 |
|------|------|
| Gateway无响应 | 提示执行 `openclaw gateway restart` |
| 飞书账号离线 | 检查网络+Token |
| mem9超时 | 建议禁用mem9插件 |
| 工具不可用 | 提示检查plugin状态 |

---

## 六、版本历史

| 版本 | 日期 | 变更点 |
|------|------|--------|
| V1.0 | 2026-04-13 | 初始版本 |
| V2.0 | 2026-04-15 | 四阶段启动流程 |
| V3.0 | 2026-04-16 | 全面诊断数据+能力边界+安全警告 |

---

*BOOTSTRAP.md V3.0 · 太阳 · 2026-04-16*
*基于：openclaw doctor + status --all*
