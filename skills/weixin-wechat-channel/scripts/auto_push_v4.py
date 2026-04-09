#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re, json, requests
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
    text = re.sub(r'\\u([0-9a-fA-F]{4})', decode_u4, text)
    text = re.sub(r'\\U([0-9a-fA-F]{8})', decode_u4, text)
    return text

def get_token():
    appid = os.environ.get('WECHAT_APPID') or os.environ.get('WECHAT_APP_ID')
    secret = os.environ.get('WECHAT_APPSECRET') or os.environ.get('WECHAT_APP_SECRET')
    r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params={'grant_type': 'client_credential', 'appid': appid, 'secret': secret}, timeout=60)
    return r.json().get('access_token')

def add_material(image_path, token):
    if not os.path.exists(image_path): return None
    with open(image_path, 'rb') as f:
        files = {'media': (Path(image_path).name, f, 'image/jpeg')}
        r = requests.post(f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image', files=files, timeout=60)
    result = r.json()
    if 'url' in result: return result.get('url')
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

def push(title, html_file, digest, thumb_media_id=None):
    s = requests.Session(); s.trust_env = False
    token = get_token()
    if not token: print('FAIL: token获取失败'); return False
    
    with open(html_file, 'r', encoding='utf-8') as f: text = f.read()
    
    keyword = title + ' ' + digest
    img_paths = select_imgs(keyword)
    wx_urls = []
    for p in img_paths:
        url = add_material(p, token)
        if url: wx_urls.append(url)
    
    content = build_html(title, text, wx_urls)
    content = sanitize_text(content)
    title = ensure_utf8_content(title)
    digest = ensure_utf8_content(digest)
    
    article = {
        'Title': title,
        'Author': '',
        'Digest': digest,
        'Content': content,
        'ContentSourceUrl': '',
        'NeedOpenComment': 1,
        'OnlyFansCanComment': 0,
    }
    if thumb_media_id: article['ThumbMediaId'] = thumb_media_id
    
    payload = {'Articles': [article]}
    r = s.post(f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}', data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'}, timeout=60)
    result = r.json()
    if result.get('media_id'): print(f'SUCCESS:{result["media_id"]}'); return True
    else: print(f'FAIL:{result}'); return False

if __name__ == '__main__':
    if len(sys.argv) < 4: print('用法: python3 auto_push_v4.py <title> <text_file> <digest> [thumb_media_id]'); sys.exit(1)
    push(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
