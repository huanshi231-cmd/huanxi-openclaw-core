#!/bin/bash -l
# 系统健康检查 - 每天自动运行，发现问题写入状态文件

LOG_FILE=~/.openclaw/workspace-system/memory/health-status.md
cd ~/.openclaw

echo "# 系统健康状态 — $(date '+%Y-%m-%d %H:%M')" > $LOG_FILE

# 1. 记忆搜索索引状态
echo "## 记忆搜索索引" >> $LOG_FILE
idx_status=$(openclaw memory status 2>/dev/null | grep "Dirty:" | head -1)
echo "\`$idx_status\`" >> $LOG_FILE
dirty=$(echo "$idx_status" | grep -o "Dirty: [a-z]*" | awk '{print $2}')
if [ "$dirty" = "yes" ]; then
    echo "⚠️ 索引需要重建" >> $LOG_FILE
fi

# 2. 模型状态（通过日志检测最近的 fallback）
echo "## 模型 fallback 检测" >> $LOG_FILE
recent_502=$(grep -c "502\|429\|quota" ~/.openclaw/logs/gateway.log 2>/dev/null | tail -1)
echo "近期错误请求次数: $recent_502" >> $LOG_FILE
if [ "$recent_502" -gt 0 ]; then
    echo "⚠️ 检测到 API 异常，需要检查模型配额" >> $LOG_FILE
fi

# 3. mempalace cron 执行状态
echo "## MemPalace Wake-up" >> $LOG_FILE
mp_lines=$(wc -l < ~/.openclaw/workspace-system/memory/mempalace_wakeup.md 2>/dev/null || echo "0")
echo "wakeup 文件行数: $mp_lines" >> $LOG_FILE
if [ "$mp_lines" -lt 5 ]; then
    echo "⚠️ mempalace wakeup 内容过少，检查 cron 是否正常" >> $LOG_FILE
fi

# 4. Session 配置验证
echo "## Session 配置" >> $LOG_FILE
idle=$(cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('session',{}).get('reset',{}).get('idleMinutes','未配置'))" 2>/dev/null)
echo "idle 分钟数: $idle" >> $LOG_FILE
if [ "$idle" = "未配置" ] || [ "$idle" = "1440" ]; then
    echo "⚠️ session 可能每天重置，请确认配置" >> $LOG_FILE
fi

echo "✅ 检查完成" >> $LOG_FILE
