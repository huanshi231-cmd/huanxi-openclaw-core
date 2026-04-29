#!/usr/bin/env python3
"""Learnings 历史经验检索"""
import os, sys

LEARNINGS_DIR = os.path.expanduser("~/.openclaw/workspace-main/.learnings/")

def search(keywords, max_results=5):
    results = []
    kws = [k.lower() for k in keywords]
    for fname in sorted(os.listdir(LEARNINGS_DIR)):
        if not fname.endswith(('.md', '.log', '.txt')):
            continue
        fpath = os.path.join(LEARNINGS_DIR, fname)
        try:
            with open(fpath, 'r', errors='ignore') as f:
                content = f.read()
            cl = content.lower()
            mc = sum(cl.count(k) for k in kws)
            if mc > 0:
                lines = content.split('\n')
                matched = [f"  行{i+1}: {l.strip()[:100]}" for i,l in enumerate(lines) if any(k in l.lower() for k in kws)]
                results.append({'file': fname, 'match': mc, 'preview': matched[:3]})
        except:
            pass
    results.sort(key=lambda x: x['match'], reverse=True)
    return results[:max_results]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 learnings_search.py <关键词1> [关键词2] ...")
        sys.exit(1)
    results = search(sys.argv[1:])
    if results:
        print(f"找到 {len(results)} 个相关经验：\n")
        for r in results:
            print(f"📁 {r['file']} (匹配{r['match']}次)")
            for l in r['preview']:
                print(l)
            print()
    else:
        print("未找到相关经验")
