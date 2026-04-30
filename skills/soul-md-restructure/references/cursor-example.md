# Cursor Prompt 结构（5模块）

来源：Cursor IDE 系统提示词

## 整体结构

| 模块 | 核心内容 |
|------|----------|
| Rule of the House | 核心 house rules，触发式 |
| Short Responses | 简短回复规范 |
| Ask Before Func Call | 调用函数前需确认 |
| Personal Connection | 个人偏好/风格 |
| Code Style | 代码风格规范 |

## 亮点

1. **Rule of the House 极简**：只用 3-5 条核心规则，不写大段说明
2. **Short Responses**：明确"简短"的标准（结论先行，无废话）
3. **Personal Connection**：把用户偏好写成事实列表，不用句子
4. **Code Style 实用**：不写理论，直接给 Good/Bad 对比示例

## 可借鉴格式

```markdown
## Rule of the House

- [触发条件] → [动作]
- 不做 X，除非 Y
- 遇到 Z 情况，优先执行 W
```

```markdown
## Personal Connection

- 称呼：叫我 X
- 沟通：中文优先，不中英混杂
- 回复：结论先行，不要解释过程
```
