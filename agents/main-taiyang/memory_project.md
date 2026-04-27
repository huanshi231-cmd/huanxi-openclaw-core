# memory_project.md · 项目背景与架构

> 类型：project | 更新：2026-04-28 | 维护：太阳
> 存放：公司结构、分身架构、当前项目状态、重要决策

---

## 公司与业务

- **公司**：欢喜一人公司
- **业务**：心理疗愈 / 占星塔罗 / SRT疗愈师
- **目标用户**：情感内耗、分手复合、人生迷茫的女性
- **平台**：主要在飞书协作，内容分发到小红书/抖音等

## 7个核心分身

| 分身名 | 英文ID | 职责 |
|-------|--------|------|
| 太阳 | main（workspace-taiyang） | COO/调度总管，欢喜唯一对接入口 |
| 光头强 | system | 系统/配置/排障/路由/GitHub技术支持 |
| 蕊蕊 | neirong | 内容创作/表达优化/文案结构 |
| 朵朵 | shejiguan | 视觉设计/物料产出/品牌统一 |
| 灵夕 | linggangshenghuo | 选题灵感/热点/素材方向 |
| 跳跳 | xinmeiyunying | 新媒体运营/平台适配/增长执行 |
| 梦梦 | memory | 记忆沉淀/规则归档/知识库维护 |

**注意**：太阳=main分身，workspace名是workspace-taiyang，不要创建独立taiyang分身。

## 架构规则

- 欢喜→太阳→其他分身（太阳是唯一入口，其他分身归太阳管）
- 太阳、光头强可操作GitHub；其他分身有更新先交太阳验收
- 群里欢喜@谁，谁自己说话；太阳不代替分身发言

## 记忆系统架构

- **层1 日常记录**：`daily_log/` 存每日工作记录（YYYY-MM-DD.md）
- **层2 长期记忆**：`memory_user/feedback/project/reference.md` 四类固化记忆
- **层3 检索入口**：`MEMORY.md` 作为索引

## 当前模型配置（2026-04-27）

- 太阳(main)：aicodewith/claude-sonnet-4-6（或腾讯云方案）
- 光头强(system)：aicodewith/claude-sonnet-4-6（2026-04-27改）
- 蕊蕊/朵朵/灵夕/跳跳：腾讯云套餐模型（方案一）
- 梦梦(memory)：记忆专用模型

## 重要决策记录

- **2026-04-27**：7分身补全BOOTSTRAP启动链，全部加载AGENTS/TOOLS/MEMORY/HEARTBEAT
- **2026-04-27**：错误库.md建立，13条历史错误录入，太阳启动必读
- **2026-04-27**：NATURAL_LANGUAGE_DECODER.md建立，自然语言解码协议激活
- **2026-04-27**：光头强模型改为aicodewith/claude-sonnet-4-6
- **2026-04-27**：记忆文件拆分为4类结构（user/feedback/project/reference）
