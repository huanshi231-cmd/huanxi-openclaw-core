#!/usr/bin/env python3
"""每天汇总所有分身的对话到共享飞书文档"""
import os
import json
import glob
import subprocess
from datetime import datetime

FEISHU_TOKEN_FILE = os.path.expanduser("~/.openclaw/feishu_tokens.json")
SHARED_DOC_ID = "FtuZdG7gLoDEQvxgdM5cGMsqnVb"
MEMORY_DIR = "/Users/huanxi/.openclaw/workspace-system/memory"
TODAY = datetime.now().strftime("%Y-%m-%d")

AGENTS = ["main", "neirong", "linggangshenghuo", "liaoyuyewu", "system"]

def get_token():
    """获取飞书access token"""
    try:
        with open(FEISHU_TOKEN_FILE) as f:
            tokens = json.load(f)
        return tokens.get("system", {}).get("access_token", "")
    except:
        return ""

def extract_user_messages(session_file):
    """从session文件中提取用户消息"""
    messages = []
    try:
        with open(session_file, 'r') as f:
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
                    for l in text.split('\n'):
                        l = l.strip()
                        if l.startswith('施欢:'):
                            snippet = l[3:].strip()[:200]
                            if snippet and len(snippet) > 5:
                                messages.append(snippet)
                            break
                except:
                    continue
    except:
        pass
    return messages

def get_today_sessions(agent_id):
    """获取某分身今日的session文件"""
    session_dir = f"/Users/huanxi/.openclaw/agents/{agent_id}/sessions"
    today_files = []
    if os.path.exists(session_dir):
        for f in glob.glob(f"{session_dir}/*.jsonl"):
            mt = os.path.getmtime(f)
            dt = datetime.fromtimestamp(mt)
            if dt.strftime("%Y-%m-%d") == TODAY:
                today_files.append(f)
    return today_files

def append_to_feishu_doc(token, content_blocks):
    """通过飞书API追加内容到文档"""
    import urllib.request
    
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{SHARED_DOC_ID}/blocks/{SHARED_DOC_ID}/children"
    
    payload = json.dumps({
        "children": content_blocks,
        "index": -1
    }).encode()
    
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"Feishu API error: {e}")
        return None

def main():
    token = get_token()
    if not token:
        print("No Feishu token, saving locally instead")
        token = None
    
    # 汇总各分身今日内容
    summary_lines = []
    summary_lines.append(f"## {TODAY} 全局记忆汇总\n")
    
    for agent_id in AGENTS:
        sessions = get_today_sessions(agent_id)
        if not sessions:
            continue
        
        all_msgs = []
        for sf in sessions:
            all_msgs.extend(extract_user_messages(sf))
        
        if all_msgs:
            unique = sorted(set(all_msgs))[:20]  # 去重，最多20条
            summary_lines.append(f"### {agent_id}\n")
            for msg in unique:
                summary_lines.append(f"- {msg}")
            summary_lines.append("")
    
    # 追加到今日memory文件
    daily_file = f"{MEMORY_DIR}/{TODAY}.md"
    with open(daily_file, 'a') as f:
        f.write("\n## 全局记忆汇总\n")
        f.write("\n".join(summary_lines))
    
    print(f"Summary written to {daily_file}")
    print("\n".join(summary_lines[:10]))
    
    # 如果有token，也尝试写到飞书文档
    if token:
        blocks = []
        for line in summary_lines:
            if line.startswith('## '):
                blocks.append({"block_type": 3, "heading1": {"elements": [{"type": "text_run", "text_run": {"content": line[3:]}}]}})
            elif line.startswith('### '):
                blocks.append({"block_type": 4, "heading2": {"elements": [{"type": "text_run", "text_run": {"content": line[4:]}}]}})
            elif line.startswith('- '):
                blocks.append({"block_type": 2, "bullet": {"elements": [{"type": "text_run", "text_run": {"content": line[2:]}}]}})
        
        if blocks:
            result = append_to_feishu_doc(token, blocks)
            if result:
                print("Feishu doc updated")

if __name__ == "__main__":
    main()
