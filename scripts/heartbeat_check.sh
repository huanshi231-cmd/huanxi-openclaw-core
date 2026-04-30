#!/bin/bash
# 心跳自检脚本 - 每10分钟执行

DATE=$(date '+%Y-%m-%d %H:%M')
LOG="$HOME/.openclaw/logs/heartbeat.log"

echo "[$DATE] === 心跳检查 ===" >> $LOG

# 1. Gateway状态
if pgrep -f "openclaw" > /dev/null 2>&1; then
    echo "[$DATE] ✅ Gateway运行中" >> $LOG
else
    echo "[$DATE] ❌ Gateway未运行，尝试重启" >> $LOG
    openclaw gateway start 2>&1 >> $LOG
fi

# 2. 磁盘空间检查
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "[$DATE] ⚠️ 磁盘使用率${DISK_USAGE}%，立即清理" >> $LOG
    # 清理临时文件
    rm -rf /tmp/page*.jpg /tmp/page*.ppm 2>/dev/null
    rm -rf /tmp/ch*.jpg /tmp/*.pdf 2>/dev/null
    echo "[$DATE] 已清理临时文件" >> $LOG
elif [ "$DISK_USAGE" -gt 80 ]; then
    echo "[$DATE] ⚠️ 磁盘使用率${DISK_USAGE}%" >> $LOG
fi

# 3. Cron任务状态
CRON_RUNS=$(crontab -l 2>/dev/null | grep -v "^#")
if [ -n "$CRON_RUNS" ]; then
    echo "[$DATE] ✅ Cron任务已配置" >> $LOG
else
    echo "[$DATE] ⚠️ 无Cron任务" >> $LOG
fi

# 4. 内存检查（如果有memory_pressure）
# macOS没有/proc，使用vm_stat
if [ "$(uname)" = "Darwin" ]; then
    VM_STAT=$(vm_stat 2>/dev/null | grep "Pages active" | awk '{print $3}' | sed 's/%//')
    # 只记录，不告警（macOS内存管理不同）
    echo "[$DATE] 内存活动页: $VM_STAT" >> $LOG
fi

# 5. 最近消息检查（检查session文件更新时间）
SESSION_FILE="$HOME/.openclaw/workspace-system/memory/diary/$(date '+%Y-%m-%d').md"
if [ -f "$SESSION_FILE" ]; then
    LAST_MODIFY=$(stat -f "%Sm" "$SESSION_FILE" 2>/dev/null | head -1)
    echo "[$DATE] 日记最后更新: $LAST_MODIFY" >> $LOG
fi

echo "[$DATE] === 心跳检查完成 ===" >> $LOG
echo "" >> $LOG

