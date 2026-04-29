---
name: mempalace-memory
description: 记忆宫殿搜索增强。查记忆、之前说过什么、系统决策、工作流时使用。
---

# MemPalace 记忆宫殿

基于 Milla Jovovich 和 Ben Sigman 开发的开源记忆系统，已在本地配置。

## 使用方式

### 搜索记忆
直接说"查一下之前关于XXX的记忆"或"之前说过XXX吗"

### 触发词
- 查记忆 / 记忆宫殿
- 之前说过 / 之前讨论过
- 这个任务之前怎么做的
- 查一下系统决策 / 工作流

## 技术细节

- CLI路径：`mempalace`
- 数据目录：`~/.mempalace/palace/`
- 当前索引：4442 个抽屉
- Wing：memory, workspace_neirong, workspace_system, workspace_linggangshenghuo, workspace_liaoyuyewu

## 调用方式

```bash
mempalace search "查询内容" --results 5
mempalace wake-up  # 显示全局上下文
mempalace wake-up --wing workspace_neirong  # 显示指定workspace上下文
```
