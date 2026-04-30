---
name: system-admin
description: 系统管理员专用skill。处理系统配置、agent管理、权限设置、文件操作、进程管理、日志分析。当用户提到系统搭建、配置修改、权限管理、agent创建或修改时触发。
---

# 系统管理员 Skill

## 核心能力

- 系统配置管理（openclaw.json）
- Agent创建、修改、删除
- 权限分配与管理
- 文件读写操作
- 进程管理（gateway restart等）
- 日志分析
- 飞书API调用（建群、发消息等）

## 常用操作

### Agent管理
```bash
# 查看所有agent
grep '"id":' ~/.openclaw/openclaw.json

# 添加新agent → 编辑openclaw.json agents.list

# 修改agent权限 → 编辑tools.allow数组
```

### 配置管理
```bash
# 重启gateway
openclaw gateway restart

# 检查配置
openclaw doctor

# 修复配置
openclaw doctor --fix
```

### 飞书操作
```bash
# 获取token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a93ab924cc0b5cc8","app_secret":"bsxxdF53NEfbJV0pcsyGPbW2ogAGuwh7"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 发消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"<chat_id>","msg_type":"text","content":"{\"text\":\"<消息>\"}"}'
```

## 快速修复

| 问题 | 解决 |
|------|------|
| 配置无效 | `openclaw doctor --fix` |
| gateway挂了 | `openclaw gateway restart` |
| 权限不够 | 查agent tools.allow |
| 群无响应 | 查bindings绑定 |
