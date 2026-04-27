# IMAGE_DELIVERY_RUNBOOK.md · 图片可见交付规则

> 版本：V1.0 | 更新时间：2026-04-27

## 规则

图片交付必须让欢喜当场可见。

优先级：

1. JPG 格式。
2. 用消息工具的 `media` 原生图片字段发送。
3. 同时复制一份到桌面，方便欢喜本机查看。
4. 不只发本地路径，不只发 GitHub 链接，不只发附件提示。

## 当前桌面交付路径

```text
/Users/huanxi/Desktop/7个核心机器人头像合集_v2.jpg
```

## 如果欢喜说看不到

立刻执行：

```bash
cp <图片路径> ~/Desktop/<清晰文件名>.jpg
```

然后重新用原生图片方式发送。

## 已验证成功方案（2026-04-27）

飞书聊天内可见图片的可靠方案：

1. 先保存 JPG 到桌面。
2. 用 Finder 选中图片文件。
3. `Cmd+C` 复制。
4. 切换到 Feishu 当前对话。
5. `Cmd+V` 粘贴。
6. `Enter` 发送。

验证结果：用户侧收到 `image_key`，说明图片已作为飞书图片进入聊天记录。

## 自动化命令参考

```applescript
set imgPath to POSIX file "/Users/huanxi/Desktop/图片名.jpg"
tell application "Finder"
    activate
    reveal imgPath
end tell
delay 0.8
tell application "System Events"
    keystroke "c" using command down
end tell
delay 0.5
tell application "Feishu" to activate
delay 1.0
tell application "System Events"
    keystroke "v" using command down
    delay 1.5
    key code 36
end tell
```

## 二次验证记录

2026-04-27 15:41，连续发送两张桌面 JPG：

1. `cover_v1_暖紫色治愈风.jpg`
2. `cover_v2_极简莫兰迪风.jpg`

用户侧均返回 `image_key`，确认飞书聊天记录可见。
