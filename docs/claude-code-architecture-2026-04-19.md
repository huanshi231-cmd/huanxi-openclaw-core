# Claude Code 架构深度解析
> 来源：claude-code-sourcemap-main 源码分析
> 日期：2026-04-19
> 目的：学习CC架构，提升OpenClaw和我自己的能力

---

## 一、Tool接口标准化（Tool.ts - 792行）

### 1.1 核心类型定义

```typescript
export type Tool<
  Input extends AnyObject = AnyObject,
  Output = unknown,
  P extends ToolProgressData = ToolProgressData,
> = {
  name: string
  aliases?: string[]  // 向后兼容的别名
  searchHint?: string // 3-10词的能力描述，用于ToolSearch
  
  // 核心方法
  call(args, context, canUseTool, parentMessage, onProgress): Promise<ToolResult<Output>>
  description(input, options): Promise<string>
  
  // Schema
  readonly inputSchema: Input
  readonly inputJSONSchema?: ToolInputJSONSchema
  outputSchema?: z.ZodType<unknown>
  
  // 能力判断
  isConcurrencySafe(input): boolean    // 是否可并发
  isReadOnly(input): boolean            // 是否只读
  isDestructive?(input): boolean        // 是否破坏性操作
  isEnabled(): boolean                  // 是否启用
  
  // 权限
  checkPermissions(input, context): Promise<PermissionResult>
  validateInput?(input, context): Promise<ValidationResult>
  
  // UI渲染
  renderToolResultMessage(content, progress, options): React.ReactNode
  renderToolUseMessage(input, options): React.ReactNode
  renderToolUseProgressMessage?(...): React.ReactNode
  
  // 元数据
  maxResultSizeChars: number  // 结果大小上限
  shouldDefer?: boolean       // 是否需要ToolSearch后才能调用
  alwaysLoad?: boolean        // 是否始终加载
}
```

### 1.2 Tool构建工厂

```typescript
const TOOL_DEFAULTS = {
  isEnabled: () => true,
  isConcurrencySafe: (_input) => false,     // 默认不安全
  isReadOnly: (_input) => false,            // 默认有写操作
  isDestructive: (_input) => false,
  checkPermissions: (input, _ctx) => ({ behavior: 'allow', updatedInput: input }),
  toAutoClassifierInput: (_input) => '',     // 默认跳过安全分类
  userFacingName: (_input) => '',
}

export function buildTool<D extends AnyToolDef>(def: D): BuiltTool<D> {
  return { ...TOOL_DEFAULTS, userFacingName: () => def.name, ...def }
}
```

**关键原则**：
- fail-closed：默认不安全、默认有写操作
- 显式声明：工具必须显式声明自己是安全的

### 1.3 ToolUseContext（工具执行上下文）

```typescript
export type ToolUseContext = {
  options: {
    commands: Command[]
    debug: boolean
    mainLoopModel: string
    tools: Tools
    verbose: boolean
    thinkingConfig: ThinkingConfig
    mcpClients: MCPServerConnection[]
    mcpResources: Record<string, ServerResource[]>
    isNonInteractiveSession: boolean
    agentDefinitions: AgentDefinitionsResult
    maxBudgetUsd?: number
    customSystemPrompt?: string
    appendSystemPrompt?: string
  }
  abortController: AbortController
  messages: Message[]
  // ... 大量状态管理回调
}
```

---

## 二、Task任务系统（Task.ts - 125行）

### 2.1 7种任务类型

```typescript
export type TaskType =
  | 'local_bash'           // 本地bash命令
  | 'local_agent'          // 本地agent
  | 'remote_agent'         // 远程agent
  | 'in_process_teammate' // 进程内队友
  | 'local_workflow'       // 本地工作流
  | 'monitor_mcp'          // MCP监控
  | 'dream'                // 梦境任务
```

### 2.2 任务状态机

```typescript
export type TaskStatus =
  | 'pending'    // 待执行
  | 'running'    // 执行中
  | 'completed'  // 已完成
  | 'failed'     // 失败
  | 'killed'     // 被杀死
```

### 2.3 TaskHandle与TaskStateBase

```typescript
export type TaskHandle = {
  taskId: string
  cleanup?: () => void
}

export type TaskStateBase = {
  id: string
  type: TaskType
  status: TaskStatus
  description: string
  toolUseId?: string
  startTime: number
  endTime?: number
  totalPausedMs?: number
  outputFile: string
  outputOffset: number
  notified: boolean
}
```

### 2.4 任务ID生成

```typescript
const TASK_ID_PREFIXES: Record<string, string> = {
  local_bash: 'b',
  local_agent: 'a',
  remote_agent: 'r',
  in_process_teammate: 't',
  local_workflow: 'w',
  monitor_mcp: 'm',
  dream: 'd',
}
// 8字符随机ID，36^8 ≈ 2.8万亿组合
```

---

## 三、Token计算机制

### 3.1 cl100k_base编码

Claude Code使用 `cl100k_base` 进行token计数（与GPT-4相同）。

### 3.2 核心函数

```typescript
// 从API响应获取实际token使用量
export function getTokenCountFromUsage(usage: Usage): number {
  return (
    usage.input_tokens +
    (usage.cache_creation_input_tokens ?? 0) +
    (usage.cache_read_input_tokens ?? 0) +
    usage.output_tokens
  )
}

// 从消息历史估算token数
export function roughTokenCountEstimationForMessages(messages)
```

### 3.3 Context管理

```typescript
const MAX_CONTEXT_TOKENS = 200000  // Claude最大上下文
const TOKEN_COUNT_THINKING_BUDGET = 1024
const TOKEN_COUNT_MAX_TOKENS = 2048
```

---

## 四、安全机制

### 4.1 权限层级

```typescript
export type PermissionMode = 
  | 'default' 
  | 'plan' 
  | 'bypass' 
  | 'auto' 
  | 'disable'

export type PermissionResult = {
  behavior: 'allow' | 'deny' | 'prompt'
  updatedInput?: Record<string, unknown>
}
```

### 4.2 权限检查流程

1. `validateInput()` - 输入验证
2. `checkPermissions()` - 权限检查
3. `preparePermissionMatcher()` - 规则匹配
4. 权限规则引擎 - 模式匹配（如 `Bash(git *)`）

### 4.3 安全分类器

```typescript
toAutoClassifierInput(input): unknown
// 返回值用于自动模式安全分类
```

---

## 五、多Agent并发

### 5.1 MAX_WORKERS

```typescript
MAX_WORKERS = 4  // 最大并发数
```

### 5.2 任务分发

```typescript
// 根据TaskType分发到不同队列
getTaskByType(type: TaskType) => Task
```

---

## 六、关键设计模式

### 6.1 fail-closed原则

- 默认不允许并发
- 默认有写操作
- 默认跳过安全分类

### 6.2 工具接口一致性

所有工具都通过 `buildTool()` 构建，确保：
- 默认值统一
- 类型安全
- 可预测行为

### 6.3 Context灌注

```typescript
contextModifier?: (context: ToolUseContext) => ToolUseContext
// 允许工具修改自己的执行上下文
```

---

## 七、对OpenClaw的启发

### 7.1 Skills接口标准化

```
当前问题：Skills接口不统一
解决方向：参考Tool.ts，定义标准Skill接口
```

### 7.2 任务类型扩展

```
当前：单一任务类型
参考：7种TaskType精细分类
建议：
- immediate_task (即时任务)
- background_task (后台任务)
- subagent_task (子Agent任务)
- cron_task (定时任务)
```

### 7.3 Token精确计算

```
当前：粗略估算
参考：cl100k_base精确计算
建议：集成token计数库
```

### 7.4 安全机制

```
当前：基础权限控制
参考：多层权限检查 + 自动分类器
建议：
- 输入验证层
- 权限检查层
- 安全分类层
```

---

## 八、行动清单

| 优先级 | 任务 | 状态 |
|--------|------|------|
| P0 | 制定Skills标准接口 | 待办 |
| P1 | 实现精确token计算 | 待办 |
| P2 | 完善权限检查流程 | 待办 |
| P2 | 任务类型精细化 | 待办 |
| P3 | 安全分类器 | 长远目标 |

---

*文档生成时间：2026-04-19 00:15 GMT+8*

---

## 三、Skills 系统（loadSkillsDir.ts 34415行精华）

### 3.1 技能加载五来源

| 来源 | 路径 | 加载方式 | user-invocable |
|------|------|----------|----------------|
| managed | `~/.claude/skills/` | 目录格式 skill-name/SKILL.md | 默认true |
| user | `~/.claude/skills/` | 目录格式 | 默认true |
| project | `./.claude/skills/` | 目录格式 | 默认true |
| additional | `--add-dir`指定 | 目录格式 | 显式指定 |
| legacy | `/commands/` | 兼容 SKILL.md 和单文件 | 默认true |

### 3.2 核心类型：Command

```typescript
type Command = {
  type: 'prompt'
  name: string
  description: string
  whenToUse?: string          // 何时使用
  argumentHint?: string       // 参数提示
  argNames?: string[]         // 参数名列表
  allowedTools?: string[]     // 允许的工具
  model?: string              // 指定模型
  disableModelInvocation?: boolean
  userInvocable?: boolean    // 是否可被用户调用
  context?: 'inline' | 'fork' // 执行上下文
  agent?: string              // 指定agent
  effort?: EffortValue        // 努力等级
  paths?: string[]            // 条件触发路径
  hooks?: HooksSettings       // 生命周期钩子
  skillRoot?: string          // 技能根目录
  source: SettingSource | 'bundled' | 'mcp' | 'plugin'
  loadedFrom: LoadedFrom
  contentLength: number
  isHidden: boolean
  progressMessage: string
  userFacingName(): string
  getPromptForCommand(args, toolUseContext): Promise<ContentBlockParam[]>
}
```

### 3.3 Frontmatter 标准字段

```yaml
---
name: 技能显示名
description: 技能描述
when_to_use: 何时使用此技能
arguments: [arg1, arg2]       # 参数列表
argument-hint: 参数提示文字
allowed-tools: [Read, Write, ...]  # 允许的工具
model: claude-sonnet-4         # 指定模型
disable-model-invocation: false
user-invocable: true          # 是否可被用户调用
context: fork                 # inline | fork
agent: agent-name             # 指定agent
effort: medium                 # effort等级
shell: !                      # 是否执行shell命令
paths:                        # 条件触发路径
  - "src/**/*.ts"
  - "*.md"
hooks:                        # 生命周期钩子
  on_match: ...
  on_invoke: ...
---
```

### 3.4 条件技能（Conditional Skills）

```typescript
// 技能按 paths frontmatter 分为两类
if (skill.paths && skill.paths.length > 0) {
  // 条件技能：只有当匹配的文件被touch时才激活
  conditionalSkills.set(skill.name, skill)
} else {
  // 无条件技能：始终加载
  unconditionalSkills.push(skill)
}
```

### 3.5 技能加载管道

```
loadSkillsFromSkillsDir()     ← 扫描 skill-name/SKILL.md
loadSkillsFromCommandsDir()   ← 扫描 legacy /commands/
        ↓
    Promise.all()              ← 并行加载所有来源
        ↓
    realpath()  deduplicate    ← 按 inode 去重（处理symlink）
        ↓
    分流：conditional vs unconditional
        ↓
    getSkillDirCommands()     ← memoized 结果
```

### 3.6 MCP 技能注册机制

解决循环依赖的注册模式：
```typescript
// mcpSkillBuilders.ts - 叶子模块，打破循环依赖
let builders: MCPSkillBuilders | null = null
export function registerMCPSkillBuilders(b): void { builders = b }
export function getMCPSkillBuilders(): MCPSkillBuilders {
  if (!builders) throw new Error('not registered')
  return builders
}

// loadSkillsDir.ts - 模块初始化时注册
registerMCPSkillBuilders({ createSkillCommand, parseSkillFrontmatterFields })
```

### 3.7 Bundled Skills（内置技能）

内置技能不走文件系统，直接注册：
```typescript
registerBundledSkill({
  name: '内置技能名',
  description: '描述',
  whenToUse: '何时使用',
  allowedTools: ['Read', 'Edit'],
  getPromptForCommand: async (args, ctx) => {
    // 动态生成 prompt 内容
    return [{ type: 'text', text: '...' }]
  }
})
```

### 3.8 安全设计

1. **O_NOFOLLOW | O_EXCL** 防止 symlink 攻击
2. **0o700/0o600** 权限控制
3. **MCP 技能禁止内联 shell**：`if (loadedFrom !== 'mcp')` 才执行 shell
4. **路径遍历防护**：`normalize()` + `..` 检测

---

## 四、Token 计算（cost-tracker.ts）

### 4.1 五维 Token 分类

```typescript
ModelUsage = {
  inputTokens: number           // 输入token
  outputTokens: number          // 输出token
  cacheReadInputTokens: number  // 缓存读（省钱）
  cacheCreationInputTokens: number // 缓存写
  webSearchRequests: number     // 网页搜索次数
  costUSD: number               // 美元成本
  contextWindow: number         // 上下文窗口
  maxOutputTokens: number       // 最大输出
}
```

### 4.2 Session 持久化

```typescript
// 保存当前session成本
saveCurrentSessionCosts()

// 恢复之前session成本（跨session累计）
restoreCostStateForSession(sessionId)

// 存储结构
projectConfig = {
  lastCost: number,
  lastAPIDuration: number,
  lastLinesAdded/Removed: number,
  lastModelUsage: { [model]: ModelUsage },
  lastSessionId: string
}
```

### 4.3 按模型聚合

```typescript
// 按 canonical name 聚合
usageByShortName[shortName] += usage
```

---

## 五、OpenClaw 差距分析

### 5.1 Skills 系统差距

| 项目 | Claude Code | OpenClaw | 差距 |
|------|------------|----------|------|
| 技能来源 | 5种（managed/user/project/additional/legacy） | 2种（workspace/skills） | 大 |
| Frontmatter | 20+字段完整 | 基础 | 大 |
| 条件技能 | ✅ paths触发 | ❌ | 极大 |
| MCP技能 | ✅ 完整注册 | ❌ | 极大 |
| 去重 | realpath inode | 无 | 大 |
| Token统计 | 五维分类 | 无 | 极大 |
| Session持久化 | ✅ save/restore | ❌ | 极大 |
| Bundled技能 | ✅ 内置技能注册 | ❌ | 大 |

### 5.2 落地建议优先级

| 优先级 | 任务 | 理由 |
|--------|------|------|
| P0 | Frontmatter标准化 | 所有技能系统基础 |
| P1 | 五维Token统计 | 计费/优化必需 |
| P1 | 去重机制（inode） | 多workspace场景 |
| P2 | 条件技能触发 | 复杂项目管理 |
| P2 | Session持久化 | 成本追踪 |
| P3 | MCP技能注册 | 高级场景 |

---

*学习时间：2026-04-19 14:28 | 来源：Claude Code sourcemap v1.0*
*核心收获：技能系统的本质是"带元数据的prompt模板工厂"，核心差异在加载管道和元数据标准化*

---

## 六、Query 推理引擎（query.ts 1729行精华）

### 6.1 核心架构：AsyncGenerator + 状态机

```typescript
export async function* query(params: QueryParams): AsyncGenerator<
  StreamEvent | RequestStartEvent | Message | TombstoneMessage | ToolUseSummaryMessage,
  Terminal
>
```

**query() 是外层包装** → 调用 `queryLoop()` → 返回 `AsyncGenerator`

**状态机核心**：while(true) 循环，每次迭代 = 一个 turn

### 6.2 Turn 生命周期（单轮对话）

```
┌─────────────────────────────────────────────────────────┐
│                    while (true)                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. pre-process                                   │  │
│  │   - skill discovery prefetch（并行）             │  │
│  │   - applyToolResultBudget（工具结果预算）         │  │
│  │   - snipCompact（历史裁剪）                       │  │
│  │   - microcompact（微压缩）                        │  │
│  │   - contextCollapse（上下文折叠）                 │  │
│  │   - autoCompact（自动压缩）                       │  │
│  │   - calculateTokenWarningState（token预警）        │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. callModel（流式调用）                          │  │
│  │   - yield stream_request_start                    │  │
│  │   - yield message（流式输出）                      │  │
│  │   - StreamingToolExecutor（流式工具执行）         │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. recovery（错误恢复）                           │  │
│  │   - prompt_too_long → collapse drain / reactive  │  │
│  │   - max_output_tokens → escalate / retry         │  │
│  │   - media_size_error → reactive compact           │  │
│  │   - stop_hook blocking → inject blocking errors   │  │
│  │   - token_budget → continue / stop               │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 4. tool execution（工具执行）                      │  │
│  │   - streamingToolExecutor vs runTools            │  │
│  │   - yield tool result messages                    │  │
│  │   - generateToolUseSummary（Haiku总结）           │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 5. post-processing（后处理）                      │  │
│  │   - get queued commands as attachments           │  │
│  │   - memory prefetch consume                       │  │
│  │   - skill discovery prefetch consume              │  │
│  │   - refreshTools（刷新MCP工具）                  │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 6. next turn（下一轮）                            │  │
│  │   state = { messages: [...all], turnCount++ }    │  │
│  │   continue / return                              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 6.3 五大错误恢复机制

| 错误类型 | 恢复策略 | 优先级 |
|----------|----------|--------|
| prompt_too_long | collapse_drain → reactive_compact → 兜底报错 | P0 |
| max_output_tokens | escalate 8k→64k → inject recovery message → 最多3次 | P1 |
| media_size_error | reactive_compact strip-retry | P1 |
| model_fallback | 切换 fallback model 重试 | P2 |
| stop_hook_blocking | inject blocking errors → continue | P2 |

### 6.4 四大压缩机制（按执行顺序）

```
snipCompact       → 历史消息内容裁剪
     ↓
microCompact      → 单条消息微压缩
     ↓
contextCollapse   → 折叠保留尾部的消息
     ↓
autoCompact       → 触发则替换为 summary + attachments
```

### 6.5 依赖注入（QueryDeps）

```typescript
type QueryDeps = {
  callModel: typeof queryModelWithStreaming  // API调用
  microcompact: typeof microcompactMessages   // 微压缩
  autocompact: typeof autoCompactIfNeeded    // 自动压缩
  uuid: () => string                         // 唯一ID生成
}
```
**作用**：测试可注入 fake，生产用 real 实现

### 6.6 Token Budget 机制

```typescript
type BudgetDecision =
  | { action: 'continue', nudgeMessage, continuationCount, pct }
  | { action: 'stop', completionEvent: { diminishingReturns, ... } }

// 停止条件：
// 1. 消耗 >90% 预算
// 2. 连续3次递减（每次增长 <500 tokens）
```

---

## 七、QueryEngine.ts（46630行 - SDK入口）

### 7.1 核心职责

- 对外暴露 SDK 接口
- 管理整个 session 生命周期
- 协调 query() 和 UI/状态

### 7.2 关键能力

```typescript
type QueryEngineConfig = {
  cwd: string
  tools: Tools
  commands: Command[]        // skill/命令列表
  mcpClients: MCPServerConnection[]
  agents: AgentDefinition[]
  canUseTool: CanUseToolFn
  maxTurns?: number
  maxBudgetUsd?: number
  taskBudget?: { total: number }
  jsonSchema?: Record<string, unknown>  // 结构化输出
  ...
}
```

---

## 八、Claude Code 源码全览总结

### 8.1 核心模块一览

| 模块 | 行数 | 核心职责 |
|------|------|----------|
| main.tsx | 803924 | React渲染/CLI入口 |
| QueryEngine.ts | 46630 | SDK接口/状态协调 |
| query.ts | 1729 | **推理循环/状态机** |
| Tool.ts | 792 | **工具接口标准** |
| Task.ts | 125 | **任务类型定义** |
| cost-tracker.ts | 323 | **Token五维统计** |
| loadSkillsDir.ts | 34415 | **技能加载管道** |
| bundledSkills.ts | ~500 | 内置技能注册 |
| mcpSkillBuilders.ts | ~150 | MCP注册机制 |
| tokenBudget.ts | ~100 | 预算控制 |

### 8.2 OpenClaw 差距总结

| 优先级 | 差距 | 差距量级 | 落地价值 |
|--------|------|----------|----------|
| P0 | 工具接口标准化（Tool泛型） | 极大 | 高 |
| P0 | 推理循环状态机（query模式） | 极大 | 高 |
| P0 | 错误恢复机制（5种恢复路径） | 极大 | 高 |
| P1 | Frontmatter标准（20+字段） | 大 | 高 |
| P1 | 五维Token统计 + Session持久化 | 极大 | 中 |
| P1 | 四大压缩机制（snip/micro/collapse/auto） | 极大 | 中 |
| P2 | 条件技能触发（paths frontmatter） | 大 | 中 |
| P2 | MCP技能注册 | 大 | 中 |
| P3 | Token Budget控制 | 大 | 低 |

### 8.3 最值得借鉴的三个设计

1. **AsyncGenerator 状态机**（query.ts）
   - 每个 turn 是一个循环迭代
   - 错误恢复通过 `continue` 重试
   - 状态全在 State 对象里，不污染外部

2. **依赖注入测试框架**（query/deps.ts）
   - 4个核心依赖可注入 fake
   - 6-8个测试文件共享同一套 mock 模式

3. **渐进式压缩管道**（snip → micro → collapse → auto）
   - 按需触发，互不干扰
   - 兜底永远有 summary 替代

---

## 九、源码学习完毕清单

- [x] Tool.ts（工具接口标准）
- [x] Task.ts（7种任务类型）
- [x] cost-tracker.ts（五维Token统计）
- [x] Skills系统（loadSkillsDir + bundledSkills + mcpSkillBuilders）
- [x] query.ts（推理循环状态机）
- [x] tokenBudget.ts（预算控制）
- [x] deps.ts（依赖注入）
- [x] QueryEngine.ts（SDK入口，结构浏览）
- [x] 全部学习完毕 ✅

---

*Claude Code 源码学习完成 | 2026-04-19 15:44*
*核心结论：Claude Code 的精髓是"错误恢复 + 渐进压缩 + 依赖注入"，这三点值得 OpenClaw 重点借鉴*
