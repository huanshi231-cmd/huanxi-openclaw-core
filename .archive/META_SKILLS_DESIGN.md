# 亦菲元技能体系 - 完整设计方案

> 基于《亦菲元技能设计》文档，为系统分身创建的元技能体系

---

## 一、核心愿景

**三层进化目标：**
- 自动化：无需指令，主动发现问题
- 智能化：输出可靠，可追溯，可解释
- 智慧化：越用越聪明，能力自生长

---

## 二、五大元技能详细设计

### 1. task-automator（任务管家）

**核心职责：** 任务编排与主动巡检

**心跳检查项：**
- Gateway进程状态
- 磁盘使用率
- Cron任务执行情况

**调用通道：**
- Heartbeat：每10分钟检查
- Cron：每日04:00执行daily-evolution

**daily-evolution四阶段：**
1. 对话整理 - 回顾当日对话
2. 工具盘点 - 检查工具使用情况
3. 最佳实践固化 - 更新到AGENTS.md
4. 报告生成 - 输出进化报告

---

### 2. quality-auditor（质量检察官）

**核心职责：** 质量评估与规则审计

**心跳检查项：**
- 技能依赖状态
- 输出质量评分
- 规则执行一致性

**调用通道：**
- after_tool_call：记录耗时和成功率
- Cron：每小时skills check
- Cron：每日04:30学习成果检测

**审计内容：**
- SOUL.md规则执行情况
- 三轮校验执行率
- 反馈采纳率

---

### 3. context-curator（记忆策展师）

**核心职责：** 上下文优化与记忆蒸馏

**心跳检查项：**
- sessions.json大小
- 上下文长度
- Token使用量

**调用通道：**
- before_prompt_build：控制上下文
- before_compaction：记忆蒸馏
- Cron：每周日02:00记忆清理

**记忆蒸馏流程：**
1. 回顾memory/YYYY-MM-DD.md
2. 对信息评分
3. 高价值内容晋升到MEMORY.md
4. 清理过期信息

---

### 4. evolution-engineer（进化引擎）

**核心职责：** 经验学习与能力生成

**调用通道：**
- agent_end：记录教训到.learnings/
- Cron：每日04:30扫描.learnings/

**触发能力生成条件：**
- 同一错误出现3次以上
- 高频模式识别
- 新技能需求发现

**调用Skills：**
- self-improving-agent
- proactive-agent
- autoskill-evolver
- ontology

---

### 5. security-guardian（安全卫士）

**核心职责：** 安全审计与风险拦截

**心跳检查项：**
- 异常登录记录
- 敏感文件变更
- 外部通信异常

**调用通道：**
- before_tool_call：拦截高危操作

**拦截规则：**
- rm -rf / 类命令
- 外部数据发送
- 配置文件修改
- 未知来源文件执行

---

## 三、六大核心文件（认知基石）

| 优先级 | 文件 | 核心作用 | 更新频率 |
|--------|------|---------|---------|
| 1 | SOUL.md | 身份、价值观、禁令 | 施欢纠错时 |
| 2 | IDENTITY.md | 身份定位 | 几乎不变 |
| 3 | AGENTS.md | SOP、安全红线 | 任务变化时 |
| 4 | USER.md | 施欢偏好 | 发现变化时 |
| 5 | TOOLS.md | 工具使用约定 | 工具变化时 |
| 6 | BOOTSTRAP.md | 启动自检 | 几乎不变 |

---

## 四、四大记忆层

| 记忆类型 | 存储位置 | 更新频率 | 管理元技能 |
|---------|---------|---------|-----------|
| 短期记忆 | memory/diary/YYYY-MM-DD.md | 每日 | context-curator |
| 长期记忆 | MEMORY.md | 每周蒸馏 | context-curator |
| 知识图谱 | knowledge/目录 | 实时 | evolution-engineer |
| 经验教训 | .learnings/目录 | 实时 | evolution-engineer |

---

## 五、六大调用通道

| 通道 | 触发方式 | 元技能 |
|------|---------|--------|
| Hooks | 事件驱动 | security-guardian, quality-auditor, context-curator |
| Cron | 定时 | task-automator, evolution-engineer, quality-auditor |
| Heartbeat | 10分钟周期 | task-automator, quality-auditor, security-guardian |
| CLI | 命令行 | 所有元技能 |
| ContextEngine | 上下文管理 | context-curator |
| Skills | 技能调用 | 所有元技能 |

---

## 六、智慧闭环工作流

```
【每日04:00 - task-automator】
daily-evolution四阶段：
1. 对话整理 → 2. 工具盘点 → 3. 最佳实践固化 → 4. 报告生成

【每日04:30 - evolution-engineer】
扫描.learnings/ → 若有高频模式 → 触发AutoSkill生成

【每小时 - quality-auditor】
skills check → 记录质量数据

【每周日02:00 - context-curator】
memory-hygiene → 记忆蒸馏 → MEMORY.md更新

【实时 - security-guardian】
before_tool_call → 高危拦截

【实时 - quality-auditor】
after_tool_call → 记录耗时和成功率

【会话启动】
六大核心文件注入 → memory/diary加载 → BOOTSTRAP自检
```

---

## 七、缺失组件清单

| 组件 | 状态 | 优先级 | 行动 |
|------|------|--------|------|
| .learnings/目录 | 缺失 | P0 | 创建 |
| ontology知识图谱 | 缺失 | P1 | 研究实现 |
| Dreaming梦境功能 | 缺失 | P1 | 研究实现 |
| autoskill-evolver | 缺失 | P2 | 寻找替代 |
| before_tool_call钩子 | 缺失 | P1 | 研究OpenClaw |
| daily-evolution四阶段 | 部分 | P1 | 完善 |

---

## 八、执行计划

### 第一周
1. 创建.learnings/目录
2. 完善HEARTBEAT.md检查项
3. 完善Cron定时任务

### 第二周
1. 研究OpenClaw Hooks机制
2. 实现context-curator记忆蒸馏
3. 完善evolution-engineer流程

### 第三周
1. 研究ontology知识图谱
2. 实现Dreaming梦境功能
3. 达成智慧化目标

---

