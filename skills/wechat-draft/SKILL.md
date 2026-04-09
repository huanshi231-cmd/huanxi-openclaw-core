---
name: wechat-draft
description: "微信公众号草稿箱推送。输入标题+正文HTML+摘要，自动完成：封面图上传→sanitize清洗→草稿箱推送。用于 content_type=公众号 时。"
---

# 微信公众号草稿箱推送 Skill

自动完成公众号文章推送草稿箱全流程，neirong 只需提供标题和正文内容。

## 输入参数

| 参数 | 说明 |
|------|------|
| title | 文章标题 |
| content | 已清洗的 HTML 正文内容 |
| digest | 摘要（可留空） |
| cover_image_path | 封面图本地路径（可选，不传则用纯色封面） |

## ⛔ 铁律：推送前必须清洗，无论任何情况

**每次推送前，不管是新稿还是修改稿，不管改了什么风格，必须执行：**

```bash
python3 /Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts/sanitize_wechat_html.py \
  tmp/wechat_draft_body.html \
  tmp/wechat_draft_body.clean.html
```

**用 `.clean.html` 的内容推送，不能用原始 HTML。跳过此步 = 必然乱码。**

## 执行流程

1. 把 HTML 正文写入 `tmp/wechat_draft_body.html`
2. 运行 sanitize 脚本，生成 `tmp/wechat_draft_body.clean.html`
3. 读取 `WECHAT_APPID` / `WECHAT_APPSECRET` 环境变量（直连，不走代理）
4. 获取 `access_token`
5. 若有封面图 → 上传到永久素材获取 `thumb_media_id`
6. 用清洗后内容调用微信 `draft/add` 接口推送草稿箱
7. 返回 `media_id` 表示成功

## 微信草稿箱 API

```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
```

Payload:
```json
{
  "articles": [{
    "title": "<标题>",
    "author": "",
    "digest": "<摘要>",
    "content": "<HTML内容>",
    "content_source_url": "",
    "thumb_media_id": "<封面media_id>",
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  }]
}
```

## 错误处理

- `40001` / `40125`：AppID 或 AppSecret 失效 → 检查 `.env`
- `44006`：封面图 media_id 无效 → 重新上传素材
- `60010`：`need_open_comment` 参数问题 → 设为 `0` 重试

## 成功后返回

```json
{
  "media_id": "xxxxxxxx",
  "msg": "草稿箱推送成功"
}
```
