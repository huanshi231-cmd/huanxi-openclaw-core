# mem9 云端向量记忆系统配置教程

> M1 M9 云上向量记忆系统 - OpenClaw 记忆插件配置详解

---

## 一、mem9 是什么

mem9 是 OpenClaw 的**云端持久化记忆插件**，将记忆存储在云端（mem9.ai），跨session和跨机器保持记忆。

---

## 二、两条安装路径

| 路径 | 场景 | API Key |
|------|------|---------|
| **Create New** | 首次安装，需要新建 API Key | 自动生成 |
| **Reconnect** | 已有 API Key，重新安装/换机器 | 用户提供已有 Key |

---

## 三、安装命令

```bash
# 正常安装
openclaw plugins install @mem9/mem9

# 网络慢时（大陆环境）
NPM_CONFIG_REGISTRY=https://registry.npmmirror.com openclaw plugins install @mem9/mem9
```

---

## 四、配置 openclaw.json

### Reconnect 配置（含 apiKey）
```json
{
  "plugins": {
    "slots": { "memory": "mem9" },
    "entries": {
      "mem9": {
        "enabled": true,
        "config": {
          "apiUrl": "https://api.mem9.ai",
          "apiKey": "<你的API_KEY>"
        }
      }
    },
    "allow": ["mem9"]
  }
}
```

### Create New 配置（不含 apiKey）
```json
{
  "plugins": {
    "slots": { "memory": "mem9" },
    "entries": {
      "mem9": {
        "enabled": true,
        "config": {
          "apiUrl": "https://api.mem9.ai"
        }
      }
    },
    "allow": ["mem9"]
  }
}
```

---

## 五、重启 Gateway

```bash
openclaw gateway restart
```

**Create New 路径**：重启后从日志提取 `Auto-provisioned apiKey=<id>`，写回配置

---

## 六、验证成功信号

日志中出现任一 = 正常：
```
[mem9] Injecting N memories into prompt context
[mem9] Ingest accepted for async processing
[mem9] Server mode (v1alpha2)
```

---

## 七、配置 key 速查

| Key 路径 | 值 |
|---------|------|
| `plugins.slots.memory` | `"mem9"` |
| `plugins.entries.mem9.enabled` | `true` |
| `plugins.entries.mem9.config.apiUrl` | `https://api.mem9.ai` |
| `plugins.entries.mem9.config.apiKey` | API Key |
| `plugins.allow` | `["mem9"]` |

---

## 八、当前配置

- **API Key**：`efe4b1ee-d264-4f8b-8657-7d75aac116ab`
- **管理后台**：https://mem9.ai/your-memory/

---

*整理自：mem9-ai SKILL.md + SETUP.md（v1.0.38） 整理日期：2026-04-22*
