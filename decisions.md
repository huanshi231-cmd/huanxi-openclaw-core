# decisions.md · 决策记录

> 来源：施欢明确做出的决策
> 更新规则：决策一旦确认立即记录

---

## 2026-04-14 · 架构决策

### 首席协调官定位确认
**决策**：幸运太阳定位为首席协调官（COO），各分身执行具体任务
**依据**：T0-Agent协同运营体系V4.0

### 分身调度表确认
| 关键词 | 分身 |
|--------|------|
| 灵感、素材、读书 | linggangshenghuo |
| 疗愈、课程、客户 | liaoyuyewu |
| 创作、发布 | neirong |
| 系统配置、技术问题 | system |
| 记忆检索、历史记录 | memory |

---

## 2026-04-13 · 抗幻觉决策

### 抗幻觉规则全体系执行
**决策**：100%执行抗幻觉协议，真实性优先于一切
**依据**：施欢发送的抗幻觉全体系指令

---

## 2026-04-12 · 元技能决策

### 元技能体系建立
**决策**：建立task-automator、quality-auditor、context-curator、evolution-engineer、security-guardian五大元技能
**依据**：T0进化三部曲 + 亦菲元技能设计

---

## 待确认决策

（施欢还未确认的事项列在这里）


---

## 2026-04-25 · 系统配置决策

### AGENTS.md 蒸馏规则确认
**决策**：AGENTS.md 字符数超过 12000 时，必须立即将 lessons 部分蒸馏到 .learnings/ 目录，仅保留核心规则在 AGENTS.md
**依据**：2026-04-25 质量审计发现 AGENTS.md 达到 17901 字符，存在截断风险

### 插件白名单规则确认
**决策**：所有需要使用的插件必须显式添加到 plugins.allow 配置中，禁止依赖隐式允许
**依据**：2026-04-26 质量审计发现 feishu-doc 插件被排除，导致功能不可用

### 模型配置验证规则确认
**决策**：新增或切换模型前，必须验证 token plan 支持该模型，避免批量 failover
**依据**：2026-04-25 MiniMax-M2.7-highspeed 连续 4 次报错，影响 cron 任务执行

## 2026-04-26 模型优先级调整
- 首选模型：Minimax（minimax-cn/MiniMax-M2.7-highspeed）
- 故障回滚优先级：火山方舟（volcengine-plan/ark-code-latest）
- 调整人：欢喜

## 2026-04-26 模型调用规则最终确认
- 主模型（优先调用）：Minimax M2.7高速版（minimax-cn/MiniMax-M2.7-highspeed）
- 备用回滚模型（主模型故障时自动切换）：火山方舟智能调度（volcengine-plan/ark-code-latest）
- 规则生效范围：所有Agent全局调用
- 确认人：欢喜
