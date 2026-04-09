# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Feishu Delivery (Content Creation)

- Target folder name: `欢喜内容创作`
- Target folder token: `待首次写入后回填`
- Doc title format: `短视频成稿_<主题关键词>_<YYYYMMDD_HHMM>_v1`
- Reply mode: return doc link + one-line summary only
- 说明：仅在需要飞书交付或归档参数时查询本段。

<!-- clawx:begin -->
## ClawX Tool Notes

### uv (Python)

- `uv` is bundled with ClawX and on PATH. Do NOT use bare `python` or `pip`.
- Run scripts: `uv run python <script>` | Install packages: `uv pip install <package>`

### Browser

- `browser` tool provides full automation (scraping, form filling, testing) via an isolated managed browser.
- Flow: `action="start"` → `action="snapshot"` (see page + get element refs like `e12`) → `action="act"` (click/type using refs).
- Open new tabs: `action="open"` with `targetUrl`.
- To just open a URL for the user to view, use `shell:openExternal` instead.
<!-- clawx:end -->

<!-- 生图工具 2026-03-29 -->
## 生图工具配置

### 豆包Seedream（主力）
- 模型：`doubao-seedream-5-0-260128`
- 端点：`https://ark.cn-beijing.volces.com/api/v3/images/generations`
- API Key：`59e227c0-b14c-4e31-b825-0ab44658de81`
- 最小尺寸：2048x2048

### image工具
- 用途：看图理解/分析，不是生图

### 视觉提示词模板
- 飞书文档：`JaVldjJlCoE5q5xnEtDcxKatn0b`

## 生图工具配置

## 生图工具配置（2026-03-29 更新）

### 可用生图工具

1. **豆包Seedream（主力）**
   - 模型：`doubao-seedream-5-0-260128`
   - 端点：`https://ark.cn-beijing.volces.com/api/v3/images/generations`
   - API Key：`59e227c0-b14c-4e31-b825-0ab44658de81`（在volcano配置里）
   - 尺寸：最小 2048x2048（最低像素 3686400）
   - 命令：
     ```bash
     curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer 59e227c0-b14c-4e31-b825-0ab44658de81" \
       -d '{"model":"doubao-seedream-5-0-260128","prompt":"描述","size":"2048x2048","n":1}'
     ```

2. **Gemini生图（暂不可用）**
   - Google API Key有额度限制，暂无法使用
   - 火山智能路由不支持Gemini生图

3. **image工具**
   - 用途：看图理解/分析，不是生图
   - 支持模型：doubao vision等

### 生图流程
1. 用curl调用火山引擎API生成图片
2. 下载图片到本地
3. 用message工具发送图片到飞书

### 视觉提示词模板
- 存在飞书文档：[视觉提示词_Prompt模板库_20260329](https://feishu.cn/docx/JaVldjJlCoE5q5xnEtDcxKatn0b)
- 使用时读取此文档中的prompt模板

## Google Gemini 中转配置（2026-03-29 施欢明确告知）

### Gemini生图中转
- **中转API Key**：`AIzaSyDeB-_BIDRXWveRnEmKDnZWWiHfuCAaBHA`（在liaoyuyewu的models.json里）
- **Base URL**：`https://generativelanguage.googleapis.com/v1beta`
- **可用模型**：
  - `gemini-2.5-flash-image`（生图）
  - `gemini-3.1-flash-image-preview`（生图预览）
- **调用方式**：OpenAI兼容格式
  ```
  POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=AIzaSyDeB-_BIDRXWveRnEmKDnZWWiHfuCAaBHA
  ```

### 已知问题
- 火山智能路由（volcano/ep-xxx）不支持Gemini生图
- 直接调用Google API需要通过中转

### 图片比例参数
- 豆包Seedream支持尺寸：`1024x1024`（1:1）、`2048x2048`（1:1）、可定制比例

## Gemini生图（待配置）

- **模型名称**：`gemini-3.1-flash-image-preview`
- **中转**：通过 aipaibox（`https://api.aipaibox.com/v1`）
- **问题**：当前 aipaibox key（`sk-5IPkEFTj...`）没有该模型权限，需要确认已开通
- **待办**：等待施欢提供有效的 aipaibox Gemini 生图 key

## Gemini/Imagen 生图中转（aipaibox）

- **中转URL**：`https://api.aipaibox.com/v1`
- **当前有效key**：`sk-4jsIegU1l6ve8fAUoOMz9o1OnNzuyS3LPDKDLaaZVUPPsTMG`
- **支持的模型**：
  - `imagen-4.0-ultra-generate-001` ✅ 可用
  - `gemini-3.1-flash-image-preview` ❌ 不支持

## 配图库路径（2026-03-30 新增）

**共享配图目录：** `~/.openclaw/workspace/images/`（主工作空间同步过来的）

**本地配图路径（neirong工作空间）：**
- `/Users/huanxi/.openclaw/workspace-shortvideo/images/healing_new_cover.jpg` — 封面图（迷宫女孩）
- `/Users/huanxi/.openclaw/workspace-shortvideo/images/article_soul_maze.jpg` — 章节图1-内心迷宫
- `/Users/huanxi/.openclaw/workspace-shortvideo/images/article_heart_tangle.jpg` — 章节图2-心结如线
- `/Users/huanxi/.openclaw/workspace-shortvideo/images/article_tarot_stars.jpg` — 章节图3-星盘塔罗

**图片使用规则：**
- 写公众号文章时直接复用以上路径的图片，不重新生成
- 如需上传微信素材，用 `/tmp/` 下的路径（微信上传需要先下载到/tmp）
- 图片模型按次计费，不要重复生成


## 重要：微信API返回内容的解码问题（2026-03-30修复）

微信草稿箱API返回的内容中，中文是Unicode转义格式（如 `\u592a\u9633`），**必须先解码再发送给用户**，否则用户看到的是乱码。

Python解码方法：
```python
import re
def decode_unicode_escapes(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
content = decode_unicode_escapes(raw_api_response)
```

**发送给用户之前，所有来自微信API的文本都必须解码。**

## 公众号输出格式铁律（2026-03-30）

## 飞书发图片标准流程（2026-04-07 永久配置）

### 配置状态
- `mediaLocalRoots` 已添加到 `channels.feishu.accounts.neirong`
- 允许目录：`workspace-neirong/images/`、`workspace-neirong/`、`/tmp/`
- 网关已重启，配置生效

### 发图片 4 步流程
1. **生图** → 豆包 API 生成，保存到 `/tmp/原图.jpg`
2. **压缩** → PIL 压缩到 800x800，quality=85
3. **保存** → `~/.openclaw/workspace-neirong/images/xxx.jpg`
4. **发送** → `message action=send channel=feishu accountId=neirong filePath=工作空间路径`

### Python 压缩模板
```python
from PIL import Image
img = Image.open('/tmp/原图.jpg')
img = img.resize((800, 800), Image.Resampling.LANCZOS)
img.save('/Users/huanxi/.openclaw/workspace-neirong/images/输出.jpg', quality=85)
```

### 禁止
- 不发桌面路径
- 不发链接代替图片
- 不跳过压缩

## 定时搜图任务配置（2026-04-08 新增）

### 每周三搜图补充飞书图库
- **任务ID**: `04d1335c-1ee6-45bb-a1fd-31fccfd7dec3`
- **执行时间**: 每周三 10:00 (cron: `0 0 10 * * 3`)
- **状态**: ✅ 已启用
- **任务内容**: 搜索Pexels补充飞书图库（主题：水晶/星空/自然/脉轮/花卉/光能量），每次20张上传到飞书免费图专区
- **附加任务**: 同时更新QUOTE_BANK待补充区，补充5-10条金句
- **完成动作**: ①发简报到飞书协作群 ②失败告警到协作群

### 免费图片来源
- **Pexels**: https://www.pexels.com/ （免费商用）
- **主题关键词**: 水晶、星空、自然、脉轮、花卉、光能量
- **上传位置**: 飞书免费图专区

### 相关配置文件
- **Cron任务配置**: `/Users/huanxi/.openclaw/cron/jobs.json`
- **金句库**: `knowledge/QUOTE_BANK_HUANXI_V1.md`

### 飞书"网络能量图片"云文档
- **文档token**: `PFpQdcQ64oR82oxf3LRcZg40nTe`
- **用途**: 每周三搜图任务自动插入图片的目标文档
- **上传方式**: 用 `feishu_doc action=upload_image` 上传图片，再用 `feishu_doc action=write` 写入文档
