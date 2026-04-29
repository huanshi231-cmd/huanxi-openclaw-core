#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 最终版 v11
使用xiaohu-format排版 + 3张图片 + emoji支持
"""
import os, re, sys, json, requests, subprocess
from pathlib import Path

IMGS = {
    '情绪': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_13_light_glow.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_15_flower_nature.jpg'],
    '疗愈': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_01_crystal_energy.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_19_nature_peace.jpg'],
    '塔罗': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_10_stars_sky.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_11_chakra_symbols.jpg'],
    '星座': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_07_milky_way.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg'],
    'default': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_19_nature_peace.jpg']
}
DEFAULT_COVER = '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_aquarius_cover.jpg'

def get_token():
    appid = os.environ.get("WECHAT_APPID") or os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APPSECRET") or os.environ.get("WECHAT_APP_SECRET")
    s = requests.Session(); s.trust_env = True
    r = s.get("https://api.weixin.qq.com/cgi-bin/token", params={"grant_type": "client_credential", "appid": appid, "secret": secret}, timeout=60)
    return s, r.json().get("access_token")

def upload(s, token, path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f:
        files = {"media": (Path(path).name, f, "image/jpeg")}
        r = s.post(f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image", files=files, timeout=60)
    result = r.json()
    return result.get("media_id"), result.get("url")

def select_imgs(keyword, count=3):
    import hashlib
    seed = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16)
    matched = []
    for k, paths in IMGS.items():
        if k in keyword: matched.extend([p for p in paths if os.path.exists(p)])
    if not matched:
        for paths in IMGS.values(): matched.extend([p for p in paths if os.path.exists(p)])
    seen = set(); result = []
    for i in range(count):
        idx = (seed + i * 3) % max(len(matched), 1)
        if matched[idx] not in seen: seen.add(matched[idx]); result.append(matched[idx])
    return result[:count]

def html_to_md(html):
    """HTML转Markdown"""
    md = []
    html = re.sub(r'<img[^>]*>', '', html)
    for line in html.split('\n'):
        line = line.strip()
        if not line: continue
        if m := re.match(r'<h1[^>]*>(.*?)</h1>', line, re.DOTALL): md.append(f"# {m.group(1)}\n"); continue
        if m := re.match(r'<h2[^>]*>(.*?)</h2>', line, re.DOTALL): md.append(f"## {m.group(1)}\n"); continue
        if m := re.match(r'<p[^>]*>(.*?)</p>', line, re.DOTALL):
            c = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', m.group(1))
            c = re.sub(r'<[^>]+>', '', c)
            md.append(f"{c}\n"); continue
        clean = re.sub(r'<[^>]+>', '', line)
        if clean.strip(): md.append(f"{clean}\n")
    return '\n'.join(md)

def add_emoji(text):
    emojis = ['🌙', '💜', '🌸', '✨', '💧', '🔔', '🌿', '🦋']
    lines = text.split('\n'); idx = 0
    result = []
    for line in lines:
        if line.startswith('## '):
            line = f"## {emojis[idx % len(emojis)]} {line[3:]}"; idx += 1
        result.append(line)
    return '\n'.join(result)

def insert_imgs(html, urls):
    if not urls: return html
    tag = lambda u: f'<p style="text-align:center;margin:24px 0;"><img src="{u}" style="width:100%;max-width:520px;border-radius:10px;" /></p>'
    h1 = html.find('<h1'); p = html.find('<p')
    start = min(x for x in [h1, p] if x >= 0)
    if len(urls) >= 3:
        html = html[:start] + tag(urls[0]) + html[start:]
        html += tag(urls[2])
        mid = len(html) // 2
        html = html[:mid] + tag(urls[1]) + html[mid:]
    elif len(urls) == 2:
        html = html[:start] + tag(urls[0]) + html[start:]
        html += tag(urls[1])
    elif urls:
        html = html[:start] + tag(urls[0]) + html[start:]
    return html

def sanitize(html):
    sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
    from sanitize_wechat_html import sanitize_text
    return sanitize_text(html)

def main():
    if len(sys.argv) < 4:
        print("用法: python3 push_article.py <标题> <输入文件> <摘要> [主题]"); sys.exit(1)
    
    title, input_file, digest, theme = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "coffee-house"
    
    # 读取输入
    with open(input_file, "r", encoding="utf-8") as f: raw = f.read()
    
    # 转Markdown
    md = html_to_md(raw)
    md = add_emoji(md)
    
    md_file = "/tmp/wechat-push/article.md"
    os.makedirs("/tmp/wechat-push", exist_ok=True)
    with open(md_file, "w", encoding="utf-8") as f: f.write(md)
    
    # 排版
    subprocess.run(['python3', '/Users/huanxi/.openclaw/workspace-neirong/skills/xiaohu-wechat-format/scripts/format.py', '--input', md_file, '--theme', theme, '--no-open'], capture_output=True, timeout=120)
    
    # 读取格式化HTML
    preview = "/tmp/wechat-format/article/preview.html"
    if not os.path.exists(preview): print("FAIL: 排版失败"); sys.exit(1)
    with open(preview, "r", encoding="utf-8") as f: formatted = f.read()
    
    # 提取section
    idx1 = formatted.find('id="articleContent"')
    if idx1 < 0: idx1 = formatted.find('class="article-content"')
    s_start = formatted.find('<section', idx1) if idx1 > 0 else formatted.find('<section')
    s_end = formatted.find('</section>', s_start)
    article = formatted[s_start:s_end+10] if s_start > 0 and s_end > s_start else formatted
    
    s, token = get_token()
    if not token: print("FAIL: token"); sys.exit(1)
    
    # 封面
    cover_id, _ = upload(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    print(f"封面: {cover_id[:30] if cover_id else '无'}...")
    
    # 图片
    img_paths = select_imgs(title + ' ' + digest, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload(s, token, p)
        if url: wx_urls.append(url); print(f"图: {Path(p).name}")
    
    # 插入图片
    if wx_urls: article = insert_imgs(article, wx_urls)
    
    # 清洗
    content = sanitize(article)
    
    # 推送 - 用json参数
    article_payload = {"title": title, "author": "欢喜", "digest": digest, "content": content, "content_source_url": "", "need_open_comment": 1, "only_fans_can_comment": 0}
    if cover_id: article_payload["thumb_media_id"] = cover_id
    
    r = s.post(f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}", json={"articles": [article_payload]}, timeout=60)
    result = r.json()
    if result.get("media_id"): print(f"SUCCESS:{result['media_id']}")
    else: print(f"FAIL:{result}"); sys.exit(1)

if __name__ == "__main__": main()
