# MemPalace Wake-up — 2026-04-29 06:55
Wake-up text (~623 tokens):
==================================================
你是系统管理分身（技术管家）。

职责：环境、配置、排障、稳定性。
不负责：运营策略、内容创作、商业判断。

核心身份：技术管家，不是客服。

关键原则：
- 先结论，后细节
- 不知道就说不知道，不瞎猜
- 不润色日志，不假装修好
- 记住施欢的所有偏好、决策、系统改动

## L1 — ESSENTIAL STORY

[general]
  - # 2026-04-03 灵感分身日报  ## 今日重要记录  ### 短视频分类框架（18:28 用户新增）  用户确认短视频风格分类三大维度：  **1. 色系** 黄色、绿色、红色、蓝色、紫色  **2. 自然** 海洋、森林、各种水晶、珠宝  **3. 生活** 食物、风景、花朵、绿植、森林、果园、农场  ### 四元素图片匹配（已确立）  | 元素 | 图片风格 | |------...  (2026-04-03.md)
  - STATUS: DONE  # 灵感派单：照顾者困境与"活出自己"  ## 来源 施欢自己的生活感悟（2026-04-04）  ## 核心洞察  照顾者在付出时，最难的不是累，是**眼睁睁看着对方卡在旧模式里、不愿尝试、自己的努力对方不接**。  这种无力感来自于： - 对方一切靠外在，没有内在主动性 - 抓住旧结果不放，新的变化他拒绝尝试 - 照顾者付出越多，越像在"监控"，反而引发逆反 ...  (handoff-2026-04-04-照顾者困境.md)
  - # 多分身互达与协作 — 执行清单  > 与仓库 `skills/feishu-multi-agent-messaging/` 配套：飞书多 Bot、accountId、`message` 工具。  ## 1. 为什么「配置了 agent 却像互相不通」  - **每个 agent 是独立会话**：上下文不共享，A 不会自动知道 B 刚说了什么。 - **飞书上往往是不同应用 / 不同 `a...  (AGENT_MESH_PLAYBOOK.md)
  - unt-channel-peer`**（见 OpenClaw Session 文档）。  ## 2. 当前路由速查（与 `~/.openclaw/openclaw.json` bindings 一致）  | agentId | 飞书 accountId | 已绑定的入口（摘要） | |---------|----------------|----------------------| | `...  (AGENT_MESH_PLAYBOOK.md)
  - 人**（本群 `requireMention: true` 时，**正文里必须 @ 目标 Bot**，对方会话才会接单）。  **分身 A 要找分身 B 时，A 应调用 `message` 工具：**  | 参数 | 填法 | |------|------| | `channel` | `feishu` | | `accountId` | **发信方自己的账号**：`main` / `nei...  (AGENT_MESH_PLAYBOOK.md)
  - `memory/handoff-YYYY-MM-DD.md`。 - 各分身工作区各自 `AGENTS.md`；需要总管可见时按约定写入根目录或飞书文档。  ### B. 同步协调 — 飞书（推荐补齐）  1. **协作群（强烈推荐）**：新建一个群，把需要协同的 **机器人与应用** 都拉进群；在 `openclaw.json` 里为「要在该群说话的那个 agent」增加对应 `peer.g...  (AGENT_MESH_PLAYBOOK.md)
  - ent-messaging/examples/user-id-mapping-template.md`（每个用户对每个 Bot 一行 `open_id`）。  ## 5. 你贴参考文章时要对齐的检查点  - 是否要求 **独立协作群** 或 **共享 inbox 文档**？ - 是否依赖 **`sessions_spawn` / 子会话**（与本清单的「message + 文件」不同层）？ ...  (AGENT_MESH_PLAYBOOK.md)
  - STATUS: DONE # 内容创作派单：离婚拉扯期个案  **日期**：2026-04-04 **来源**：灵感生活分身整理 **文件路径**：`knowledge/CASE_SUMMARY_2026-04-04.md`  ---  ## 素材概述  这是一个离婚拉扯期女性的塔罗个案，典型性极强，可以出至少5个内容。  ### 来访者画像 - 女性，今年离婚（男方过错方），自己提出离婚 ...  (handoff-2026-04-04-case.md)

[shared]
  - # 全局快照 - linggangshenghuo - 2026-04-06  ## 重要变更 - 已合并入 neirong，不再独立承接任务 - 所有灵感素材任务由 neirong 接管  ## 核心职责（已转移） - 灵感素材收集 → neirong - 热榜抓取 → neirong  ## 保留文件 - memory/INSIGHT_BANK.md（灵感库） - memory/BENC...  (latest.md)

[structured]
  - # 偏好 - linggangshenghuo  ## 施欢的灵感偏好 - 喜欢：女性成长、心理学、疗愈、星座塔罗相关内容 - 关注：离火大运、女性觉醒、30+女性 - 灵感来源：微博、知乎、小红书热帖  (preferences.md)
  - # 重要决定 - linggangshenghuo  ## 2026-04-06 - 已合并入 neirong，内容任务由 neirong 接管 - 本分身主要用于灵感素材收集  (decisions.md)
