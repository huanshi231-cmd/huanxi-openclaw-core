#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 精美排版版
把没有任何样式的原文HTML，改造成带精美排版的完整HTML
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

# 全局样式配置
CSS_STYLES = """
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 17px;
    line-height: 1.9;
    color: #3a3a3a;
    background-color: #fff;
    margin: 0;
    padding: 0;
}
</style>
"""

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

def select_images(keyword, count=4):
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

def beautify_html(html, wx_urls):
    """
    把简陋的HTML改造成精美排版的完整HTML
    """
    # 先删掉所有原来的img标签（稍后我们自己加）
    html = re.sub(r'<img[^>]*>', '', html)
    html = re.sub(r'\s*data-src="[^"]*"', '', html)
    
    # 换行符统一
    html = html.replace('\r\n', '\n').replace('\r', '\n')
    
    # 构建完整页面
    page = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html, body {{ margin: 0; padding: 0; }}
.wrap {{ max-width: 680px; margin: 0 auto; padding: 20px 20px 60px; background: #fff; }}
</style>
</head>
<body>
<div class="wrap">
'''
    
    # 处理每个块
    img_idx = [0]
    lines = html.split('\n')
    buffer = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            continue
        
        # H1 - 主标题
        h1_match = re.match(r'<h1[^>]*>(.*?)</h1>', stripped, re.DOTALL)
        if h1_match:
            if buffer:
                page += apply_paragraph_styles(buffer)
                buffer = []
            title = h1_match.group(1)
            page += f'<h1 style="font-size:24px;font-weight:bold;text-align:center;color:#222;margin:30px 0 25px;padding:0;line-height:1.5;letter-spacing:1px;">{title}</h1>\n'
            continue
        
        # H2 - 小标题
        h2_match = re.match(r'<h2[^>]*>(.*?)</h2>', stripped, re.DOTALL)
        if h2_match:
            if buffer:
                page += apply_paragraph_styles(buffer)
                buffer = []
            title = h2_match.group(1)
            # 在h2后面加图片
            img_html = ''
            if img_idx[0] < len(wx_urls):
                img_html = f'<p style="text-align:center;margin:20px 0;"><img src="{wx_urls[img_idx[0]]}" style="width:100%;max-width:480px;border-radius:12px;display:inline-block;" /></p>'
                img_idx[0] += 1
            page += f'''<h2 style="font-size:19px;font-weight:bold;color:#2a5a8a;margin:35px 0 18px;padding:0 0 8px;border-bottom:2px solid #e8f0f7;line-height:1.5;">{title}</h2>
{img_html}
'''
            continue
        
        # P标签
        p_match = re.match(r'<p[^>]*>(.*?)</p>', stripped, re.DOTALL)
        if p_match:
            buffer.append(line)
            continue
        
        # 其他标签
        if stripped.startswith('<') and not stripped.startswith('</'):
            buffer.append(line)
            continue
        
        # 裸文本 -> 转成p
        buffer.append(f'<p>{stripped}</p>')
    
    # 处理剩余buffer
    if buffer:
        page += apply_paragraph_styles(buffer)
    
    page += '</div></body></html>'
    
    return page

def apply_paragraph_styles(buffer):
    """把buffer里的内容加上精美段落样式"""
    result = []
    for line in buffer:
        stripped = line.strip()
        if not stripped:
            continue
        
        # 已经是有标签的
        if stripped.startswith('<h'):
            result.append(stripped)
            continue
        
        # 提取内容
        p_match = re.match(r'<p[^>]*>(.*?)</p>', stripped, re.DOTALL)
        if p_match:
            content = p_match.group(1)
            # strong标签处理
            content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'<strong style="color:#c0392b;font-weight:bold;">\1</strong>', content)
            result.append(f'<p style="font-size:16px;line-height:1.95;color:#444;margin:14px 0;text-indent:2em;">{content}</p>')
        else:
            # 裸文本
            result.append(f'<p style="font-size:16px;line-height:1.95;color:#444;margin:14px 0;text-indent:2em;">{stripped}</p>')
    
    return '\n'.join(result) + '\n'

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_beautiful.py <title> <html_file> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    digest = sys.argv[3]
    
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()
    
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
    
    # 精美排版
    content = beautify_html(html, wx_urls)
    
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
