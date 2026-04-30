#!/bin/bash
# Dreaming脚本 - 记忆蒸馏与评分
# 每周日02:00自动运行

DATE=$(date '+%Y-%m-%d')
MEMORY_DIR="$HOME/.openclaw/workspace-system/memory/diary"
LEARNINGS_DIR="$HOME/.openclaw/workspace-system/.learnings"
LOG_FILE="$HOME/.openclaw/logs/dreaming.log"

echo "[$DATE] === Dreaming开始 ===" >> $LOG_FILE

# 获取本周的日记文件
WEEK_FILES=$(find $MEMORY_DIR -name "*.md" -mtime -7 2>/dev/null)
FILE_COUNT=$(echo "$WEEK_FILES" | wc -l)

echo "[$DATE] 本周共 $FILE_COUNT 个日记文件" >> $LOG_FILE

# 统计高分内容
HIGH_SCORE_COUNT=0

# 这里可以加入评分逻辑
# 规则：包含"教训"、"改进"、"最佳实践"等关键词的得高分

for file in $WEEK_FILES; do
    # 检查是否有高价值内容
    if grep -q "教训\|改进\|最佳实践\|成功\|错误" "$file" 2>/dev/null; then
        HIGH_SCORE_COUNT=$((HIGH_SCORE_COUNT + 1))
        echo "  高价值文件: $(basename $file)" >> $LOG_FILE
    fi
done

echo "[$DATE] 发现 $HIGH_SCORE_COUNT 个高价值记录" >> $LOG_FILE
echo "[$DATE] === Dreaming完成 ===" >> $LOG_FILE
echo "[$DATE] Dreaming完成：$HIGH_SCORE_COUNT 个高价值记录待处理" >> $LOG_FILE

