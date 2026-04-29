# TEAM_SESSIONS.md · 7个核心分身会话ID与openId

> 更新：2026-04-28 | 维护：太阳

---

## 7个核心分身完整信息

| 分身 | 职责 | openId（飞书@用） | Session Key（sessions_send用） |
|------|------|------------------|-------------------------------|
| 太阳 | COO/运营总管 | `ou_26ef2adfee37cf61503ee6b6cdc2b581` | `agent:main:feishu:system:direct:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 光头强 | 系统官/技术支持 | `ou_1724f0025d51c97fb7fde880ebbb6ae5` | `agent:system:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 蕊蕊 | 内容官/文案策划 | `ou_13de9a82ab69491c4de1a3db0cd1c7d5` | `agent:neirong:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 朵朵 | 设计官/视觉制作 | `ou_72c126be119e94177c40730ef4316278` | `agent:shejiguan:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 跳跳 | 新媒体运营官/内容分发 | `ou_1c9b3d78a919c2d8e6248aed8483c5ae` | `agent:xinmeiyunying:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 灵夕 | 疗愈业务官/咨询服务 | `ou_6be411e6ee853b75368c0ec9c3f8d920` | `agent:liaoyuyewu:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |
| 梦梦 | 记忆官/知识沉淀 | `ou_44b845b99943a85b7ee327597b397ce4` | `agent:memory:feishu:group:oc_6c409c73f6d1bc540d0e54d472ea6bf2` |

欢喜 openId：`ou_310bc6f494ec996cdf92a7ee6dc39e42`

---

## 飞书群@格式（发消息时用）

```
<at user_id="ou_xxx">名字</at>
```

示例：太阳@蕊蕊：
```
<at user_id="ou_13de9a82ab69491c4de1a3db0cd1c7d5">蕊蕊</at>
```

---

## 协作流程

```
欢喜私信太阳 → 太阳判断需要哪些分身
→ 太阳用 sessions_send 或飞书@发任务给分身
→ 分身在群里回复（欢喜可见整个过程）
→ 太阳汇总回复欢喜
```
