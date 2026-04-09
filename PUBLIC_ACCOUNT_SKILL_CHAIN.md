# 公众号：技能链（对齐总控版式与质感）

任务含 **公众号长文、公众号排版、微信图文、HTML 成稿、走发布草稿模式** 任一时，**必须**按下面顺序读技能与规范再写，不要只靠模型空写。

## 必读顺序

1. **`skills/weixin-wechat-channel/SKILL.md`**  
   策划 → markdown → 润色要求；有 **`wechat_mp_draft` / `wechat_mp_cn`** 时优先用内置工具存草稿。**进草稿箱前必须按 SKILL 里「推送前强制」跑 `sanitize_wechat_html.py`**，再读清洗后文件填工具参数，否则极易出现 `U53CC` 类乱码。
2. **`references/wechat_mp_html_spec.md`**  
   677px 容器、字体、标题与禁止项（与总控所用 `wechat-mp-article-push/design.md` 同源标准）。
3. **需要全文细则时**再读：  
   `/Users/huanxi/Desktop/小龙虾/skills/wechat-mp-article-push/design.md`  
   （若当前工具读不到该路径，以 `references/wechat_mp_html_spec.md` 为准并说明「未读到完整 design」即可。）

## 与总控对齐的写作习惯

- 先定结构再铺文字：分段、空行、`#`/`##` 层次；金句与私域承接位预留。
- **公众号段落要落到规范 HTML**（或工具要求的格式），避免把「像公众号」当成飞书里一段无样式长文。
- 用字：正常中文，禁止 `U53CC`、`\u53CC` 等码位字面量（见 `AGENTS.md`）。

## 与既定流程的关系

- **默认仍先进飞书神稿**（见 `WORKFLOW_AUTOPUBLISH_V1.md`），本链负责**把公众号部分写到总控同级质量**。
- **仅用户明确**「走发布草稿模式 / 直接存公众号草稿」时，再调草稿工具。
