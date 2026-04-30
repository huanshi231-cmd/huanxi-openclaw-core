# 跨Agent记忆同步问题 - 待系统分身处理

## 问题描述
当前 cross-agent-memory-sync.py 只在每天 23:25 同步一次，导致白天各Agent之间上下文丢失。施欢需要重复说很多遍同样的内容。

## 已确认的现状
1. `cross-agent-memory-sync.py` 已安装且配置正确
2. cron 配置：
   - 30 * * * * sync-shared-memory.sh（每小时同步共享记忆到本地）
   - 25 23 * * * cross-agent-memory-sync.py（每天23:25汇总到飞书）
   - 35 23 * * * system生成日工作总结
3. 同步频率太低，白天各Agent无法实时共享对话上下文

## 需要处理的方向

### 方案1：提高同步频率
- 把 sync-shared-memory.sh 改成更频繁的执行（比如每15-30分钟）
- 或者在每次对话后触发一次轻量同步

### 方案2：实时共享记忆
- 每个Agent每次被唤醒时，主动读取其他分身的最新memory/latest.md
- 需要在Agent的启动流程里加入"读取共享memory"的步骤

## 施欢的期望
- 不需要重复说同样的话
- 一个Agent说过的事情，其他Agent能立刻知道
- 希望这个问题能真正解决，不是凑合

## 任务要求
1. 评估两个方案的可行性
2. 选择或组合一个方案实施
3. 实施后验证效果
4. 回传给施欢和主控

## 参考信息
- 共享飞书文档ID：FtuZdG7gLoDEQvxgdM5cGMsqnVb
- 共享memory目录：/Users/huanxi/.openclaw/workspace-system/memory/shared
- 各分身workspace：
  - main: ~/.openclaw/workspace
  - neirong: ~/.openclaw/workspace-shortvideo
  - linggangshenghuo: ~/.openclaw/workspace-linggangshenghuo
  - liaoyuyewu: ~/.openclaw/workspace-liaoyuyewu
  - system: ~/.openclaw/workspace-system
