#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 完整自动化（排版+图片）
"""
import os, re, sys, json, requests
from pathlib import Path

sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
from sanitize_wechat_html import sanitize_text

IMAGE_LIB = {
    '情绪': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_13_light_glow.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg'],
    '疗愈': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_01_crystal_energy.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg'],
    '塔罗': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_11_chakra_symbols.jpg'],
    'default': ['/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg', '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg']
}

def ensure_utf8_content(text):
    if not text: return text
    def decode_u4(m): return chr(int(m.group(1), 16))
    text = re.sub(r"\\u([0-9a-fA-F]{4})", decode_u4, text)
    text = re.sub(r"\\U([0-9a-fA-F]{8})", decode_u4, text)
    return text

def get_token(s, appid, secret):
    r = s.get("https://api.weixin.qq.com/cgi-bin/token", params={"grant_type": "client_credential", "appid": appid, "secret": secret}, timeout=60)
    return r.json().get("access_token")

def upload_img(s, token, path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f:
        files = {"media": (Path(path).name, f, "image/jpeg")}
        r = s.post(f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image", files=files, timeout=60)
    result = r.json()
    if "url" in result: return result.get("url")
    return None

def select_imgs(keyword, count=3):
    for k, paths in IMAGE_LIB.items():
        if k in keyword: return [p for p in paths if os.path.exists(p)][:count]
    return [p for p in IMAGE_LIB['default'] if os.path.exists(p)][:count]

def build_html(title, text_content, wx_urls):
    html = f'<h1>{title}</h1>'
    sections = text_content.split('\n\n')
    img_idx = 0
    for i, sec in enumerate(sections):
        if sec.strip():
            html += f'<p>{sec}</p>'
            if (i + 1) % 2 == 0 and img_idx < len(wx_urls):
                html += f'<p><img src="{wx_urls[img_idx]}" /></p>'
                img_idx += 1
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_with_images.py <title> <text_file> <digest> [thumb_media_id]")
        sys.exit(1)
    
    title = sanitize_text(sys.argv[1])
    html_file = sys.argv[2]
    digest = sanitize_text(sys.argv[3])
    thumb_media_id = sys.argv[4].strip() if len(sys.argv) > 4 else ""
    
    with open(html_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 选择并上传图片
    keyword = title + ' ' + digest
    img_paths = select_imgs(keyword)
    wx_urls = []
    s = requests.Session(); s.trust_env = False
    appid = os.environ.get("WECHAT_APPID") or os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APPSECRET") or os.environ.get("WECHAT_APP_SECRET")
    token = get_token(s, appid, secret)
    
    for p in img_paths:
        url = upload_img(s, token, p)
        if url: wx_urls.append(url)
    
    # 构建HTML
    content = build_html(title, text, wx_urls)
    content = ensure_utf8_content(content)
    title = ensure_utf8_content(title)
    digest = ensure_utf8_content(digest)
    
    article = {
        "title": title,
        "author": "",
        "digest": digest,
        "content": content,
        "content_source_url": "",
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if thumb_media_id: article["thumb_media_id"] = thumb_media_id
    
    payload = {"articles": [article]}
    print(f"推送草稿: {title}")
    r = s.post(f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}", data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"}, timeout=60)
    result = r.json()
    if "media_id" in result: print(f"SUCCESS:{result['media_id']}")
    else: print(f"FAIL:{result}"); sys.exit(1)

if __name__ == "__main__": main()
