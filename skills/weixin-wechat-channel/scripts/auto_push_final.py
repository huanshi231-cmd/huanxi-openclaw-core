#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

def parse_blocks(html):
    """把HTML解析成独立的块（h1/h2/p/文本）"""
    blocks = []
    
    # 先删掉所有img标签
    html = re.sub(r'<img[^>]*>', '', html)
    html = re.sub(r'data-src="[^"]*"', '', html)
    
    # 清理markdown
    html = re.sub(r'#{1,6}\s+', '', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 逐行分析
    in_p = False
    current_p_content = []
    
    for line in html.split('\n'):
        stripped = line.strip()
        if not stripped:
            if current_p_content:
                text = ' '.join(current_p_content)
                if text:
                    blocks.append(('text', text))
                current_p_content = []
            in_p = False
            continue
        
        # H1
        h1 = re.match(r'<h1[^>]*>(.*?)</h1>', stripped, re.DOTALL)
        if h1:
            if current_p_content:
                text = ' '.join(current_p_content)
                if text:
                    blocks.append(('text', text))
                current_p_content = []
            blocks.append(('h1', h1.group(1)))
            continue
        
        # H2
        h2 = re.match(r'<h2[^>]*>(.*?)</h2>', stripped, re.DOTALL)
        if h2:
            if current_p_content:
                text = ' '.join(current_p_content)
                if text:
                    blocks.append(('text', text))
                current_p_content = []
            blocks.append(('h2', h2.group(1)))
            continue
        
        # P标签内容
        p_match = re.match(r'<p[^>]*>(.*?)</p>', stripped, re.DOTALL)
        if p_match:
            current_p_content.append(p_match.group(1))
            in_p = True
            continue
        
        # 其他标签
        if stripped.startswith('<'):
            current_p_content.append(stripped)
            in_p = True
            continue
        
        # 裸文本
        current_p_content.append(stripped)
        in_p = True
    
    # 剩余
    if current_p_content:
        text = ' '.join(current_p_content)
        if text:
            blocks.append(('text', text))
    
    return blocks

def build_html(title, text, wx_urls):
    """
    简洁排版：
    - 标题
    - 开头图片
    - 前半部分（保留h2结构）
    - 中间图片
    - 后半部分
    - 结尾图片
    """
    # 删img、清markdown
    text = re.sub(r'<img[^>]*>', '', text)
    text = re.sub(r'data-src="[^"]*"', '', text)
    text = re.sub(r'#{1,6}\s+', '', text)
    
    img1, img2, img3 = (wx_urls + [None]*3)[:3]
    
    # HTML头
    html = f'''<section style="padding:0 15px;margin:0;">
<h1 style="font-size:20px;font-weight:bold;text-align:center;margin:25px 0 20px;line-height:1.6;color:#222;">{title}</h1>
'''
    
    # 开头图片
    if img1:
        html += f'<p style="text-align:center;margin:20px 0;"><img src="{img1}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    # 找h2分割点
    h2_positions = [i for i, (t, _) in enumerate(parse_blocks(text)) if t == 'h2']
    
    if len(h2_positions) >= 2:
        # 以第2个h2为分割点
        mid_h2_idx = h2_positions[1]
        blocks = parse_blocks(text)
        front_blocks = blocks[:mid_h2_idx]
        back_blocks = blocks[mid_h2_idx:]
    elif len(h2_positions) == 1:
        mid_h2_idx = h2_positions[0]
        blocks = parse_blocks(text)
        front_blocks = blocks[:mid_h2_idx]
        back_blocks = blocks[mid_h2_idx:]
    else:
        # 没有h2，平均分
        blocks = parse_blocks(text)
        total = len(blocks)
        split = total // 2
        front_blocks = blocks[:split]
        back_blocks = blocks[split:]
    
    # 渲染前半部分
    for btype, bcontent in front_blocks:
        if btype == 'h2':
            html += f'<h2 style="font-size:17px;font-weight:bold;color:#2a5a8a;margin:25px 0 12px;padding-bottom:6px;border-bottom:1px solid #e8f0f7;">{bcontent}</h2>\n'
        else:
            # 处理strong
            bcontent = re.sub(r'<strong>(.*?)</strong>', r'<strong style="color:#c0392b;font-weight:bold;">\1</strong>', bcontent)
            html += f'<p style="font-size:15px;line-height:2;text-indent:2em;margin:0 0 14px;color:#333;">{bcontent}</p>\n'
    
    # 中间图片
    if img2:
        html += f'<p style="text-align:center;margin:25px 0;"><img src="{img2}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    # 渲染后半部分
    for btype, bcontent in back_blocks:
        if btype == 'h2':
            html += f'<h2 style="font-size:17px;font-weight:bold;color:#2a5a8a;margin:25px 0 12px;padding-bottom:6px;border-bottom:1px solid #e8f0f7;">{bcontent}</h2>\n'
        else:
            bcontent = re.sub(r'<strong>(.*?)</strong>', r'<strong style="color:#c0392b;font-weight:bold;">\1</strong>', bcontent)
            html += f'<p style="font-size:15px;line-height:2;text-indent:2em;margin:0 0 14px;color:#333;">{bcontent}</p>\n'
    
    # 结尾图片
    if img3:
        html += f'<p style="text-align:center;margin:25px 0;"><img src="{img3}" style="width:100%;max-width:400px;border-radius:8px;" /></p>\n'
    
    html += '</section>'
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_final.py <title> <text_file> <digest>")
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
