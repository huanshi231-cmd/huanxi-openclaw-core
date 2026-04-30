#!/bin/bash
# 每日工作总结生成脚本
# 路径修复 + 生成结果导向的总结

AGENT_ID="system"
MEMORY_DIR="/Users/huanxi/.openclaw/workspace-system/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)
SUMMARY_FILE="${MEMORY_DIR}/${TODAY}.md"

echo "[$(date)] 生成工作总结..."

# 结果导向的总结模板
cat > "${SUMMARY_FILE}" << EOF
# ${TODAY} 工作总结

## 今日结果

**核心完成**：（今天实际搞完的事）

**部分完成**：（做了但没完全搞定的事，原因）

**未启动**：（本来计划做但没动的事）

## 重要决策

（今天做出的关键决定和原因）

## 明日重点

（明天第一件要处理的事）

## 待跟进

（之前遗留的、需要注意的事项）
EOF

echo "✓ 工作总结已生成: ${SUMMARY_FILE}"
echo "内容:"
cat "${SUMMARY_FILE}"
