#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 完整自动化版
1. 读取本地文本
2. 按主题匹配本地图片，上传到微信（封面用media_id，正文用url）
3. 自动排版（段落+图片穿插）
4. 推送到草稿箱
"""
import os, re, sys, json, requests
from pathlib import Path

sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
from sanitize_wechat_html import sanitize_text

# 本地图片库（按主题分类）
IMAGE_LIB = {
    '情绪': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_13_light_glow.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_12_light_energy.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
    ],
    '疗愈': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_01_crystal_energy.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_19_nature_peace.jpg',
    ],
    '塔罗': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_10_stars_sky.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_11_chakra_symbols.jpg',
    ],
    '星座': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_10_stars_sky.jpg',
    ],
    'default': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
    ]
}

# 默认封面图
DEFAULT_COVER = '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_aquarius_cover.jpg'

def ensure_utf8_content(text):
    if not text: return text
    def decode_u4(m): return chr(int(m.group(1), 16))
    text = re.sub(r"\\u([0-9a-fA-F]{4})", decode_u4, text)
    text = re.sub(r"\\U([0-9a-fA-F]{8})", decode_u4, text)
    return text

def get_token():
    appid = os.environ.get("WECHAT_APPID") or os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APPSECRET") or os.environ.get("WECHAT_APP_SECRET")
    s = requests.Session(); s.trust_env = False
    r = s.get("https://api.weixin.qq.com/cgi-bin/token", params={"grant_type": "client_credential", "appid": appid, "secret": secret}, timeout=60)
    return s, r.json().get("access_token")

def upload_image(s, token, path):
    """上传图片到微信永久素材，返回media_id和url"""
    if not os.path.exists(path): return None, None
    with open(path, "rb") as f:
        files = {"media": (Path(path).name, f, "image/jpeg")}
        r = s.post(f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image", files=files, timeout=60)
    result = r.json()
    if "media_id" in result:
        return result.get("media_id"), result.get("url")
    return None, None

def select_images(keyword, count=3):
    """根据关键词选择匹配的图片"""
    for k, paths in IMAGE_LIB.items():
        if k in keyword:
            return [p for p in paths if os.path.exists(p)][:count]
    return [p for p in IMAGE_LIB['default'] if os.path.exists(p)][:count]

def build_html(title, text_content, wx_urls):
    """构建带排版的HTML：标题+段落+图片穿插"""
    # 清理标题
    title_html = f'<h1 style="font-size:22px;font-weight:bold;margin:20px 0;text-align:center;">{title}</h1>'
    
    # 分段
    paragraphs = text_content.split('\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    body_html = ''
    img_idx = 0
    
    for i, para in enumerate(paragraphs):
        # 每段用 <p> 包裹
        body_html += f'<p style="font-size:16px;line-height:1.8;margin:12px 0;text-indent:2em;">{para}</p>'
        
        # 每2段插一张图（如果还有图片可用）
        if (i + 1) % 2 == 0 and img_idx < len(wx_urls):
            body_html += f'<p style="text-align:center;margin:16px 0;"><img src="{wx_urls[img_idx]}" style="width:80%;max-width:400px;border-radius:8px;" /></p>'
            img_idx += 1
    
    return title_html + body_html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_full.py <title> <text_file> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    digest = sys.argv[3]
    
    # 读取文本
    with open(html_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败")
        sys.exit(1)
    
    # 1. 上传封面图，获取media_id
    cover_path = DEFAULT_COVER if os.path.exists(DEFAULT_COVER) else None
    if cover_path:
        thumb_id, _ = upload_image(s, token, cover_path)
    else:
        thumb_id = None
    print(f"封面media_id: {thumb_id}")
    
    # 2. 选择并上传正文图片
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url:
            wx_urls.append(url)
            print(f"正文图片URL: {url}")
    
    # 3. 构建HTML
    content = build_html(title, text, wx_urls)
    content = sanitize_text(content)
    content = ensure_utf8_content(content)
    title_utf8 = ensure_utf8_content(title)
    digest_utf8 = ensure_utf8_content(digest)
    
    # 4. 构建payload
    article = {
        "title": title_utf8,
        "author": "欢喜",
        "digest": digest_utf8,
        "content": content,
        "content_source_url": "",
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if thumb_id:
        article["thumb_media_id"] = thumb_id
    
    payload = {"articles": [article]}
    
    # 5. 推送
    print(f"推送草稿: {title_utf8}")
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
