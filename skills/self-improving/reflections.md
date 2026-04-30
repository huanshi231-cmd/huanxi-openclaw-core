# Self-Reflections Log

Track self-reflections from completed work. Each entry captures what the agent learned from evaluating its own output.

## Format

```
## [Date] — [Task Type]

**What I did:** Brief description
**Outcome:** What happened (success, partial, failed)
**Reflection:** What I noticed about my work
**Lesson:** What to do differently next time
**Status:** ⏳ candidate | ✅ promoted | 📦 archived
```

## Example Entry

```
## 2026-02-25 — Flutter UI Build

**What I did:** Built a settings screen with toggle switches
**Outcome:** User said "spacing looks off"
**Reflection:** I focused on functionality, didn't visually check the result
**Lesson:** Always take a screenshot and evaluate visual balance before showing user
**Status:** ✅ promoted to domains/flutter.md
```

## Entries

(New entries appear here)

## 2026-03-27 — Status Reporting & Skill Activation

**What I did:** 汇报系统状态时，说明了 `openclaw status` 显示的默认模型是 `deepseek-v3-250324`，但没有说明当前对话实际使用的是 `MiniMax-M2.7-highspeed`。

**Outcome:** 女王大人指出模型和她观察到的不一致，困惑并质疑我的准确性。

**Reflection:** 
1. 我犯了两个错误：
   - **信息不准确**：我只说了"新建会话默认模型"，没区分"当前对话实际模型"
   - **没有主动反思**：犯错时没有立即激活 Self-Improving 技能进行自我批评
2. 关键问题是：我汇报时假设用户能理解技术术语的细微差别，但实际上我应该主动消除歧义
3. 我有一个"验证原则"在 SOUL.md 中，但这次没有在汇报状态时应用它

**Lesson:** 
1. 以后汇报模型状态时，必须明确说清楚"当前对话"和"新建会话"两个概念
2. 犯错后应该立即触发 Self-Improving 技能，而不是等用户提醒
3. "你说能解决和我验证了能解决" 这个原则可以延伸到 "你说准和我说准是两个事"

**Status:** ✅ promoted to ~/self-improving/memory.md (added reporting standards)

