#!/bin/bash
# 自愈脚本 - 自动捕获错误并更新规则

ERROR_LOG="$1"
LESSON="$2"

if [ -z "$ERROR_LOG" ] || [ -z "$LESSON" ]; then
    echo "用法: self_heal.sh \"错误日志\" \"教训总结\""
    exit 1
fi

FEEDBACK_FILE="$HOME/.openclaw/workspace-system/memory/feedback.md"

# 追加到 feedback.md
cat >> "$FEEDBACK_FILE" << LESSON_BLOCK

**[教训自动捕获]** $(date '+%Y-%m-%d')
错误: $ERROR_LOG
教训: $LESSON
LESSON_BLOCK

echo "已写入 feedback.md"
