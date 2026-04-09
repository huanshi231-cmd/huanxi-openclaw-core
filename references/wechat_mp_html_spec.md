# 公众号 HTML 规范（节选 · 与总控同源）

与仓库技能 `wechat-mp-article-push/design.md` 一致；写公众号长文或出 HTML 时**按本节执行**，不要凭感觉套 div。

## 基础结构

- 单文件 HTML，`lang="zh-CN"`，`<meta charset="UTF-8">`。
- `<title>` 放文章标题；**正文区内不要重复再放一遍与 `<title>` 相同的主标题**。
- 禁止：外链 CSS、JS、`<header>` 包主标题、内容区主标题下画线/左边框装饰标题。

## 容器（677px）

```css
.design-container {
    width: 677px;
    max-width: 100%;
    margin: 0 auto;
    padding: 0;
    box-sizing: border-box;
    background-color: #fff;
}
.content-container {
    padding: 0;
    margin: 0;
}
```

- `body`：微软雅黑 / PingFang SC，背景 `#f5f5f5`，正文色 `#333`。

## 字体与段落

- 正文 `p`：`font-size` 约 15–16px，`line-height: 1.8`。
- `h1` 居中加粗；`h2`/`h3` 分级清晰；**标题层次与 design.md 编号习惯一致**（H1 一、二、三；子级 1.1、1.2…）。

## 图片与金句

- 图最大宽度 677px，居中；`blockquote` 可做金句区（左侧竖线 + 浅底），勿堆花哨渐变。
- 配色：疗愈向以柔和中性色 + 少量强调色；避免乱用多色渐变。

## 推送前清洗（防草稿箱 U53CC）

进 `wechat_mp_draft` 前：**先**把 HTML 写入 `tmp/wechat_draft_body.html`，再执行：

`python3 skills/weixin-wechat-channel/scripts/sanitize_wechat_html.py tmp/wechat_draft_body.html tmp/wechat_draft_body.clean.html`

用清洗后的文件内容填工具参数。详见 `skills/weixin-wechat-channel/SKILL.md` 对应章节。

## 完整版

若需全文细则（配色表、布局组件等），可读本机仓库文件：  
`/Users/huanxi/Desktop/小龙虾/skills/wechat-mp-article-push/design.md`  
（优先用 `fs_read`；若工作区隔离读不到，再请用户把该文件同步到当前工作区 `references/`。）
