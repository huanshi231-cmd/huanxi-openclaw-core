# mem9 云端向量记忆系统 - 官方安装指南

> 来源：mem9.ai 官方文档 + GitHub README
> 官方地址：https://mem9.ai/openclaw-memory

---

## 一、mem9 是什么

mem9 是 OpenClaw 的**云端持久化记忆插件**，实现：
- 跨 session 和机器的持久记忆
- 多 Agent 共享记忆层
- 混合检索（向量+关键词）+ 可视化仪表盘

---

## 二、安装方式（任选其一）

### 方式 A：从 ClawHub 安装（推荐）
```bash
openclaw plugins install @mem9/mem9
```

### 方式 B：从 GitHub 源码安装
```bash
git clone https://github.com/mem9-ai/mem9.git
cd mem9/openclaw-plugin
npm install
```

**网络慢时（大陆环境）**：
```bash
NPM_CONFIG_REGISTRY=https://registry.npmmirror.com openclaw plugins install @mem9/mem9
```

---

## 三、配置 openclaw.json

mem9 以 **kind: "memory"** 插件形式加载，替换 OpenClaw 内置的记忆槽位。

### Hosted API（使用 mem9 官方服务器）
```json
{
  "plugins": {
    "slots": { "memory": "mem9" },
    "entries": {
      "mem9": {
        "enabled": true,
        "config": {
          "apiUrl": "https://api.mem9.ai",
          "apiKey": "<你的API_KEY>",
          "searchTimeoutMs": 15000,
          "defaultTimeoutMs": 8000
        }
      }
    },
    "allow": ["mem9"]
  }
}
```

### Self-hosted（自建服务器）
```json
{
  "plugins": {
    "slots": { "memory": "mem9" },
    "entries": {
      "mem9": {
        "enabled": true,
        "config": {
          "apiUrl": "http://你的服务器地址:8080",
          "apiKey": "<API_KEY>"
        }
      }
    }
  }
}
```

---

## 四、配置参数详解

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `apiUrl` | string | mnemo-server 地址 | 必填 |
| `apiKey` | string | API Key（v1alpha2 方式） | 必填 |
| `searchTimeoutMs` | number | 记忆搜索超时(ms) | 15000 |
| `defaultTimeoutMs` | number | 其他请求超时(ms) | 8000 |
| `debug` | boolean | 调试日志开关 | false |
| `tenantID` | string | apiKey 的旧版别名 | - |

**注意**：`apiKey` 优先于 `tenantID`。不要把 Key 放在 URL 路径里。

---

## 五、两条安装路径

### 路径 1：Reconnect（已有 API Key）
已有 mem9 账号，直接填入 `apiKey`，重启即可。

### 路径 2：Create New（首次安装）
1. `apiKey` 先留空，重启 OpenClaw
2. 重启后发一条消息，触发自动创建
3. 从日志提取：`[mem9] *** Auto-provisioned apiKey=<id> ***`
4. 将 Key 写回 `plugins.entries.mem9.config.apiKey`
5. 无需再次重启，验证即可

---

## 六、重启与验证

```bash
# 重启 Gateway
openclaw gateway restart
```

**验证成功信号**（日志中出现任一即可）：
```
[mem9] Server mode (v1alpha2)
[mem9] Injecting N memories into prompt context
[mem9] Ingest accepted for async processing
```

**验证命令**：
```bash
openclaw gateway logs 2>&1 | grep mem9
```

---

## 七、mem9 提供的 5 个工具 + 4 个钩子

### 5 个工具（Tool）
| 工具 | 用途 |
|------|------|
| `memory_store` | 存储新记忆 |
| `memory_search` | 混合检索（向量+关键词） |
| `memory_get` | 按 ID 获取单条记忆 |
| `memory_update` | 更新已有记忆 |
| `memory_delete` | 删除记忆 |

### 4 个生命周期钩子（Hook）
| 钩子 | 触发时机 | 功能 |
|------|---------|------|
| `before_prompt_build` | 每次 LLM 调用前 | 搜索相关记忆并注入上下文 |
| `after_compaction` | /compact 之后 | 记录压缩状态，下次重新查询 |
| `before_reset` | /reset 之前 | 保存最近 3 条用户消息为记忆 |
| `agent_end` | Agent 结束时 | 自动保存助手指回复（如果内容足够） |

---

## 八、FAQ

**Q: 插件加载了但显示 unavailable？**
A: 以日志为准，检查是否有 `Server mode (v1alpha2)` 等成功信号。

**Q: searchTimeoutMs 和 defaultTimeoutMs 区别？**
A: searchTimeoutMs 用于搜索/召回；defaultTimeoutMs 用于注册/存储/更新/删除。

**Q: 多 Agent 如何共享记忆？**
A: 多个 OpenClaw 实例使用同一个 apiKey，即可共享同一块记忆池。

---

## 九、相关链接

| 资源 | 地址 |
|------|------|
| 官方主页 | https://mem9.ai/openclaw-memory |
| GitHub | https://github.com/mem9-ai/mem9 |
| OpenClaw 插件源码 | https://github.com/mem9-ai/mem9/tree/main/openclaw-plugin |
| 管理后台 | https://mem9.ai/your-memory/ |

---

*整理自：mem9.ai 官方文档 + GitHub README*
*整理日期：2026-04-22*
