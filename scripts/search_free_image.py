#!/usr/bin/env python3
"""从 Pexels 免 key 搜索免费图片并下载
用法: python3 search_free_image.py <关键词> [保存路径]
"""
import os, sys, requests, re, random
from pathlib import Path

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 常见主题 -> 搜索关键词
TOPIC_KEYWORDS = {
    "疗愈": "calm nature peaceful",
    "情绪": "emotional soft light portrait",
    "原生家庭": "family warm home",
    "情感": "love tender relationship",
    "自然": "nature forest ocean",
    "内心": "introspection quiet reflection",
    "成长": "growth journey path",
    "self": "calm nature peaceful",
}

def search_pexels(keyword, page=1):
    url = f"https://www.pexels.com/search/{requests.utils.quote(keyword)}/?page={page}"
    r = requests.get(url, headers=headers, timeout=20)
    urls = re.findall(r'https://images\.pexels\.com/photos/\d+/pexels-photo-\d+\.(?:jpeg|jpg)\?', r.text)
    return list(dict.fromkeys(urls))

def download_image(url, save_path):
    r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
    if r.status_code == 200 and len(r.content) > 5000:
        with open(save_path, 'wb') as f:
            f.write(r.content)
        return True
    return False

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "calm nature"
    save_dir = sys.argv[2] if len(sys.argv) > 2 else "/Users/huanxi/.openclaw/workspace-neirong/downloads/images"
    
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # 自动匹配主题关键词
    for topic, kw in TOPIC_KEYWORDS.items():
        if topic in keyword:
            search_kw = kw
            break
    else:
        search_kw = keyword
    
    print(f"搜索关键词: {search_kw}", file=sys.stderr)
    
    urls = search_pexels(search_kw)
    if not urls:
        print("未找到图片，尝试备用关键词...", file=sys.stderr)
        urls = search_pexels("nature landscape")
    
    if not urls:
        print("ERROR: 无法找到免费图片", file=sys.stderr)
        sys.exit(1)
    
    # 随机选一个，增加多样性
    selected = random.choice(urls[:20])  # 前20个里随机
    filename = f"{keyword[:20]}_{hash(selected)%10000}.jpg"
    save_path = os.path.join(save_dir, filename)
    
    print(f"下载: {selected[:80]}", file=sys.stderr)
    if download_image(selected, save_path):
        size = os.path.getsize(save_path)
        print(f"SUCCESS:{save_path}:{size}")
    else:
        print("ERROR: 下载失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
