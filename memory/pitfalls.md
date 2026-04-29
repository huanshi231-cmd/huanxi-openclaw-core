# Pitfalls - 重复踩坑记录

> 记录重复出现2次以上的问题，标记解决状态
> 更新规则：每日学习检测时扫描 .learnings/，重复问题加入此表

---

## 🔴 未解决问题（>24小时）

### 1. Feishu Card HTTP 400 错误
- **首次发现**: 2026-04-12 02:34
- **持续时长**: >36小时
- **错误信息**: `streaming start failed: Error: Create card request failed with HTTP 400`
- **出现次数**: 15+次审计记录
- **根因**: 不明，疑似飞书卡片模板配置或app version问题
- **影响**: 所有飞书卡片消息渲染失败
- **需要**: system子脑专项排查
- **状态**: 🔴 未解决

### 2. Cron 批量 Error（飞书投递缺target）
- **首次发现**: 2026-04-12 07:00-09:00时段
- **持续时长**: >36小时
- **涉及任务**: 11个cron（neirong 8个、linggangshenghuo 2个、liaoyuyewu 1个）
- **错误信息**: `Delivering to Feishu requires target <chatId|user:openId|chat:chatId>`
- **出现次数**: 10+次审计记录
- **根因**: channels.feishu.accounts 缺少defaultTarget配置
- **影响**: 内容生成成功但飞书通知失败，施欢收不到消息
- **需要**: system子脑统一配置飞书账号
- **状态**: 🔴 未解决

### 3. Context Overflow 导致Agent终止
- **首次发现**: 2026-04-12 07:00
- **涉及Agent**: neirong、linggangshenghuo
- **错误信息**: `Context overflow: estimated context size exceeds safe threshold`
- **出现次数**: 5+次
- **根因**: session历史太长，token超限
- **影响**: cron任务执行中断，agent terminated
- **需要**: 定期清理session或增加reserveTokens
- **状态**: 🟡 间歇性出现

### 4. Exec Preflight 拦截脚本执行
- **首次发现**: 2026-04-13 01:01
- **涉及脚本**: format.py、sanitize_wechat_html.py、push_draft.py
- **错误信息**: `exec preflight: complex interpreter invocation detected`
- **出现次数**: 5+次
- **根因**: 使用`cd ... && python3 ...`或heredoc `<<`形式被安全策略拒绝
- **影响**: wechat-draft流程（公众号草稿推送）被阻塞
- **解决方向**: 改用`python3 /path/to/script.py`直接调用
- **需要**: system子脑修改脚本调用方式
- **状态**: 🟡 持续未解决

---

## 🟢 已解决问题

（暂无）

---

## 📝 更新记录

- 2026-04-14: 初始创建，标记4个重复踩坑问题
