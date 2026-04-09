#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - v8 参考"你不是懒，你只是耗尽了"风格
- 677px宽度容器
- H1绿色背景白字圆角
- H2绿色字+emoji
- P段落深灰15px行高1.8
- 引用框浅绿背景+左边框
- 开头/中间/结尾各1张图
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

def parse_blocks(text):
    """解析文本，返回块列表"""
    blocks = []
    # 清理
    text = re.sub(r'<img[^>]*>', '', text)
    text = re.sub(r'data-src="[^"]*"', '', text)
    text = re.sub(r'#{1,6}\s+', '', text)
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # H1
        m = re.match(r'<h1[^>]*>(.*?)</h1>', line, re.DOTALL)
        if m:
            blocks.append(('h1', m.group(1)))
            continue
        # H2
        m = re.match(r'<h2[^>]*>(.*?)</h2>', line, re.DOTALL)
        if m:
            blocks.append(('h2', m.group(1)))
            continue
        # P
        m = re.match(r'<p[^>]*>(.*?)</p>', line, re.DOTALL)
        if m:
            blocks.append(('p', m.group(1)))
            continue
        # 其他标签
        if line.startswith('<'):
            blocks.append(('other', line))
            continue
        # 裸文本
        if line:
            blocks.append(('p', line))
    return blocks

def build_html(title, text, wx_urls):
    """参考"你不是懒"风格构建HTML"""
    blocks = parse_blocks(text)
    total = len(blocks)
    
    # 找分割点
    h2_indices = [i for i, (t, _) in enumerate(blocks) if t == 'h2']
    
    if len(h2_indices) >= 2:
        split_idx = h2_indices[len(h2_indices)//2]
    elif total > 3:
        split_idx = total // 2
    else:
        split_idx = total
    
    img1, img2, img3 = (wx_urls + [None]*3)[:3]
    
    # HTML结构
    html = f'''<html lang="zh-CN">
<div style="width:677px;max-width:100%;margin:0 auto;padding:20px 0;">
<div style="background:#fff;padding:24px 28px 32px;font-family:PingFang SC,Microsoft YaHei,sans-serif;">
<section style="background-color:#ffffff;padding:16px">

<h1 style="font-size:22px;font-weight:bold;color:#ffffff;text-align:center;background:#1a7a5a;border-radius:8px;padding:12px 24px;margin-top:24px;margin-bottom:12px;line-height:1.2;">{title}</h1>

'''
    # 开头图片
    if img1:
        html += f'<p style="text-align:center;margin:20px 0;"><img src="{img1}" style="width:100%;max-width:500px;border-radius:8px;" /></p>\n'
    
    # 前半部分
    for i, (btype, bcontent) in enumerate(blocks[:split_idx]):
        if btype == 'h2':
            html += f'<h2 style="font-size:17px;color:#1a7a5a;font-weight:bold;margin:20px 0 10px;">{bcontent}</h2>\n'
        else:
            # 处理strong
            bcontent = re.sub(r'<strong[^>]*>(.*?)</strong>', r'<strong style="color:#1a7a5a;font-weight:bold;">\1</strong>', bcontent)
            html += f'<p style="font-size:15px;color:#333;line-height:1.8;margin:12px 0;">{bcontent}</p>\n'
    
    # 中间图片
    if img2:
        html += f'<p style="text-align:center;margin:20px 0;"><img src="{img2}" style="width:100%;max-width:500px;border-radius:8px;" /></p>\n'
    
    # 后半部分
    for btype, bcontent in blocks[split_idx:]:
        if btype == 'h2':
            html += f'<h2 style="font-size:17px;color:#1a7a5a;font-weight:bold;margin:20px 0 10px;">{bcontent}</h2>\n'
        else:
            bcontent = re.sub(r'<strong[^>]*>(.*?)</strong>', r'<strong style="color:#1a7a5a;font-weight:bold;">\1</strong>', bcontent)
            html += f'<p style="font-size:15px;color:#333;line-height:1.8;margin:12px 0;">{bcontent}</p>\n'
    
    # 结尾图片
    if img3:
        html += f'<p style="text-align:center;margin:20px 0;"><img src="{img3}" style="width:100%;max-width:500px;border-radius:8px;" /></p>\n'
    
    html += '''
</section>
</div>
</div>
</html>'''
    
    return html

def main():
    if len(sys.argv) < 4:
        print("用法: python3 auto_push_v8.py <title> <text_file> <digest>")
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
    
    # 正文图片
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
