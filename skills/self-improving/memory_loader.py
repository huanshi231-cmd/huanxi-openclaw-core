#!/usr/bin/env python3
"""
启动时记忆加载器
自动读取近7天memory，输出结构化摘要
"""
import os, datetime
from pathlib import Path

MEMORY_DIR = Path("~/.openclaw/workspace/memory").expanduser()
LONGTERM_FILE = Path("~/self-improving/memory.md").expanduser()

def load_recent_memory(days=7):
    """读取近N天所有memory文件"""
    files = sorted(MEMORY_DIR.glob("????-??-??.md"), reverse=True)[:days]
    result = []
    for f in files:
        result.append(f"## {f.stem}\n" + f.read_text(encoding="utf-8"))
    return "\n\n".join(result)

def load_longterm():
    if LONGTERM_FILE.exists():
        return LONGTERM_FILE.read_text(encoding="utf-8")
    return ""

def get_summary():
    """返回7天memory结构化摘要"""
    recent = load_recent_memory(7)
    longterm = load_longterm()
    return recent, longterm

if __name__ == "__main__":
    recent, longterm = get_summary()
    print(f"=== 启动记忆加载 ===")
    print(f"近7天memory: {len(recent)} 字符")
    print(f"长期记忆: {len(longterm)} 字符")
    print("\n最近3天memory内容预览:")
    for line in recent.split("\n")[:30]:
        print(line)
