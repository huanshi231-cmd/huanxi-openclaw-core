#!/bin/bash
AGENT_ID="system"
SESSION_DIR="/Users/huanxi/.openclaw/agents/${AGENT_ID}/sessions"
MEMORY_DIR="/Users/huanxi/.openclaw/workspace-system/memory"
TODAY=$(date +%Y-%m-%d)
ARCHIVE_FILE="${MEMORY_DIR}/${TODAY}.md"

TODAY_FILES=$(find "${SESSION_DIR}" -name "*.jsonl" -newermt "today 00:00" 2>/dev/null | sort)

if [ -z "$TODAY_FILES" ]; then
    echo "[$(date)] No session files today"
    exit 0
fi

if [ ! -f "${ARCHIVE_FILE}" ]; then
    echo "# ${TODAY} 工作日志" > "${ARCHIVE_FILE}"
    echo "" >> "${ARCHIVE_FILE}"
    echo "## 记录" >> "${ARCHIVE_FILE}"
fi

for file in ${TODAY_FILES}; do
    grep '"'"'role'"'"':"'"'user'"'"'' "${file}" 2>/dev/null | python3 -c '
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        msg = d.get('"'"'message'"'"', {})
        content_list = msg.get('"'"'content'"'"', [])
        if content_list:
            text = content_list[0].get('"'"'text'"'"', '"'"''"'"')
            if text and len(text) > 10:
                for l in text.split('"'"'
'"'"'):
                    if l.startswith('"'"'施欢:'"'"'):
                        snippet = l[3:].strip()[:200]
                        if snippet:
                            print('"'"'- '"'"' + snippet)
                        break
    except:
        pass
' >> "${ARCHIVE_FILE}.tmp 2>/dev/null
done

if [ -f "${ARCHIVE_FILE}.tmp" ]; then
    sort -u "${ARCHIVE_FILE}.tmp" >> "${ARCHIVE_FILE}"
    rm "${ARCHIVE_FILE}.tmp"
fi

echo "[$(date)] Archive complete"
