#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - v7 正式版
- 精美排版：段落+图片穿插+间距+圆角
- 自动选图：主题匹配+不重复
- 一次完成推送
"""
import os, re, sys, json, requests
from pathlib import Path

sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
from sanitize_wechat_html import sanitize_text

IMAGE_LIB = {
    '情绪': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_13_light_glow.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_12_light_energy.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_15_flower_nature.jpg',
    ],
    '疗愈': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_01_crystal_energy.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_19_nature_peace.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_20_starry_night.jpg',
    ],
    '塔罗': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_10_stars_sky.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_11_chakra_symbols.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
    ],
    '星座': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_07_milky_way.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_10_stars_sky.jpg',
    ],
    'default': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_19_nature_peace.jpg',
    ]
}

DEFAULT_COVER = '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_aquarius_cover.jpg'

def get_token():
    appid = os.environ.get("WECHAT_APPID") or os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APPSECRET") or os.environ.get("WECHAT_APP_SECRET")
    s = requests.Session(); s.trust_env = False
    r = s.get("https://api.weixin.qq.com/cgi-bin/token", params={"grant_type": "client_credential", "appid": appid, "secret": secret}, timeout=60)
    return s, r.json().get("access_token")

def upload_image(s, token, path):
    if not os.path.exists(path): return None, None
    with open(path, "rb") as f:
        files = {"media": (Path(path).name, f, "image/jpeg")}
        r = s.post(f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image", files=files, timeout=60)
    result = r.json()
    if "media_id" in result:
        return result.get("media_id"), result.get("url")
    return None, None

def select_images(keyword, count=3):
    import hashlib
    seed = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16)
    matched = []
    for k, paths in IMAGE_LIB.items():
        if k in keyword:
            matched.extend([p for p in paths if os.path.exists(p)])
    if not matched:
        for paths in IMAGE_LIB.values():
            matched.extend([p for p in paths if os.path.exists(p)])
    seen = set()
    result = []
    for i in range(count):
        idx = (seed + i * 3) % len(matched)
        if matched[idx] not in seen:
            seen.add(matched[idx])
            result.append(matched[idx])
    return result[:count]

def process_html_input(html, wx_urls):
    """
    处理已经是HTML格式的输入
    1. 清理原有img标签（替换src或删除）
    2. 在每个</h2>后面插入一张新图片
    """
    # 删除原有的img标签
    html = re.sub(r'<img[^>]*>', '', html)
    
    # 删除data-src属性
    html = re.sub(r'\s*data-src="[^"]*"', '', html)
    
    img_idx = 0
    def insert_after_h2(m):
        nonlocal img_idx
        tag = m.group(0)
        if img_idx < len(wx_urls):
            img_tag = f'</p><p style="text-align:center;margin:24px 0;"><img src="{wx_urls[img_idx]}" style="width:90%;max-width:520px;border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,0.1);" /></p><p>'
            img_idx += 1
            return tag + img_tag
        return tag
    
    # 在每个</h2>后插入图片
    html = re.sub(r'</h2>', insert_after_h2, html)
    
    return html

def process_markdown_input(text, wx_urls):
    """
    处理Markdown格式输入
    转换为精美HTML
    """
    # 清理markdown
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    
    # 分割段落
    lines = text.split('\n')
    paragraphs = []
    current = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                paragraphs.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append('\n'.join(current))
    
    # 构建HTML
    html = '<h1 style="font-size:24px;font-weight:bold;text-align:center;margin:30px 0 20px;line-height:1.4;color:#333;">{title}</h1>'
    
    img_idx = 0
    for i, para in enumerate(paragraphs):
        margin_top = '28px' if i > 0 else '20px'
        html += f'<p style="font-size:17px;line-height:2;margin:{margin_top} 0;text-indent:2em;color:#444;">{para}</p>'
        
        if (i + 1) % 2 == 0 and img_idx < len(wx_urls):
            html += f'<p style="text-align:center;margin:24px 0;"><img src="{wx_urls[img_idx]}" style="width:90%;max-width:520px;border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,0.1);" /></p>'
            img_idx += 1
    
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_v7.py <title> <input_file> <digest>")
        print("input_file: 支持.html或.md格式")
        sys.exit(1)
    
    title = sys.argv[1]
    input_file = sys.argv[2]
    digest = sys.argv[3]
    
    with open(input_file, "r", encoding="utf-8") as f:
        raw = f.read()
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败")
        sys.exit(1)
    
    # 封面上传
    cover_id, _ = upload_image(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    print(f"封面: {cover_id[:30] if cover_id else '无'}...")
    
    # 上传正文图片
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=4)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url:
            wx_urls.append(url)
            print(f"图片: {Path(p).name}")
    
    # 根据输入格式处理
    if input_file.endswith('.html'):
        content = process_html_input(raw, wx_urls)
    else:
        content = process_markdown_input(raw, wx_urls)
        content = content.format(title=title)
    
    content = sanitize_text(content)
    
    # 推送
    article = {
        "title": title,
        "author": "欢喜",
        "digest": digest,
        "content": content,
        "content_source_url": "",
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if cover_id:
        article["thumb_media_id"] = cover_id
    
    payload = {"articles": [article]}
    r = s.post(
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60
    )
    result = r.json()
    if "media_id" in result:
        print(f"SUCCESS:{result['media_id']}")
    else:
        print(f"FAIL:{result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
