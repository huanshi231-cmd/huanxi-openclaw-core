
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

## 写歌/写歌词工作流程（2026-04-10 新增）

### 触发条件
- 施欢说"写歌"或"写歌词"

### 执行流程
1. **收集信息**：施欢会告诉男歌手 + 风格 + 主题
2. **写完整歌词**：
   - 结构：Intro → 主歌A → 副歌A → 主歌B → 副歌B → 结尾
   - 每段都要写完整，不能跳词
   - 不完整=不合格，要重做
3. **生成音乐**：调用 MiniMax music-2.5 API
   - 端点：https://api.minimax.chat/v1/music_generation
   - 模型：music-2.5
   - 时长：90秒
4. **保存桌面**：
   - 格式：neirong_[歌名].mp3
   - 例如：neirong_深海的锚.mp3

### API Key（MiniMax 音乐生成）
sk-api-XRtmMXcMJOVrhtYCoAMNoyL_EoyjXFxCcKut7b-ePtweO8hrOXi8IONJCVUm6640dhgvFJPqp2aBVPeUCnAO9k0zmEUK3sHsKgERfPCGYWTCGvK1HoMlyY8

### 解码方式
返回的音频数据是 hex 编码，不是 base64
audio_bytes = bytes.fromhex(data['data']['audio'])

---

## 图片查看方式（2026-04-10 施欢强调）

### 飞书消息中的图片
消息里会有 `image_key` 和 `Description` 字段，系统会自动传递图片描述给neirong。**不需要额外操作，直接回复即可。**

### 本地图片
用 `image` 工具读取路径，如 `/Users/huanxi/.openclaw/workspace-neirong/images/xxx.png`

### 施欢强调
施欢经常发图片，**neirong必须能正常查看图片，不许说看不了。**


## 2026-04-25 内容官正式名字
内容官（neirong分身）的正式名字为：蕊蕊，后续回复开头需标注【蕊蕊】
