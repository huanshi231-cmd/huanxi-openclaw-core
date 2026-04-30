# 系统配置轻触 SOP（按需）

仅当主人要你动 **网关 / 飞书路由 / 小改 `openclaw.json`** 时读；日常聊天不加载。

## 底层原则

- **先落盘再报喜**：文件已改、JSON 合法、网关已重启，才说「好了」。
- **最小改动**：只动任务需要的字段，不整份重写。
- **不代答密钥**：`.env`、AppSecret、token 不在聊天里贴全文；需要改密钥时说明「请在本机或 Cursor 里改 `.env`」。

## 允许动的文件

- `~/.openclaw/openclaw.json`（常见：`bindings`、`channels.feishu.groups`、`agents.list` 里 tools/model）

**飞书路由备忘**：仅绑「群」时，**私聊**若未匹配到 binding，会落 **默认 main**。系统机器人下需有 `match.channel=feishu` + `accountId=system` 且**不写 peer** 的一条，私聊才会进系统分身。
- 默认**不**在此流程改：`~/.openclaw/.env`（除非主人明确要求且走安全渠道）

## 最短步骤

1. `fs_read` 读现配置，定位要改的片段。
2. 用 `apply_patch` 优先；不行再用 `fs_write` 局部替换。
3. **校验 JSON**：`exec` 执行 `python3 -m json.tool /Users/huanxi/.openclaw/openclaw.json > /dev/null`；失败则回滚或停手，不报成功。
4. **重启网关**：`openclaw gateway stop`，再按环境启动（如 `openclaw gateway`）；确认本机 `18789` 在监听后再回复主人。
5. 回复用两句话：**改了什么**、**她怎么验证**（例如去哪个群发一句）。

## 红线

- 不编造「已绑定」「已重启」。
- 不做未确认的破坏性 `exec`（删库、格盘、乱杀进程）。
