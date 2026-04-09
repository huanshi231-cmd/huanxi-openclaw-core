#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 简洁优雅版
- 开头1张图
- 中间1张图  
- 结尾1张图
- 简洁排版，不过度设计
"""
import os, re, sys, json, requests
from pathlib import Path

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

def build_html(title, text, wx_urls):
    """
    简洁排版：
    1. 标题
    2. 开头图片
    3. 前半部分文字
    4. 中间图片
    5. 后半部分文字
    6. 结尾图片
    """
    # 删除原有img标签
    text = re.sub(r'<img[^>]*>', '', text)
    text = re.sub(r'\s*data-src="[^"]*"', '', text)
    
    # 清理markdown残留
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # 按段落分割
    paragraphs = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # 处理p标签
        p_match = re.match(r'<p[^>]*>(.*?)</p>', line, re.DOTALL)
        if p_match:
            paragraphs.append(p_match.group(1))
        else:
            paragraphs.append(line)
    
    # 计算分割点
    total = len(paragraphs)
    split1 = total // 3
    split2 = total * 2 // 3
    
    # 构建HTML
    img1, img2, img3 = (wx_urls + [None]*3)[:3]
    
    html = f'''<section style="padding:0 15px;margin:0;">
<h1 style="font-size:20px;font-weight:bold;text-align:center;margin:25px 0 20px;line-height:1.6;color:#222;">{title}</h1>
'''
    
    # 开头图片
    if img1:
        html += f'<p style="text-align:center;margin:20px 0;"><img src="{img1}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    # 前三分之一
    for i, p in enumerate(paragraphs[:split1]):
        margin = '20px 0 14px' if i == 0 else '0 0 14px'
        html += f'<p style="font-size:15px;line-height:2;text-indent:2em;margin:{margin};color:#333;">{p}</p>\n'
    
    # 中间图片
    if img2:
        html += f'<p style="text-align:center;margin:25px 0;"><img src="{img2}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    # 中间三分之一
    for p in paragraphs[split1:split2]:
        html += f'<p style="font-size:15px;line-height:2;text-indent:2em;margin:0 0 14px;color:#333;">{p}</p>\n'
    
    # 结尾图片
    if img3:
        html += f'<p style="text-align:center;margin:25px 0;"><img src="{img3}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    # 后三分之一
    for p in paragraphs[split2:]:
        margin_bottom = '30px' if p == paragraphs[-1] else '14px'
        html += f'<p style="font-size:15px;line-height:2;text-indent:2em;margin:0 0 {margin_bottom};color:#333;">{p}</p>\n'
    
    html += '</section>'
    
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_clean.py <title> <text_file> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    input_file = sys.argv[2]
    digest = sys.argv[3]
    
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败")
        sys.exit(1)
    
    # 封面
    cover_id, _ = upload_image(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    print(f"封面: {cover_id[:30] if cover_id else '无'}...")
    
    # 正文图片（只选3张）
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url:
            wx_urls.append(url)
            print(f"图片: {Path(p).name}")
    
    # 构建HTML
    content = build_html(title, text, wx_urls)
    
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
