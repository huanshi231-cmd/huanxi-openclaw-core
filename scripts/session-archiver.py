#!/usr/bin/env python3
import os
import json
import glob
from datetime import datetime

AGENT_ID = "system"
SESSION_DIR = f"/Users/huanxi/.openclaw/agents/{AGENT_ID}/sessions"
MEMORY_DIR = "/Users/huanxi/.openclaw/workspace-system/memory"
TODAY = datetime.now().strftime("%Y-%m-%d")
ARCHIVE_FILE = f"{MEMORY_DIR}/{TODAY}.md"

# Find today's session files
today_files = sorted(glob.glob(f"{SESSION_DIR}/*.jsonl"), 
                     key=os.path.getmtime, reverse=True)

if not today_files:
    print(f"[{datetime.now()}] No session files today")
    exit(0)

print(f"Found {len(today_files)} session files")

# Init file
if not os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, 'w') as f:
        f.write(f"# {TODAY} 工作日志\n\n## 记录\n")

lines_added = []
for filepath in today_files[:5]:  # Last 5 sessions
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    d = json.loads(line.strip())
                    if d.get('type') != 'message':
                        continue
                    msg = d.get('message', {})
                    if msg.get('role') != 'user':
                        continue
                    content_list = msg.get('content', [])
                    if not content_list:
                        continue
                    text = content_list[0].get('text', '')
                    if not text:
                        continue
                    # Extract user message
                    for l in text.split('\n'):
                        l = l.strip()
                        if l.startswith('施欢:'):
                            snippet = l[3:].strip()[:200]
                            if snippet and len(snippet) > 5:
                                lines_added.append(f"- {snippet}")
                            break
                except:
                    continue
    except:
        continue

# Dedupe and append
if lines_added:
    unique = sorted(set(lines_added))
    with open(ARCHIVE_FILE, 'a') as f:
        for line in unique:
            f.write(line + '\n')
    print(f"Added {len(unique)} lines to {ARCHIVE_FILE}")
else:
    print("No content extracted")

print(f"[{datetime.now()}] Archive complete")
