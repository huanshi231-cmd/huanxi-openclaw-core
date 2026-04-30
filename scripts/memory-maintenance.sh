#!/bin/bash
# 每晚23点清理脚本
# 功能：去重 + 合并碎片 + 更新索引

MEMORY_DIR="/Users/huanxi/.openclaw/workspace-system/memory"
TODAY=$(date +%Y-%m-%d)
LOG="$HOME/.openclaw/logs/maintenance.log"

log() { echo "[$(date)] $1" | tee -a "$LOG"; }

log "开始清理..."

# 1. 清理重复记忆（去重）
find "${MEMORY_DIR}" -name "*.md" -type f | while read f; do
    if [ -f "$f" ]; then
        # 提取所有行，去重，写回
        sort -u "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    fi
done
log "去重完成"

# 2. 合并碎片会话（把今日的碎片session归档到主memory文件）
SESSION_MARKER="## 会话记录"
if grep -q "$SESSION_MARKER" "${MEMORY_DIR}/${TODAY}.md" 2>/dev/null; then
    # 合并重复的会话记录段落
    awk '!seen[$0]++' "${MEMORY_DIR}/${TODAY}.md" > "${MEMORY_DIR}/${TODAY}.md.tmp" && mv "${MEMORY_DIR}/${TODAY}.md.tmp" "${MEMORY_DIR}/${TODAY}.md"
    log "碎片会话合并完成"
fi

# 3. 更新QMD索引（如果qmd命令存在）
if command -v qmd 2>/dev/null || [ -f "$HOME/.bun/bin/qmd" ]; then
    CMD="${HOME}/.bun/bin/qmd"
    "$CMD" index --path "${MEMORY_DIR}/.." 2>/dev/null && log "QMD索引更新完成" || log "QMD索引更新失败"
fi

log "清理完成"
