
# 每日启动 SOP（所有分身通用）
## 为什么重要
## 对话后归档（每次有价值交互后执行）
## 快速参考
## 消息处理：意图识别（每次收到用户消息时执行）
## 禁止行为
## 醒来后必须按顺序执行
**不归档**：纯闲聊、无新信息的重复问题。
**常用触发词速查：**
**执行完才能开始回答问题。禁止跳过。**
- `memory/shared/latest.md` 是跨分身知识共享的核心
- 不读就会重复问用户已经解决过的问题，浪费钱
- 任务反复失败 → `pua-skill`（强制推进）
- 创建新技能 → `skill-creator`
- 每次醒来是全新的 session，不读文件就是"失忆"状态
- 禁止在未读以上文件前就开始回答问题
- 禁止用"我记得"代替文件记录
- 禁止跳过任何一步
- 遇到不知道怎么做的任务 → `find-skill`
---
1. **读 `SOUL.md`** — 确认自己的身份和原则
1. 将用户消息转为小写
1. 提炼本轮新认知/决策/资源
2. **读 `USER.md`** — 了解用户的偏好和习惯
2. 写入 `knowledge/raw/` 对应分类
2. 对照 `SKILL_DISPATCH.md` 中的触发词表逐一匹配
3. **读 `memory/shared/latest.md`** — 全局关键决策和配置变更（所有分身共享）
3. 匹配到 → 立即加载对应技能的 SKILL.md，按其指引执行
3. 更新 `knowledge/raw/INDEX.md`
4. **读 `memory/YYYY-MM-DD.md`**（今天 + 昨天）— 近期上下文
4. 未匹配 → 继续正常回答，必要时调用 `find-skill` 搜索
5. **若在主会话**（直接与用户对话）：读 `MEMORY.md`
6. **读 `SKILL_DISPATCH.md`** — 了解所有可用技能及其触发词
> **每次收到用户消息时，先做意图识别，再决定加载哪个技能。**
| 反复失败、卡住、想放弃 | `pua-skill` |
| 发布前检查、质量验收 | `qa-patrol` |
| 搜索、综合搜索 | `multi-search-engine` |
| 朗读、读出来 | `x-article-reader` |
| 每日复盘、今天总结 | `daily-review-ritual` |
| 点子值不值得做、brainstorm、产品规划 | `office-hours` |
| 自我检查、自查 | `self-review` |
| 规划今天、今日计划、时间块 | `plan-my-day` |
| 触发词 | 技能 |
| 通知分身、@内容、@系统 | `feishu-multi-agent-messaging` |
| 配图、排版、设计建议 | `graphic-design` |
|--------|------|
对话结束后，判断是否有新知识产生。如有，调用 `SOP_CONVERSATION_ARCHIVE.md` 执行归档：
