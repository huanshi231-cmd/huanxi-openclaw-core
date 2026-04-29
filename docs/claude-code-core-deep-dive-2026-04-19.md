# Claude Code 核心机制深度解析
> 来源：claude-code-sourcemap-main 核心模块
> 日期：2026-04-19 00:20
> 使命：把CC的核心价值落地到OpenClaw

---

## 一、Compaction（压缩）机制 - CC的杀手锏

### 1.1 四层压缩架构

Claude Code能处理200K tokens上下文的秘密：**多层压缩机制**

```
┌─────────────────────────────────────────────────────────┐
│                    用户对话历史                           │
│                  (可能超过200K tokens)                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Snip (剪裁)                                  │
│  - 移除不重要的消息                                     │
│  - 基于tokensFreed计算                                  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Microcompact (微压缩)                         │
│  - 工具结果压缩                                         │
│  - 缓存编辑操作                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Context Collapse (上下文折叠)                  │
│  - 相似消息合并                                         │
│  - 保留关键信息                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Autocompact (自动压缩)                       │
│  - 触发阈值：约150K tokens                             │
│  - 生成摘要替换原始消息                                  │
│  - 保留语义核心                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   API可接受的上下文                       │
│                    (约200K tokens)                       │
└─────────────────────────────────────────────────────────┘
```

### 1.2 源码位置

```typescript
// query.ts 中的压缩调用顺序
queryCheckpoint('query_microcompact_start')
const microcompactResult = await deps.microcompact(...)
queryCheckpoint('query_autocompact_start')
const { compactionResult, consecutiveFailures } = await deps.autocompact(...)
```

### 1.3 关键发现

| 压缩层 | 触发条件 | 作用 |
|--------|----------|------|
| Snip | 每个turn | 剪裁不重要的工具结果 |
| Microcompact | 每个turn | 微压缩工具输出 |
| Context Collapse | Feature Flag | 折叠相似上下文 |
| Autocompact | >150K tokens | 完整摘要压缩 |

---

## 二、QueryEngine（查询引擎）- 1295行

### 2.1 核心职责

```typescript
export class QueryEngine {
  // 核心循环：处理每个turn
  async query(request: QueryRequest): Promise<QueryResult>
  
  // 会话状态管理
  messages: Message[]           // 对话历史
  fileCache: FileStateCache    // 文件缓存
  usage: Usage                 // token使用量
  
  // 工具执行
  tools: Tools                 // 可用工具集
  canUseTool: CanUseToolFn     // 权限检查
}
```

### 2.2 生命周期

```
用户输入 → processUserInput → query循环 → API调用 → 工具执行 → 压缩 → 返回结果
```

---

## 三、Query循环 - 1729行（真正的核心）

### 3.1 主循环结构

```typescript
// query.ts 核心循环
for await (const message of query({...})) {
  // 1. 处理用户消息
  // 2. 发送到API
  // 3. 处理工具调用
  // 4. 执行压缩检查
  // 5. 更新状态
}
```

### 3.2 Token预算追踪

```typescript
// TOKEN_BUDGET feature - 精确控制
const budgetTracker = feature('TOKEN_BUDGET') ? createBudgetTracker() : null

// 关键计算
checkTokenBudget(messages, budgetTracker)
```

### 3.3 关键钩子

```typescript
// 压缩检查点
queryCheckpoint('query_microcompact_start')
queryCheckpoint('query_microcompact_end')
queryCheckpoint('query_autocompact_start')
queryCheckpoint('query_autocompact_end')

// 错误恢复
categorizeRetryableAPIError(error)
```

---

## 四、Tool接口 - 792行（已解析）

**核心原则**：fail-closed
- 默认不安全（isConcurrencySafe = false）
- 默认有写操作（isReadOnly = false）
- 必须显式声明安全

---

## 五、7种Task类型（已解析）

| TaskType | 用途 | 特点 |
|----------|------|------|
| local_bash | 本地命令 | 最常用 |
| local_agent | 本地agent | 子任务 |
| remote_agent | 远程agent | 分布式 |
| in_process_teammate | 进程内队友 | 协作 |
| local_workflow | 工作流 | 自动化 |
| monitor_mcp | MCP监控 | 健康检查 |
| dream | 梦境任务 | 探索性 |

---

## 六、安全机制

### 6.1 多层权限检查

```
validateInput() → checkPermissions() → preparePermissionMatcher() → 规则引擎
```

### 6.2 Auto Classifier（自动分类器）

```typescript
toAutoClassifierInput(input): unknown
// 用于自动模式下的安全决策
```

---

## 七、对OpenClaw的启发 - 落地计划

### 7.1 紧急落地（P0）

**Compaction机制**（CC的杀手锏！）

```
当前问题：上下文超过阈值就崩溃
解决方向：实现多层压缩机制

Phase 1: Microcompact
- 工具结果压缩
- 简单摘要

Phase 2: Autocompact  
- 阈值触发（约150K tokens）
- 生成摘要

Phase 3: Context Collapse
- 相似消息合并
- 长期记忆提取
```

### 7.2 中期优化（P1）

| 优化项 | 当前 | 目标 |
|--------|------|------|
| Token计算 | 估算 | cl100k_base精确 |
| 任务分类 | 单一 | 7种精细分类 |
| 权限检查 | 简单 | 多层检查 |

### 7.3 长期进化（P2）

- 安全分类器
- 自动模式决策
- 预测性压缩

---

## 八、核心代码片段

### 8.1 Autocompact触发

```typescript
const { compactionResult, consecutiveFailures } = await deps.autocompact(
  messages,
  {
    compactionUsage,
    consecutiveFailures,
    lastCompactTime,
    compactThreshold: getAutoCompactThreshold(),
  }
)

if (compactionResult) {
  messages = buildPostCompactMessages(
    messages,
    compactionResult
  )
}
```

### 8.2 Token预算检查

```typescript
import { createBudgetTracker, checkTokenBudget } from './query/tokenBudget.js'

const budgetTracker = createBudgetTracker()
// 每个turn检查
checkTokenBudget(messages, budgetTracker)
```

---

## 九、继续学习计划

| 模块 | 行数 | 优先级 |
|------|------|--------|
| query.ts | 1729 | P0（已完成核心）|
| services/compact/* | - | P0 |
| utils/tokens.ts | - | P1 |
| hooks/permission/* | - | P1 |
| coordinator/* | - | P2 |

---

*文档生成时间：2026-04-19 00:20 GMT+8*
*使命：把CC的核心价值落地到OpenClaw，让太阳"成神"*

---

## 十、AutoCompact核心机制 - 351行

### 10.1 阈值计算

```typescript
const AUTOCOMPACT_BUFFER_TOKENS = 13_000
const WARNING_THRESHOLD_BUFFER_TOKENS = 20_000
const ERROR_THRESHOLD_BUFFER_TOKENS = 20_000

// 触发压缩阈值 = 上下文窗口 - 13_000
export function getAutoCompactThreshold(model: string): number {
  const effectiveContextWindow = getEffectiveContextWindowSize(model)
  return effectiveContextWindow - AUTOCOMPACT_BUFFER_TOKENS
}
```

### 10.2 熔断机制（重要！）

```typescript
// 连续失败3次后停止尝试压缩
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3

// 防止：上下文超过限制时每轮都尝试压缩，浪费API调用
if (tracking?.consecutiveFailures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES) {
  return { wasCompacted: false }  // 直接跳过
}
```

### 10.3 压缩优先级

```
1. SessionMemoryCompact（优先尝试）
   └── 如果成功，直接返回
   
2. Legacy Compact（失败时回退）
   └── 生成对话摘要替换原始消息
```

---

## 十一、Token精确计算 - tokens.ts

### 11.1 三种计算方法

```typescript
// 1. 从API响应获取实际使用量（最准确）
getTokenCountFromUsage(usage)
= input_tokens + cache_creation + cache_read + output_tokens

// 2. 估算当前上下文大小（用于触发判断）
tokenCountWithEstimation(messages)
= 最后一个API响应的实际token + 后续消息的粗略估算

// 3. 纯估算（无API响应时）
roughTokenCountEstimationForMessages(messages)
```

### 11.2 tokenCountWithEstimation核心逻辑

```typescript
export function tokenCountWithEstimation(messages: readonly Message[]): number {
  // 1. 找到最后一个有usage的assistant消息
  // 2. 回溯找到同一个API响应的所有split消息
  // 3. 用实际usage + 后续消息的估算
  return getTokenCountFromUsage(usage) + 
         roughTokenCountEstimationForMessages(messages.slice(i + 1))
}
```

### 11.3 关键常量

```typescript
MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000  // 摘要生成预留
MAX_CONTEXT_TOKENS = 200_000            // Claude最大上下文
```

---

## 十二、MicroCompact - 530行

### 12.1 作用

对工具结果进行即时压缩，不需要触发完整autocompact

### 12.2 压缩的工具类型

```typescript
const COMPACTABLE_TOOLS = new Set([
  'Read',
  ...SHELL_TOOL_NAMES,        // Bash, Shell
  'Grep',
  'Glob',
  'WebSearch',
  'WebFetch',
  'Edit',
  'Write',
])
```

### 12.3 特性

- 图片压缩：`IMAGE_MAX_TOKEN_SIZE = 2000`
- 缓存编辑支持
- 时间基础配置

---

## 十三、compact.ts核心流程 - 1705行

### 13.1 压缩流程

```
1. stripImagesFromMessages() - 移除图片（避免压缩时超限）
2. executePreCompactHooks() - 执行预压缩钩子
3. 调用compactConversation() - 生成摘要
4. executePostCompactHooks() - 执行后压缩钩子
5. runPostCompactCleanup() - 清理
```

### 13.2 摘要生成

```typescript
// 调用API生成摘要，替换原始消息
const compactionResult = await compactConversation(
  messages,
  toolUseContext,
  cacheSafeParams,
  true,  // suppressUserQuestions
  undefined,
  true,  // isAutoCompact
  recompactionInfo,
)
```

---

## 十四、对OpenClaw的落地计划

### 14.1 Phase 1: 紧急实现

| 功能 | 实现 |
|------|------|
| Token精确计算 | 集成cl100k_base或使用API响应 |
| Autocompact触发 | 上下文窗口-13_000触发 |
| 熔断机制 | 连续失败3次停止 |

### 14.2 Phase 2: 精细化

| 功能 | 实现 |
|------|------|
| Microcompact | 工具结果即时压缩 |
| 分层压缩 | Snip → Micro → Auto |

### 14.3 Phase 3: 长期

| 功能 | 实现 |
|------|------|
| Context Collapse | 折叠相似消息 |
| Session Memory | 记忆压缩 |

---

## 十五、核心代码片段

### 15.1 Autocompact触发判断

```typescript
export async function shouldAutoCompact(
  messages: Message[],
  model: string,
  querySource?: QuerySource,
  snipTokensFreed = 0,
): Promise<boolean> {
  const tokenCount = tokenCountWithEstimation(messages) - snipTokensFreed
  const threshold = getAutoCompactThreshold(model)
  
  return tokenCount >= threshold
}
```

### 15.2 熔断检查

```typescript
if (
  tracking?.consecutiveFailures !== undefined &&
  tracking.consecutiveFailures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES
) {
  return { wasCompacted: false }  // 熔断
}
```

---


---

## 十六、权限系统 - 9400+行（CC的核心防线）

### 16.1 Permission Modes（5种模式）

```typescript
// 用户可用的权限模式
const EXTERNAL_PERMISSION_MODES = [
  'acceptEdits',     // 自动接受编辑
  'bypassPermissions', // 绕过权限
  'default',        // 默认（询问）
  'dontAsk',        // 不询问
  'plan',           // Plan模式
]

// 内部模式
type InternalPermissionMode = ExternalPermissionMode | 'auto' | 'bubble'
```

### 16.2 Permission Behaviors（3种行为）

```typescript
type PermissionBehavior = 'allow' | 'deny' | 'ask'
```

### 16.3 权限检查流程

```
工具调用请求
     ↓
validateInput()      ← 第一层：输入验证
     ↓
规则匹配              ← 第二层：模式匹配（如 Bash(git *)）
     ↓
checkPermissions()   ← 第三层：权限检查
     ↓
Classifier          ← 第四层：AI分类器（auto模式）
     ↓
用户/自动决策
```

### 16.4 权限规则来源

```typescript
type PermissionRuleSource =
  | 'userSettings'     // 用户设置
  | 'projectSettings'   // 项目设置
  | 'localSettings'    // 本地设置
  | 'flagSettings'     // CLI标志
  | 'policySettings'   // 策略设置
  | 'cliArg'          // 命令行参数
  | 'command'         // 命令
  | 'session'         // 会话
```

### 16.5 权限更新操作

```typescript
type PermissionUpdate =
  | { type: 'addRules', destination, rules, behavior }
  | { type: 'replaceRules', destination, rules, behavior }
  | { type: 'removeRules', destination, rules, behavior }
  | { type: 'setMode', destination, mode }
  | { type: 'addDirectories', destination, directories }
  | { type: 'removeDirectories', destination, directories }
```

---

## 十七、YoloClassifier（自动模式安全分类器）- 1495行

### 17.1 核心功能

在Auto模式下，AI自动决定是否允许工具调用，不需要用户确认。

### 17.2 分类器结果

```typescript
type YoloClassifierResult = {
  allowed: boolean
  reason: string
  confidence: number
}
```

### 17.3 安全机制

```
1. 不安全操作 → 拒绝
2. 安全操作 → 允许
3. 不确定 → 询问用户
```

---

## 十八、denialTracking（拒绝追踪）- 熔断升级

### 18.1 拒绝计数

```typescript
type DenialTrackingState = {
  bashDenialCount: number
  otherToolDenialCount: number
  lastDenialTime: number
}
```

### 18.2 降级机制

```typescript
// 连续拒绝后，降级到询问模式
const DENIAL_LIMITS = {
  BASH_DENIAL_LIMIT: 5,
  OTHER_TOOL_DENIAL_LIMIT: 3,
}

if (denialCount >= DENIAL_LIMITS.BASH_DENIAL_LIMIT) {
  // 降级：不再自动拒绝，改询问用户
}
```

---

## 十九、对OpenClaw的启发

### 19.1 权限系统

| CC实现 | OpenClaw落地 |
|--------|-------------|
| 5种权限模式 | 当前缺失 |
| 规则来源8种 | 当前只有简单allowlist |
| AI分类器 | 当前缺失 |

### 19.2 优先级

```
P0: 基础权限模式（allow/ask/deny）
P1: 规则匹配（支持通配符）
P2: 拒绝追踪+降级
P3: AI分类器（长远目标）
```

---

## 二十、今日学习总结

### 20.1 已读模块

| 模块 | 行数 | 核心价值 |
|------|------|----------|
| Tool.ts | 792 | 工具接口标准 |
| Task.ts | 125 | 7种任务类型 |
| QueryEngine.ts | 1295 | 查询引擎 |
| query.ts | 1729 | 核心循环 |
| autoCompact.ts | 351 | 自动压缩 |
| compact.ts | 1705 | 压缩核心 |
| microCompact.ts | 530 | 微压缩 |
| tokens.ts | ~300 | Token计算 |
| permissions/* | 9400+ | 权限系统 |
| yoloClassifier.ts | 1495 | AI安全分类 |

### 20.2 核心发现

1. **Compaction是杀手锏**：多层压缩让200K上下文成为可能
2. **熔断机制防浪费**：连续失败3次停止
3. **权限系统极其精细**：8种规则来源 + AI分类
4. **Token计算精确**：API响应 + 增量估算

### 20.3 可以直接抄的

```
1. 阈值公式：context - 13000
2. 熔断：失败3次停止
3. 分层压缩：Snip → Micro → Auto
4. 基础权限模式：allow/ask/deny
```

---


---

## 二十一、安全系统深度分析

### 21.1 工具权限检查流程（useCanUseTool.tsx）

```
工具调用请求
     ↓
hasPermissionsToUseTool()  ← 核心检查函数
     ↓
   ├─→ 'allow' → 直接执行
   ├─→ 'deny' → 记录日志，返回拒绝
   └─→ 'ask'  → 进入权限队列
                ├─→ handleCoordinatorPermission()
                ├─→ handleSwarmWorkerPermission()
                └─→ 用户交互确认
```

### 21.2 权限模式（PermissionMode）

```typescript
type PermissionMode = 
  | 'default'       // 默认询问
  | 'plan'          // Plan模式
  | 'acceptEdits'   // 自动接受编辑
  | 'bypassPermissions'  // 绕过权限
  | 'dontAsk'       // 不询问
  | 'auto'          // 自动模式（AI判断）
```

### 21.3 路径安全验证（filesystem.ts - 1777行）

```typescript
// 危险文件保护
const DANGEROUS_FILES = [
  '.gitconfig', '.bashrc', '.zshrc', '.profile',
  '.mcp.json', '.claude.json'
]

// 危险目录保护
const DANGEROUS_DIRECTORIES = [
  '.git', '.vscode', '.idea', '.claude'
]
```

### 21.4 Shell命令匹配（shellRuleMatching.ts - 228行）

支持三种匹配模式：
```typescript
type ShellPermissionRule =
  | { type: 'exact', command: string }    // 精确匹配
  | { type: 'prefix', prefix: string }   // 前缀匹配（npm:*）
  | { type: 'wildcard', pattern: string } // 通配符匹配（git *）
```

### 21.5 危险命令检测（dangerousPatterns.ts）

```typescript
const CROSS_PLATFORM_CODE_EXEC = [
  'python', 'python3', 'node', 'deno', 'ruby',
  'perl', 'php', 'lua', 'npx', 'bunx', 'bash', 'sh'
]

const DANGEROUS_BASH_PATTERNS = [
  ...CROSS_PLATFORM_CODE_EXEC,
  'zsh', 'fish', 'eval', 'exec', 'env', 'xargs', 'sudo',
  'ssh', 'curl', 'wget', 'git', 'kubectl', 'aws', 'gcloud'
]
```

### 21.6 绕过权限熔断（bypassPermissionsKillswitch.ts）

```typescript
// 绕过权限检查的熔断机制
// 防止在某些情况下无限期绕过安全检查
shouldDisableBypassPermissions()
```

---

## 二十二、Tool接口标准（Tool.ts - 792行）

### 22.1 核心工具接口

```typescript
type Tool<
  Input extends AnyObject = AnyObject,
  Output = unknown,
  P extends ToolProgressData = ToolProgressData,
> = {
  // 工具名称
  name: string
  
  // 可选别名
  aliases?: string[]
  
  // 工具调用入口
  call(
    args: z.infer<Input>,
    context: ToolUseContext,
    canUseTool: CanUseToolFn,
    parentMessage: AssistantMessage,
    onProgress?: ToolCallProgress<P>,
  ): Promise<ToolResult<Output>>
  
  // 工具描述（用于权限提示）
  description(
    input: z.infer<Input>,
    options: {...}
  ): Promise<string>
  
  // 输入Schema
  readonly inputSchema: Input
  
  // 输出Schema
  outputSchema?: z.ZodType<unknown>
}
```

### 22.2 ToolUseContext（工具执行上下文）

```typescript
type ToolUseContext = {
  options: {
    commands: Command[]
    debug: boolean
    mainLoopModel: string
    tools: Tools
    thinkingConfig: ThinkingConfig
    mcpClients: MCPServerConnection[]
    isNonInteractiveSession: boolean
  }
  abortController: AbortController
  readFileState: FileStateCache
  getAppState(): AppState
  setAppState(f: (prev: AppState) => AppState): void
  messages: Message[]
  agentId?: AgentId
  // ...更多字段
}
```

### 22.3 ToolResult结构

```typescript
type ToolResult<T> = {
  data: T
  newMessages?: (UserMessage | AssistantMessage | SystemMessage)[]
  contextModifier?: (context: ToolUseContext) => ToolUseContext
  mcpMeta?: {...}  // MCP协议元数据
}
```

---

## 二十三、Hooks系统（hooks.ts）

### 23.1 钩子类型

```typescript
type HookType = 
  | 'onToolUse'           // 工具使用前后
  | 'onPermissionRequest' // 权限请求
  | 'onCompact'           // 压缩前后
  | 'onMessage'           // 消息处理
  | 'on会话Start'          // 会话开始
  | 'on会话End'            // 会话结束
  | 'onMentions'          // 提及
```

### 23.2 钩子输入输出

```typescript
type HookCallback = (input: HookInput) => HookOutput
type HookJSONOutput = { message?: string; actions?: HookAction[] }
```

---

## 二十四、对OpenClaw的完整落地计划

### 24.1 Phase 1：紧急（1-2周）

| 功能 | 行数 | 优先级 | 状态 |
|------|------|--------|------|
| Token精确计算 | ~300 | P0 | 待实现 |
| Autocompact阈值 | 351 | P0 | 待实现 |
| 熔断机制 | - | P0 | 待实现 |
| 基础权限模式 | 141 | P0 | 待实现 |

### 24.2 Phase 2：重要（1个月）

| 功能 | 行数 | 优先级 | 状态 |
|------|------|--------|------|
| 权限规则引擎 | 9400+ | P1 | 待设计 |
| 路径安全验证 | 1777 | P1 | 待实现 |
| Shell命令匹配 | 228 | P1 | 待实现 |
| 危险命令检测 | 80 | P1 | 待实现 |

### 24.3 Phase 3：长期（持续）

| 功能 | 行数 | 优先级 | 状态 |
|------|------|--------|------|
| MicroCompact | 530 | P2 | 规划中 |
| Context Collapse | - | P2 | 规划中 |
| YoloClassifier | 1495 | P3 | 长远目标 |
| AI安全分类 | - | P3 | 长远目标 |

---

## 二十五、可以直接抄的代码模式

### 25.1 阈值公式

```typescript
// Autocompact触发阈值
const AUTOCOMPACT_BUFFER_TOKENS = 13_000
const threshold = effectiveContextWindow - AUTOCOMPACT_BUFFER_TOKENS

// Warning阈值
const WARNING_THRESHOLD_BUFFER_TOKENS = 20_000
const warningThreshold = threshold - WARNING_THRESHOLD_BUFFER_TOKENS
```

### 25.2 熔断机制

```typescript
const MAX_CONSECUTIVE_FAILURES = 3

if (tracking?.consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
  return { wasCompacted: false }  // 停止重试
}
```

### 25.3 权限检查模板

```typescript
async function hasPermissionsToUseTool(
  tool: Tool,
  input: Record<string, unknown>,
  context: ToolUseContext,
): Promise<PermissionDecision> {
  // 1. 检查规则
  const rules = getAllowRules(context.toolPermissionContext)
  if (matchRule(tool.name, input, rules)) {
    return { behavior: 'allow' }
  }
  
  // 2. 检查危险模式
  if (isDangerousPattern(tool.name, input)) {
    return { behavior: 'deny', message: '危险操作' }
  }
  
  // 3. 询问用户
  return { behavior: 'ask' }
}
```

### 25.4 Shell命令匹配

```typescript
// 支持：精确、前缀、通配符三种模式
matchCommand('git commit', 'git *')  // true
matchCommand('npm install', 'npm:*')  // true
matchCommand('python script.py', 'python')  // true
```

---

