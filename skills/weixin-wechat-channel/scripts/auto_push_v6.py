#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - v6（直接处理HTML输入）
1. 读取已有HTML文件
2. 把原有图片链接替换成微信URL
3. 在合适位置插入更多图片
4. 推送到草稿箱
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
    result = []
    for i in range(count):
        idx = (seed + i * 3) % len(matched)
        if matched[idx] not in result:
            result.append(matched[idx])
    return result[:count]

def insert_images_into_html(html, wx_urls):
    """在<h2>之后段落之间插入图片"""
    if not wx_urls:
        return html
    
    img_idx = 0
    def add_img(match):
        nonlocal img_idx
        block = match.group(0)
        if img_idx < len(wx_urls):
            img_tag = f'</p><p style="text-align:center;margin:20px 0;"><img src="{wx_urls[img_idx]}" style="width:85%;max-width:480px;border-radius:12px;" /></p><p>'
            img_idx += 1
            # 在</h2>后的第一个</p>前插入图片
            return block + img_tag
        return block
    
    # 在每个</h2>标签后插入图片
    pattern = r'(</h[1-6]>)(.*?)</p>'
    
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_v6.py <title> <html_file> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    digest = sys.argv[3]
    
    # 读取HTML
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败")
        sys.exit(1)
    
    # 封面
    cover_id, _ = upload_image(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    print(f"封面media_id: {cover_id}")
    
    # 上传正文图片
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url:
            wx_urls.append(url)
            print(f"图片: {Path(p).name}")
    
    # 在</h2>后插入图片
    if wx_urls:
        html = insert_images_into_html(html, wx_urls)
    
    # 清理并推送
    content = sanitize_text(html)
    
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
    
    print(f"推送: {title}")
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
