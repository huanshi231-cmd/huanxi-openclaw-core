# 跨分身协作规则

## 当前分身架构

| 分身 | 职责 | 状态 |
|------|------|------|
| main | 私人助手，记忆写入 | 活跃 |
| system | 技术管家，本分身 | 活跃 |
| neirong | 内容主脑 | 活跃 |
| linggangshenghuo | 灵感素材 | 活跃 |
| liaoyuyewu | 塔罗/占星/SRT审核 | 活跃 |
| memory | 记忆查询 | 活跃 |

---

## 协作原则

### 1. 单一消息源
```
每个任务只由一个分身处理
不重复处理同一消息
```

### 2. 消息路由
```
系统消息 → system
内容问题 → neirong
灵感素材 → linggangshenghuo
疗愈服务 → liaoyuyewu
其他 → main
```

### 3. 协作请求格式
```
发给其他分身的请求：
[协作] xxx
[内容] xxx
[要求] xxx
[回复到] main
```

---

## 协作场景

### 场景1：需要内容支持
```
neirong需要系统帮助
→ 发消息给main
→ main路由给system
→ system执行后回复main
→ main汇总给neirong
```

### 场景2：需要疗愈知识
```
system需要判断疗愈内容
→ 发消息给liaoyuyewu
→ liaoyuyewu提供知识
→ system执行
```

### 场景3：紧急问题
```
任何分身发现紧急问题
→ 直接告知system
→ system立即处理
→ 之后告知main归档
```

---

## 飞书协作群规则

### 消息格式
```
[来源分身] system
[目标分身] neirong
[任务] xxx
[截止] xxx
[回复] 是/否
```

### 回执规则
```
收到请求 → 5分钟内回复
处理完成 → 立即回执
有问题 → 立即反馈
```

---

