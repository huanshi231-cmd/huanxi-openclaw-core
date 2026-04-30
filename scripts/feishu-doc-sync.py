#!/usr/bin/env python3
"""把飞书共享文档同步到本地，让所有分身都能搜到"""
import json
import os
import urllib.request
from datetime import datetime

TOKEN_FILE = os.path.expanduser("~/.openclaw/feishu_tokens.json")
LOCAL_DIR = "/Users/huanxi/.openclaw/workspace-system/memory/shared"
DOC_ID = "NVawdl01wo2LGlxlFtncvpKWnFh"

os.makedirs(LOCAL_DIR, exist_ok=True)

def get_token():
    try:
        with open(TOKEN_FILE) as f:
            tokens = json.load(f)
        return tokens.get("system", {}).get("access_token", "")
    except:
        return ""

def fetch_doc_content(token):
    """获取飞书文档纯文本内容"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            blocks = data.get("data", {}).get("blocks", [])
            text = extract_text_from_blocks(blocks)
            return text
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_blocks(blocks):
    text_parts = []
    for block in blocks:
        block_type = block.get("block_type", 0)
        # Text content is in the "text" field
        if "text" in block:
            for elem in block["text"].get("elements", []):
                for content in elem.get("text_run", {}).get("content", "").split("\n"):
                    if content.strip():
                        text_parts.append(content.strip())
    return "\n".join(text_parts)

token = get_token()
if not token:
    print("No Feishu token")
    exit(1)

content = fetch_doc_content(token)
out_file = f"{LOCAL_DIR}/shared-memory.md"
with open(out_file, "w") as f:
    f.write(f"# 全局共享记忆（同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}）\n\n")
    f.write(content)

print(f"Synced to {out_file}, {len(content)} chars")
