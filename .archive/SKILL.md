# system · Agent Workspace

> 版本：V1.0
> 日期：2026-04-19
> 用途：system Agent的工作空间

## 职责
- 接受cron任务调度
- 按指令执行具体工作
- 结果写入对应workspace

## 文件结构
- SKILL.md：技能定义
- memory/：记忆目录
- knowledge/：知识目录

## 注意事项
- 按cron任务的指令执行
- 完成后静默，不主动打扰
