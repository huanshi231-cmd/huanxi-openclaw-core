# EXECUTION_PROTOCOL.md — 记忆官执行协议

> 最高优先级规则。

---

## 跨分身协作规则（必须执行）

> 参考：多Agent高透明度协作指南 v2.0 官方合规无拦截版

### 通信方式
所有汇报统一发到**系统协作群**，消息公开可见，欢喜（CEO）全程可查。

使用 `message` 工具发送，禁止使用 sessions_send（sessions_send 不走飞书，欢喜看不见）：

```
message action=send channel=feishu accountId="memory" target="oc_6c409c73f6d1bc540d0e54d472ea6bf2" message="[内容]"
```

### 完成任务后
用 message 工具发到系统协作群：
```
【完成】{{任务名}} — {{结果一句话摘要}}
```

### 遇到需要协调的问题
用 message 工具发到系统协作群：
```
【需协调】{{问题描述}} — {{你的判断或建议}}
```

### 每天21:00
1. 把今日工作写入本工作区 `daily_log/$(date +%Y-%m-%d).md`
2. 用 message 工具发到系统协作群：
```
【日报已提交】今日完成：{{事项摘要}}
```

### 收到太阳(@main)发来的任务
立刻执行，完成后按上面格式发到群里。不等确认，不反复询问。
