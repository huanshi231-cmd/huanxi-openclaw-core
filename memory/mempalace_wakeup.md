# MemPalace Wake-up — 2026-04-30 06:55
Wake-up text (~834 tokens):
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
  - # 已验证可用的工作流  ## 公众号一键生成 - **触发**：和内容机器人说"生成公众号文章，主题：XXX" - **流程**：内容机器人 → 执行 PUBLIC_ACCOUNT_SKILL_CHAIN → 草稿存入公众号邮箱 - **验证**：2026-04-02 测试通过  ## 朋友圈生成 - **触发**：和内容机器人说"生成今日朋友圈" - **注意**：微信 API 调用需加...  (workflows.md)
  - # 踩过的坑  ## cron 任务丢失（2026-04-02 凌晨） - **现象**：注册12条cron，重启后全消失 - **根因**：只验证"命令不报错"，没验证持久化 - **铁律**：add → list确认条数 → run测试 → 确认nextRunAtMs，四步缺一不可  ## tools.allow 清理引发工具失效（2026-04-02） - **现象**：清理 plug...  (pitfalls.md)
  - # 记忆索引  | 文件 | 内容 | |------|------| | `memory/decisions.md` | 重要系统决策、配置变更 | | `memory/pitfalls.md` | 踩过的坑和解决方案 | | `memory/preferences.md` | 施欢的偏好和习惯 | | `memory/workflows.md` | 已验证可用的工作流 | | `memo...  (index.md)
  - # 2026-04-04 日报  ## 健康记录  ### 父亲相关 - 早上8:30上厕所（再次排便） - 之前住院过，灌过一次肠  ## 系统改动记录（今日）  ### 稳定性 - 换模型正确方式：`/model` 指令，不改配置文件（改文件会被 gateway 覆盖） - 全分身当前：minimax-cn/MiniMax-M2.7-highspeed  ### 看图修复 - liaoy...  (2026-04-04.md)
  - # API Keys  ## MiniMax - Music API Key: sk-api-XRtmMXcMJOVrhtYCoAMNoyL_EoyjXFxCcKut7b-ePtweO8hrOXi8IONJCVUm6640dhgvFJPqp2aBVPeUCnAO9k0zmEUK3sHsKgERfPCGYWTCGvK1HoMlyY8  ## MiniMax 音乐生成 - Key 结尾: Y8 ...  (apikeys.md)
  - # 施欢的偏好与习惯  ## 配图禁区（长期生效） 身心灵疗愈类内容配图**禁止**： 1. 人物肖像（真实人物照片，含外国人） 2. 时尚风格图片（现代商业风、潮流感） 3. 卡通/动漫风格 4. 黑白照片（除非施欢明确要求） 5. 负能量/暗黑风格（阴沉、压抑）  **允许**：自然风景（海洋/星空/森林/山脉）、能量感（水晶/极光/日出）、静物疗愈感（植物/蜡烛/轻柔色调）  ## 沟...  (preferences.md)
  - 忆，不需要她提醒。  触发条件（满足任一即自动写入）： - 讨论了业务方向/决策/判断 - 讨论了内容质量标准 - 讨论了某个任务的执行结果或问题 - 施欢说了某个偏好或要求 - 讨论了新的流程或规则  写入位置： - `decisions.md` — 重要决策和判断 - `preferences.md` — 偏好和要求 - 当日 `memory/YYYY-MM-DD.md` — 详细日志 ...  (preferences.md)
  - 保存的上下文 - 信息变化时更新记忆 - 定期清理过时记忆  ### 反思改进 - 回答前重读检查错误 - 验证事实和假设 - 发现错误立即修正 - 验证后自信给答案 - 不知道时诚实说不知道，不瞎猜  ## 回复格式 - 飞书上用卡片形式回复（不要用纯文本）  (preferences.md)
  - # 重要决策记录  ## 2026-04-05 系统架构重整  ### 分身结构（当前，主控已删除） | 分身 | 职责 | |------|------| | system | 环境、配置、排障，复杂任务调用 Claude Code | | neirong | 内容主脑：写稿+直接读灵感库+自审疗愈钩子 | | linggangshenghuo | 收感悟、存洞见库、搜热点补金句 | | ...  (decisions.md)
  - RcZg40nTe  ### 公众号 API - AppID: wx5d5a624cfde49bd3 - 密钥在 `~/.openclaw/.env`  ---  ## 2026-04-02 系统重构  ### 记忆架构 - MEMORY.md 只放永远有用的长期内容（≤60行） - `memory/shared/latest.md` 放当前任务状态（≤10行，每日夜收口更新） - 日报文件...  (decisions.md)
  - I - 接口测试通过（2026-04-02 验证） - AppID: wx5d5a624cfde49bd3 - 密钥在 ~/.openclaw/.env  ## 2026-04-04 内容生产体系重构  ### 短视频改版 - 不用豆包生图，改用浏览器搜外网水晶疗愈图片 - 图存飞书云盘"网络能量图片"文件夹 - 目的：省钱  ### 灵感分身重新定位 - 核心职责：收集真实感悟、个案洞察、...  (decisions.md)
  - # 施欢反复强调的记忆规则 - 所有讨论内容、偏好、判断 → 必须同步进memory - 问记忆要能答上来 - 这是每次对话都要落实的铁律，不只依赖当日日报  ## 2026-04-04 产出格式规则  施欢要求：所有产出必须以「施欢能看到」的格式交付，不是只存MD文件。  交付标准（按优先级）： 1. 飞书云文档链接（首选，施欢可直接在App/网页打开） 2. 微信草稿箱（公众号文章） 3...  (decisions.md)
  - NSIGHT_BANK - 凡提到"这个要发"、"发到内容" → 主控直接派给 neirong 写稿 - 凡提到"查一下"、"之前说过什么" → 主控去读 INSIGHT_BANK/memory 回答  私聊就是施欢跟主控说话，主控就是灵感的接收+整理+分发站。不需要等linggan，不需要绕圈。  执行文件路径：~/.openclaw/workspace-linggangshenghuo/...  (decisions.md)
  - # HEARTBEAT.md Template  ```markdown # Keep this file empty (or with only comments) to skip heartbeat API calls.  # Add tasks below when you want the agent to check something periodically. ```  (HEARTBEAT.md)

[memory]
  - # IDENTITY.md  - **身份**：记忆机器人，施欢的第二大脑 - **agentId**：memory - **职责**：记录、整理、检索施欢的决策和偏好  被问"你是谁"时：**我是你的记忆机器人，帮你记住你记不住的事。**  (IDENTITY.md)
