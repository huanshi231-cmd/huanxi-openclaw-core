# TEAM_SESSIONS.md · 7个核心分身会话唯一ID

> 更新：2026-04-28 | 用途：跨Agent协作，太阳用 sessions_send 工具直接呼叫分身

---

## 使用方式

太阳收到任务需要协作时，用 `sessions_send` 工具，target 填对应分身的 session key，发任务内容过去。

---

## 7个核心分身 Session Key

| 分身 | 职责 | Session Key |
|------|------|-------------|
| 太阳 | COO/运营总管 | `agent:main:feishu:system:direct:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 光头强 | 系统官/技术支持 | `agent:system:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 蕊蕊 | 内容官/文案策划 | `agent:neirong:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 朵朵 | 设计官/视觉制作 | `agent:shejiguan:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 跳跳 | 新媒体运营官/内容分发 | `agent:xinmeiyunying:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 灵犀 | 疗愈业务官/咨询服务 | `agent:liaoyuyewu:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 梦梦 | 记忆官/知识沉淀 | `agent:memory:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |

---

## 协作流程

```
欢喜 → 私信太阳发任务
太阳 → 用 sessions_send 发给对应分身
分身 → 在群里回复（欢喜可见整个过程）
太阳 → 汇总回复欢喜
```
