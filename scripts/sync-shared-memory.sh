#!/bin/bash
# 系统分身每小时同步共享记忆到本地目录
# 其他分身把这个目录加入搜索范围

SHARED_DIR="/Users/huanxi/.openclaw/workspace-system/memory/shared"
MEMORY_DIR="/Users/huanxi/.openclaw/workspace-system/memory"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$SHARED_DIR"

# 收集所有分身的今日memory
{
    echo "# 全局共享记忆 - $(date '+%Y-%m-%d %H:%M')"
    echo ""
    for f in "$MEMORY_DIR"/*.md; do
        if [ -f "$f" ]; then
            echo "## $(basename $f)"
            cat "$f"
            echo ""
        fi
    done
} > "$SHARED_DIR/latest.md"

echo "[$(date)] 同步完成: $SHARED_DIR/latest.md"
