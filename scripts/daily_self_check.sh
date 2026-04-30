#!/bin/bash
# 每日自检脚本 - 每天08:00执行

DATE=$(date '+%Y-%m-%d')
LOG="$HOME/.openclaw/logs/daily-self-check.log"

echo "[$DATE] === 每日自检开始 ===" >> $LOG

# 1. 核心文件完整性
echo "[$DATE] 1. 核心文件检查:" >> $LOG
for f in SOUL.md USER.md IDENTITY.md AGENTS.md SELF_CONTROL.md; do
    if [ -f "$HOME/.openclaw/workspace-system/$f" ]; then
        echo "  ✅ $f" >> $LOG
    else
        echo "  ❌ $f 缺失" >> $LOG
    fi
done

# 2. Scripts完整性
echo "[$DATE] 2. Scripts检查:" >> $LOG
SCRIPT_COUNT=$(ls $HOME/.openclaw/workspace-system/scripts/*.sh 2>/dev/null | wc -l)
echo "  脚本数量: $SCRIPT_COUNT" >> $LOG

# 3. 昨日教训检查
echo "[$DATE] 3. 教训记录:" >> $LOG
YESTERDAY=$(date -v-1d '+%Y-%m-%d')
if [ -f "$HOME/.openclaw/workspace-system/.learnings/errors/$YESTERDAY.md" ]; then
    echo "  ⚠️ 昨日有错误记录" >> $LOG
else
    echo "  ✅ 无错误" >> $LOG
fi

# 4. Cron任务状态
echo "[$DATE] 4. Cron任务:" >> $LOG
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | wc -l)
echo "  已配置: $CRON_COUNT 个" >> $LOG

# 5. 磁盘空间
echo "[$DATE] 5. 磁盘空间:" >> $LOG
DISK=$(df -h / | tail -1 | awk '{print $5}')
echo "  使用: $DISK" >> $LOG

echo "[$DATE] === 每日自检完成 ===" >> $LOG
echo "" >> $LOG

