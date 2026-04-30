#!/bin/bash
# 周回顾脚本 - 每周日23:00执行

DATE=$(date '+%Y-%m-%d')
LOG="$HOME/.openclaw/logs/weekly-review.log"
DIARY_DIR="$HOME/.openclaw/workspace-system/memory/diary"

echo "[$DATE] === 周回顾开始 ===" >> $LOG

# 1. 统计本周日记数量
WEEK_FILES=$(find $DIARY_DIR -name "*.md" -mtime -7 2>/dev/null)
WEEK_COUNT=$(echo "$WEEK_FILES" | wc -l)
echo "[$DATE] 本周日记: $WEEK_COUNT 个" >> $LOG

# 2. 统计本周教训记录
ERROR_COUNT=$(find $HOME/.openclaw/workspace-system/.learnings/errors -name "*.md" -mtime -7 2>/dev/null | wc -l)
echo "[$DATE] 错误记录: $ERROR_COUNT 个" >> $LOG

# 3. 检查Cron任务执行情况
echo "[$DATE] Cron任务:" >> $LOG
grep "cron" $HOME/.openclaw/logs/system-health.log 2>/dev/null | tail -5 >> $LOG

# 4. 检查知识库新增
KNOWLEDGE_COUNT=$(find $HOME/.openclaw/workspace-system/knowledge -name "*.md" -mtime -7 2>/dev/null | wc -l)
echo "[$DATE] 新增知识: $KNOWLEDGE_COUNT 个" >> $LOG

# 5. 生成周报摘要
echo "[$DATE] === 周报摘要 ===" >> $LOG
echo "本周完成:" >> $LOG
echo "- 日记: $WEEK_COUNT 个" >> $LOG
echo "- 错误: $ERROR_COUNT 个" >> $LOG
echo "- 知识: $KNOWLEDGE_COUNT 个" >> $LOG

echo "[$DATE] === 周回顾完成 ===" >> $LOG
echo "" >> $LOG

# 6. 输出到施欢可见的位置
cat >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md << 'SUMMARY'
# 周总结

## 本周数据
SUMMARY

echo "| 指标 | 数值 |" >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md
echo "|------|------|" >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md
echo "| 日记 | $WEEK_COUNT 个 |" >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md
echo "| 错误 | $ERROR_COUNT 个 |" >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md
echo "| 知识 | $KNOWLEDGE_COUNT 个 |" >> $HOME/.openclaw/workspace-system/memory/weekly-summary.md

