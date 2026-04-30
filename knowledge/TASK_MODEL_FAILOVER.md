# 模型高可用配置问题 - 待系统分身处理

## 问题描述
2026-04-01 17:46-18:05 期间，neirong 无响应，原因：
1. MiniMax API 过载（529错误）
2. 所有 auth profile 进入冷却
3. 无有效 fallback，模型彻底不可用

## 错误日志
```
FailoverError: No available auth profile for minimax-cn (all in cooldown or unavailable)
AI service is temporarily overloaded (529)
Kimi API error (401): Invalid Authentication
Kimi API error (404): url.not_found
```

## 根因
当前 minimax-cn 没有配置多个 auth profile，导致：
- 单一 API Key 一旦进入 cooldown
- 没有任何 fallback 可以用
- 模型直接挂掉

## 需要修复
1. 为 minimax-cn 配置多个 auth profile（多个 API Key 互为备份）
2. 或者配置可靠的 fallback 模型提供商
3. 确保当主模型不可用时，自动切换到备用

## 施欢的期望
不要再出现"说一半没反应"的情况，需要真正的容错高可用

## 优先级
P0 - 影响实际使用，必须修复

---

## 额外问题：微信API IP白名单（2026-04-01 18:34新增）

**当前出口IP：** 112.43.8.28
**错误：** `invalid ip 112.43.8.28, not in whitelist`
**影响：** 无法推送微信公众号草稿箱

**需要操作：**
把 112.43.8.28 加到微信公众平台后台的 IP 白名单里

微信后台路径：设置与开发 → 基本配置 → IP白名单
