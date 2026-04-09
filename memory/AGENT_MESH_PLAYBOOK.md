# 多分身互达与协作 — 执行清单

> 与仓库 `skills/feishu-multi-agent-messaging/` 配套：飞书多 Bot、accountId、`message` 工具。

## 1. 为什么「配置了 agent 却像互相不通」

- **每个 agent 是独立会话**：上下文不共享，A 不会自动知道 B 刚说了什么。
- **飞书上往往是不同应用 / 不同 `accountId`**：发消息时必须带对 **`accountId`**，否则身份或路由会错（详见该 Skill）。
- **私聊 `open_id` 按 Bot 隔离**：同一用户在主 Bot 与子 Bot 下的 `open_id` 不同，需要映射表才能跨 Bot 私聊投递。
- **同群多应用会话串台**：若 `session.dmScope` 为 `per-channel-peer`，同一群 `oc_…` 可能被多个飞书 `accountId` 共用一条会话键，出现「@ 主控却像内容机在答」。多 Bot 协作请用 **`per-account-channel-peer`**（见 OpenClaw Session 文档）。

## 2. 当前路由速查（与 `~/.openclaw/openclaw.json` bindings 一致）

| agentId | 飞书 accountId | 已绑定的入口（摘要） |
|---------|----------------|----------------------|
| `linggangshenghuo` | `main` | 灵感生活群 `oc_2aec7039d593bd0a99c5d83b45f31c3b` |
| `liaoyuyewu` | `main` | 疗愈业务群 `oc_bd38951f2c71b52f8d59d721ceb9a980` |
| `neirong` | `neirong` | 该账号下全部会话（当前偏私聊） |
| `system` | `system` | 系统协作群 `oc_6c409c73f6d1bc540d0e54d472ea6bf2` + 同账号私聊兜底 |
| `main` | `main` | **系统协作群** 同上 `oc_6c…`（与灵感/疗愈群分流绑定，见 `~/.openclaw/openclaw.json`） |

`main` 亦常用 Cursor/默认工作流；飞书未单独绑定的会话以网关策略为准。

### 3.1 三机「互相沟通」怎么操作（系统协作群已通的前提下）

机器人**没有**飞书互私聊；协作 = **在系统协作群里发消息**，必要时 **@ 对方机器人**（本群 `requireMention: true` 时，**正文里必须 @ 目标 Bot**，对方会话才会接单）。

**分身 A 要找分身 B 时，A 应调用 `message` 工具：**

| 参数 | 填法 |
|------|------|
| `channel` | `feishu` |
| `accountId` | **发信方自己的账号**：`main` / `neirong` / `system`（谁执行工具填谁） |
| `target` | 系统协作群 `oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 正文 | 一句话说明意图 + **飞书 @ 目标机器人** +（可选）`[→总控]` / `[→内容]` / `[→系统]` 前缀；长文只写摘要，细节放云文档或 `memory/handoff-*.md` 并发链接 |

**人类串流程**：在群里先 @总控 定调，再 @内容 / @系统 执行；或让总控在转发里 @ 下一棒。

**各分身 `AGENTS.md` 建议加一条硬规则**：用户或任务要求「通知另一分身」时，**禁止只回复做不到**，必须按上表往协作群发一条并 @ 对方。

详见 `skills/feishu-multi-agent-messaging/SKILL.md`（`@用户` XML 格式等）。

## 3. 三道信息管道（至少选两种叠用）

### A. 异步真源 — 仓库文件（已具备）

- 跨分身状态：`memory/HANDOFF_TEMPLATE.md` → 另存为 `memory/handoff-YYYY-MM-DD.md`。
- 各分身工作区各自 `AGENTS.md`；需要总管可见时按约定写入根目录或飞书文档。

### B. 同步协调 — 飞书（推荐补齐）

1. **协作群（强烈推荐）**：新建一个群，把需要协同的 **机器人与应用** 都拉进群；在 `openclaw.json` 里为「要在该群说话的那个 agent」增加对应 `peer.group` 绑定（或约定只用某个 Bot 在群里发进度）。
2. **`message` 发送时必写**：`channel=feishu`、`accountId`（与上表一致）、`target`（`oc_…` 群 或 `ou_…` 私聊）。
3. **群协作节奏**（Skill 摘要）：用户/总管下任务 → 相关 Bot 群内确认 → 执行方群内同步状态 → 需要时 @ 人类 — **状态进群里**，不要假设别的 agent 能读到你私聊里的内容。

### C. 流水线 — 一键 / cron

- 适合：固定步骤、产出落在 **约定路径**（如某目录下的 md/json），下一棒 agent **启动时读文件**。
- 与 A 同类：靠 **路径契约** 而非实时对话。

## 4. 私聊跨 Bot 时

复制并填写：`skills/feishu-multi-agent-messaging/examples/user-id-mapping-template.md`（每个用户对每个 Bot 一行 `open_id`）。

## 5. 你贴参考文章时要对齐的检查点

- 是否要求 **独立协作群** 或 **共享 inbox 文档**？
- 是否依赖 **`sessions_spawn` / 子会话**（与本清单的「message + 文件」不同层）？
- 安全：开放群里的 **MEMORY / 密钥** 仍遵守根目录 `AGENTS.md` 与 `MEMORY.md` 边界。

---

**下一步（人工）**：若同意「协作群」方案，选定群 ID → 在 `bindings` 里为对应 agent 增加该群匹配 → 重启网关（按你的维护窗口）→ 用一条测试消息验证「谁能收到、谁的身份发出」。
