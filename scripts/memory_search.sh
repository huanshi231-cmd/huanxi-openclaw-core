#!/bin/bash
# 统一记忆搜索脚本
# 用法: bash memory_search.sh "关键词"

QUERY="$1"
if [ -z "$QUERY" ]; then
    echo "用法: memory_search.sh \"关键词\""
    exit 1
fi

echo "=== 搜索结果 ==="
echo ""

echo "--- 最新日记 ---"
grep -r "$QUERY" ~/.openclaw/workspace-system/memory/diary/*.md 2>/dev/null | head -5

echo ""
echo "--- Shared ---"
grep -r "$QUERY" ~/.openclaw/workspace-system/memory/shared/*.md 2>/dev/null | head -5

echo ""
echo "--- Feedback ---"
grep -r "$QUERY" ~/.openclaw/workspace-system/memory/feedback.md 2>/dev/null | head -5

echo ""
echo "--- Skills Pool ---"
grep -r "$QUERY" ~/.openclaw/workspace-system/skills/*/SKILL.md 2>/dev/null | head -5
