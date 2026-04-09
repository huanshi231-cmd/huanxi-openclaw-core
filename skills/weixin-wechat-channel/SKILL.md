---
name: wechat-public-auto
description: "微信公众号自动发文一站式技能。组合 内容策划 + 人性化润色 + 自动创建草稿，一条龙生成公众号文章保存到草稿箱。Use when user needs to write 公众号文章、微信公众号、create wechat public account article, auto save to draft。"
---

# 微信公众号自动发文一站式技能

整合了 **内容运营专家 + humanizer 人性化润色 + 微信公众号草稿箱** 三个能力，一站式完成从选题到存草稿。

**内容创作分身**：执行本技能前请先读工作区根目录 **`PUBLIC_ACCOUNT_SKILL_CHAIN.md`**；出 HTML 时必须遵守 **`references/wechat_mp_html_spec.md`**（与总控所用 `design.md` 同源），再按下列流程写作。

## 工作流程

1. **接收用户需求** - 用户给出文章主题
2. **内容策划** - 按照 `operations-expert` 内容策略确定受众、价值、目标、结构
3. **写作初稿** - 根据策划写出完整文章，markdown 格式，段落之间空行
4. **人性化润色** - 调用 `humanizer` 去除 AI 写作痕迹，让文字更自然
5. **自动创建草稿** - 自动生成/复用封面，创建草稿保存到微信公众号后台
6. **返回结果** - 告诉用户 Media ID 和成功信息，用户登录公众号就能发布

## 格式要求

- markdown 写作，每个大段落之间必须空一行
- 标题用 `#`、`##` 标记
- 写完润色保证：
  - 去除 AI 套话（"pivotal role", "evolving landscape" 这类）
  - 变化句子长度，避免单调
  - 去掉三连排比、虚假平行结构
  - 去掉emoji、过度加粗
  - 段落之间保证空行，HTML 输出每个块加 `<br>` 保证显示有空行

## 推送前强制：Unicode 清洗（解决草稿箱出现 U53CC / \\uXXXX）

模型有时把 JSON 转义或码位写进正文，微信会**原样展示**。**凡要进草稿箱**，必须先落盘再清洗，**禁止**把未清洗的长字符串直接塞进工具参数。

1. 用 `fs_write` 将完整 HTML（或工具要求的正文）写入工作区 UTF-8 文件，例如 `tmp/wechat_draft_body.html`。
2. 执行（路径相对工作区根）：
   ```bash
   python3 skills/weixin-wechat-channel/scripts/sanitize_wechat_html.py tmp/wechat_draft_body.html tmp/wechat_draft_body.clean.html
   ```
3. 用 `fs_read` 读取 **`tmp/wechat_draft_body.clean.html`**，将**读到的全文**填入 `wechat_mp_draft` / `wechat_mp_cn` 的正文/HTML 字段（字段名以工具 schema 为准）。

**脚本路径**：`skills/weixin-wechat-channel/scripts/sanitize_wechat_html.py`（处理 `\uXXXX`、`U+XXXX`、裸 `U53CC`、**小写 `u8bbau9a6c` 链**〔反斜杠丢失后的 JSON 转义，易把「论马」打成码〕）。

**走 Python `push_draft.py` 时**：脚本已内置清洗，但仍建议上游先生成 `.html` 文件再调用，便于排错。

## 依赖

- **优先**：若当前 OpenClaw 分身已开通工具 **`wechat_mp_draft`** / **`wechat_mp_cn`**，请用内置工具存草稿，且**必须按上一节「推送前强制」先清洗再传参**（与仅写提示词不同，这是防乱码的硬步骤）。
- **脚本方式**：需要环境变量 **`WECHAT_APPID` + `WECHAT_APPSECRET`**（或 **`WECHAT_APP_ID` + `WECHAT_APP_SECRET`**）已配置且**成对匹配**同一公众号。若公众平台后台**重置过 AppSecret**，必须把 `.env` 里两套名字**一起更新**，否则会报「AppID 与 AppSecret 不匹配」（常被口误成 Apple ID）。
- 微信公众平台 **开发 → 基本配置 → IP 白名单**：需包含**发起请求机器的公网 IP**（与是否使用本技能无关；未配置会导致微信接口报错）
- 需要 `requests` `pillow` Python 依赖已安装

## 微信 API 必须直连（忽略系统代理）

若系统或终端里配置了 `HTTP_PROXY`/`HTTPS_PROXY`，`requests` 会默认走代理；代理未开时请求会失败。**凡访问 `https://api.weixin.qq.com` 一律直连**，不要依赖环境变量里的代理（本技能不绑定任何第三方代理或端口广告）。

**最简写法（执行工具/脚本时照抄）：**

```python
import os
import requests

s = requests.Session()
s.trust_env = False  # 不读环境变量里的代理，微信国内直连即可

appid = os.environ["WECHAT_APPID"]
secret = os.environ["WECHAT_APPSECRET"]
r = s.get(
    "https://api.weixin.qq.com/cgi-bin/token",
    params={"grant_type": "client_credential", "appid": appid, "secret": secret},
    timeout=60,
)
```

**备选**：单次请求可写 `proxies={"http": None, "https": None}`；或复用本目录 `scripts/wechat_http.py` 里的 `session()` / `get()` / `post()`。

**说明**：微信公众平台后台的 **IP 白名单** 仍须正确配置（公网出口 IP），与「关不关系统代理」无关；不要为绕开代理去删白名单。

## 作者

组合技能 by OpenClaw session, 2026-03-17
