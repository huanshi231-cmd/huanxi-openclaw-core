---
name: soul-md-restructure
version: 1.0.1
description: "将臃肿的SOUL.md拆分为精简索引版+独立规则子文件。Use when: (1) 用户说'重构SOUL'、'拆分md文件'、'整理规则'; (2) SOUL.md超过200行需要拆分; (3) 规则太多难以维护。Key capabilities: SOUL.md只做索引导航（<120行），禁止只改主文件不拆分，每子文件独立+YAML frontmatter。"
---

# SOUL.md 重构最佳实践

将臃肿的系统规则文件拆分为：精简索引版（主文件） + 独立规则文件（子目录）。

## ⚠️ 硬约束（禁止违反）

- **禁止**只改主文件不拆分，必须拆分出子文件
- SOUL.md 行数 <120，所有子文件行数 <100
- 每子文件必须有 YAML frontmatter
- 触发式规则，禁止描述式规则

## 触发词

重构SOUL、拆分md文件、整理规则、优化系统规则、SOUL.md太长

## 适用场景

- SOUL.md 超过 200 行需要重构
- 规则太多难以维护和定位
- 不同模块规则互相耦合
- 新增规则不知道放哪里

## 操作流程

### 步骤 1：分析现有 SOUL.md

读取完整内容，识别所有模块，按主题归类。

常用模块划分：

```
核心层：人设/价值观/说话风格
规则层：边界规则/执行规则/质量规则/任务模式/情绪理解/记忆规则/真实性规则/进化机制
技能层：Skills索引/记忆文件索引
```

### 步骤 2：拆分文件

原则：
- 每文件一个主题
- 清单化（- [ ] 格式），不写段落
- 触发式规则（非描述式）
- 100 行以内

### 步骤 3：写 YAML frontmatter

每个子文件必须有头部：

```yaml
---
name: 文件名（kebab-case）
description: 一句话描述 + 触发条件
---
```

### 步骤 4：重写 SOUL.md

SOUL.md = 核心人设（<30行） + 三张导航表（rules/skills/memory）

结构示例：
```markdown
# SOUL.md — 名字的核心准则
> v版本 · 日期 · 精简索引版

## 我是谁
（<10行核心人设）

## 规则索引
| 文件 | 职责 | 触发条件 |
|------|------|----------|
| boundary.md | 决策授权与边界 | 需要判断能否执行某操作时 |
| execution.md | 执行规则与触发式行为 | 任务执行中、自我检查时 |

## Skills索引
（Skills目录结构）

## 记忆文件
（memory文件索引）
```

### 步骤 5：验证

- SOUL.md 行数 <120
- 每子文件行数 <100
- 所有文件有 YAML frontmatter
- 无重复内容

## 参考文档

- `references/devin-example.md` — Devin 2.0 结构参考
- `references/cursor-example.md` — Cursor Prompt 结构参考
- `references/official-format.md` — 官方 skill 格式
- `references/aaak-spec.md` — AAAK 压缩记忆格式（可选）

## 常见错误

| 错误 | 正确做法 |
|------|----------|
| SOUL.md 写太多细节 | SOUL.md 只做索引，详细内容放子目录 |
| 用 □ 做清单 | 用 - [ ]（Markdown 兼容） |
| 规则写成交代式 | 触发式：满足条件 → 执行动作 |
| 描述式标题 | 动词式标题：如"边界规则"→"决策授权与边界" |
