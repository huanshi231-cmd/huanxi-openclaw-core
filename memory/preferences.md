
## 回复格式（2026-04-07补充）
- 飞书上用卡片形式回复（不要用纯文本）

## ⛔ 公众号推送铁律（2026-04-08，永久有效）

**任何一次推送，无论是新稿、修改稿、改颜色、改风格、改字体，都必须执行以下流程，缺一步不可：**

1. 把 HTML 写入 `tmp/wechat_draft_body.html`
2. 运行清洗：
   ```bash
   python3 skills/weixin-wechat-channel/scripts/sanitize_wechat_html.py \
     tmp/wechat_draft_body.html \
     tmp/wechat_draft_body.clean.html
   ```
3. 用 `tmp/wechat_draft_body.clean.html` 的内容推送，不用原始文件
4. 使用 `auto_push_v7.py`，禁止新建其他版本脚本

**不清洗直接推 = 必然乱码。改完 CSS 不等于清洗。改回旧颜色不等于清洗。每次都要重跑。**

## 公众号排版要求（欢喜原话）
- 图片：开头1张、中间1张、结尾1张，共3张，不能更多
- 风格：简洁优雅，参考土星回归那篇
- 禁止：密集插图、过度设计
