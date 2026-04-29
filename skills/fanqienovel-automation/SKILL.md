---
name: 番茄小说自动化
slug: fanqienovel-automation
version: 1.1.0
description: "通过CDP 9222端口自动化操作番茄小说作家专区。开心果总结的方法：AppleScript打开URL + CDP 9222端口读取页面内容。用于自动创建章节、上传内容等。"
metadata: {"author":"开心果","method":"CDP 9222端口自动化"}
---

# 番茄小说自动化 Skill v1.1

## 概述
本 Skill 用于自动化操作番茄小说作家专区，实现自动创建章节、上传内容等功能。核心方法由开心果总结，结合 AppleScript 和 CDP（Chrome DevTools Protocol）端口 9222。

## 核心步骤

### 1. 启动 Chrome 调试模式
在终端执行以下命令启动 Chrome 并开启调试端口 9222：
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-profile" \
  --no-first-run \
  --no-default-browser-check &
```

### 2. 检查 9222 端口是否监听
```bash
lsof -i :9222
```
如果无输出，说明Chrome调试端口未开启，需重新执行步骤1。

### 3. 用 AppleScript 打开番茄作家专区
```bash
osascript -e 'tell application "Google Chrome" to open location "https://fanqienovel.com/main/writer/"'
```

### 4. 等待页面加载（3-5秒）
```bash
sleep 4
```

### 5. 读取页面内容
使用以下脚本读取页面内容：
```javascript
const CDP = require('chrome-remote-interface');

async function main() {
  const targets = await CDP.List({port: 9222});
  const page = targets.find(t => t.url.includes('fanqie') || t.url.includes('writer'));
  const client = await CDP({port: 9222, target: page.id});
  const {Runtime} = client;
  const result = await Runtime.evaluate({expression: 'document.body.innerText.substring(0, 3000)'});
  console.log(result.result.value);
  await client.close();
}
main();
```

### 6. 点击按钮（如创建章节）
使用以下脚本点击页面上的按钮：
```javascript
const CDP = require('chrome-remote-interface');

async function clickButton(buttonText) {
  const targets = await CDP.List({port: 9222});
  const page = targets.find(t => t.url.includes('fanqie') || t.url.includes('writer'));
  const client = await CDP({port: 9222, target: page.id});
  const {Runtime} = client;
  const clickResult = await Runtime.evaluate({expression: `
    (function() {
      const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
      const btn = buttons.find(b => b.innerText.includes('${buttonText}'));
      if (btn) {
        btn.click();
        return '已点击: ' + btn.innerText.trim();
      } else {
        return '未找到按钮: ${buttonText}';
      }
    })();
  `});
  console.log(clickResult.result.value);
  await client.close();
}

// 示例：点击「创建章节」按钮
clickButton('创建章节');
```

### 7. 填写内容并保存
找到输入框，填入章节标题和正文内容，然后点击保存/存草稿按钮。

## 完整操作流程（实测有效）

1. 启动Chrome调试模式 → `lsof -i :9222` 确认端口监听
2. AppleScript打开作家专区 → 等待4秒
3. 读取页面确认登录态
4. 找到作品《执笔成双》→ 点击进入
5. 点击「创建章节」→ 填入章节标题和正文
6. 点击「保存草稿」→ 完成

## 关键要点
1. **端口 9222 必须开启**：Chrome 必须以调试模式启动
2. **登录态会过期**：如果页面跳转到登录页，说明登录态失效，需重新登录
3. **登录态处理**：每次启动Chrome调试模式后，首次打开作家专区会保持登录态
4. **页面查找**：通过 URL 中包含 `fanqie` 或 `writer` 来定位番茄小说页面
5. **检查登录态**：读取页面内容，如果包含"登录"字样，说明需重新登录

## 使用场景
- 自动创建新章节
- 读取作品数据
- 上传内容
- 分析页面数据

## 异常处理
- **端口未监听**：重新执行Chrome调试命令
- **登录态失效**：用AppleScript重新打开作家专区，扫码登录
- **找不到按钮**：检查页面是否加载完成，增加等待时间
- **CDP连接失败**：重启hermes进程后再试

## 版本记录
- v1.0.0：开心果总结的完整方法，包含 CDP 9222 端口自动化流程
- v1.1.0：补充登录态处理、端口检查、完整操作流程（2026-04-29 实测更新）

---
*本 Skill 由开心果总结，太阳整理记录 v1.1*

## 成功进入编辑器的方法（实测 2026-04-29）

1. **重启Chrome调试模式**（用户手动在终端执行）：
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug-profile" --no-first-run --no-default-browser-check &
   ```

2. **确认端口开启**：
   ```bash
   lsof -i :9222
   ```
   有输出说明端口正常

3. **用AppleScript打开作家专区**：
   ```bash
   osascript -e 'tell application "Google Chrome" to open location "https://fanqienovel.com/main/writer/"'
   ```

4. **等待4-5秒让页面完全加载**

5. **用CDP读取页面验证登录态**：如果页面包含用户名或作品列表，说明登录成功

6. **点击「创建章节」按钮**

7. **进入编辑页面**：可看到编辑器界面，说明成功进入

**关键点**：每次操作前需确认9222端口监听，端口断了需重新启动Chrome调试模式

---

## 📌 组织架构 v1.1（2026-04-29）

### 部门归属
- **部门：** 运营部
- **角色：** 主管
- **系统：** Hermes（外部AI实例）
- **下属：** 跳跳（新媒体运营）、朵朵（视觉设计）

---
