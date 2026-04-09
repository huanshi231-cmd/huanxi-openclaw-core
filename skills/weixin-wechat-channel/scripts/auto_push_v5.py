#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 完整自动化版 v5
修复：乱码+markdown清理+图片src+主题匹配
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

def clean_markdown(text):
    """清理markdown标记，转换为纯文本"""
    # 标题标记
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # 粗体 **text** 或 __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    # 斜体 *text* 或 _text_
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    # 行内代码 `code`
    text = re.sub(r'`(.+?)`', r'\1', text)
    # 链接 [text](url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # 图片
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    # 引用 >
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    # 分割线 ---
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    return text

def build_html(title, text_content, wx_urls):
    """构建带排版的HTML"""
    # 标题
    html = f'<h1 style="font-size:22px;font-weight:bold;margin:20px 0;text-align:center;line-height:1.4;">{title}</h1>'
    
    # 分割段落
    paragraphs = text_content.split('\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    img_idx = 0
    for i, para in enumerate(paragraphs):
        # 段前空隙
        margin_top = '24px' if i == 0 else '12px'
        # 正文段落：首行缩进
        html += f'<p style="font-size:16px;line-height:1.9;margin:{margin_top} 0;text-indent:2em;">{para}</p>'
        
        # 每2段插一张图片
        if (i + 1) % 2 == 0 and img_idx < len(wx_urls):
            html += f'<p style="text-align:center;margin:20px 0;"><img src="{wx_urls[img_idx]}" style="width:85%;max-width:480px;border-radius:12px;display:inline-block;" /></p>'
            img_idx += 1
    
    return html

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
    """根据关键词选择匹配的图片，每次选不同的（轮换）"""
    import hashlib
    # 用关键词hash来决定起始索引，避免每次都选同样的图
    seed = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16)
    
    matched = []
    for k, paths in IMAGE_LIB.items():
        if k in keyword:
            matched.extend([p for p in paths if os.path.exists(p)])
    
    if not matched:
        matched = [p for p in IMAGE_LIB['default'] if os.path.exists(p)]
    
    # 轮换选择，避免每次都用同样的图
    result = []
    for i in range(count):
        idx = (seed + i) % len(matched)
        if matched[idx] not in result:
            result.append(matched[idx])
    
    return result[:count]

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_v5.py <title> <text_file> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    digest = sys.argv[3]
    
    # 读取文本
    with open(html_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 清理markdown标记
    text = clean_markdown(text)
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败")
        sys.exit(1)
    
    # 封面
    cover_id, _ = upload_image(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    print(f"封面media_id: {cover_id}")
    
    # 正文图片 - 根据主题选不同的图
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url:
            wx_urls.append(url)
            print(f"图片: {Path(p).name} -> {url[:60]}...")
    
    # 构建HTML
    content = build_html(title, text, wx_urls)
    content = sanitize_text(content)
    
    # payload
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
