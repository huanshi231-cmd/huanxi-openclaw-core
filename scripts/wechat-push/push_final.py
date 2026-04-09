#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号推送 - 最终版（铁律版）
流程：排版 → 加emoji → 清洗 → 插图片 → 推送
"""
import os, re, sys, json, requests, subprocess
from pathlib import Path

sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
from sanitize_wechat_html import sanitize_text

# 图片库
IMAGE_LIB = {
    '情绪': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_13_light_glow.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_12_light_energy.jpg',
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
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_07_milky_way.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_08_stars_meteor.jpg',
    ],
    'default': [
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_14_flower_bloom.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_17_nature_forest.jpg',
        '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_06_stars_night.jpg',
    ]
}

DEFAULT_COVER = '/Users/huanxi/.openclaw/workspace-neirong/images/20260408_aquarius_cover.jpg'

# H2 emoji装饰映射
H2_EMOJI = {
    '你有没有发现': '🌙 ',
    '一个你可能没注意到的信号': '💜 ',
    '那个一直在压抑的你，终于被正名了': '🌸 ',
    '哭哭马为什么会让人哭': '✨ ',
    '情绪经济爆发背后，是一代人的觉醒': '💧 ',
    '怎么开始善待自己的情绪？': '🔔 ',
    '最后': '🌿 ',
}

# 主题轮换计数器
COUNTER_FILE = '/tmp/wechat-push/wechat_theme_counter.txt'
THEMES = ['coffee-house', 'newspaper', 'elegant-blue', 'midnight', 'terracotta']

def get_theme():
    """获取当前主题（轮换）"""
    counter = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE) as f:
                counter = int(f.read().strip())
        except:
            counter = 0
    theme = THEMES[counter % len(THEMES)]
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(counter + 1))
    return theme

def get_token():
    appid = os.environ.get("WECHAT_APPID")
    secret = os.environ.get("WECHAT_APPSECRET")
    s = requests.Session(); s.trust_env = False
    r = s.get(f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}", timeout=60)
    return s, r.json().get("access_token")

def upload_image(s, token, path):
    if not os.path.exists(path): return None, None
    with open(path, "rb") as f:
        files = {"media": (Path(path).name, f, "image/jpeg")}
        r = s.post(f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image", files=files, timeout=60)
    result = r.json()
    return result.get("media_id"), result.get("url")

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

def main():
    if len(sys.argv) < 4:
        print("用法: python3 push_final.py <title> <input_md> <digest>")
        sys.exit(1)
    
    title = sys.argv[1]
    input_file = sys.argv[2]
    digest = sys.argv[3]
    
    s, token = get_token()
    if not token:
        print("FAIL: token获取失败"); sys.exit(1)
    
    # 1. 排版（自动轮换主题）
    theme = get_theme()
    print(f"主题: {theme}")
    subprocess.run(['python3', '/Users/huanxi/.openclaw/workspace-neirong/skills/xiaohu-wechat-format/scripts/format.py',
                    '--input', input_file, '--theme', theme, '--no-open'],
                   capture_output=True, timeout=120)
    
    # 2. 提取section
    with open("/tmp/wechat-format/article/preview.html", "r") as f:
        html = f.read()
    s_start = html.find('<section', html.find('articleContent'))
    s_end = html.find('</section>', s_start)
    section = html[s_start:s_end+10]
    
    # 3. H2添加emoji装饰
    for text, emoji in H2_EMOJI.items():
        section = section.replace(f'>{text}<', f'>{emoji}{text}<')
    
    # 4. 清洗（铁律：不可跳过！）
    content = sanitize_text(section)
    print("清洗完成")
    
    # 5. 上传图片
    keyword = title + ' ' + digest
    img_paths = select_images(keyword, count=3)
    wx_urls = []
    for p in img_paths:
        _, url = upload_image(s, token, p)
        if url: wx_urls.append(url)
    
    cover_id, _ = upload_image(s, token, DEFAULT_COVER) if os.path.exists(DEFAULT_COVER) else (None, None)
    
    # 6. 插图片（开头/中间/结尾）
    img_tag = lambda u: f'<p style="text-align:center;margin:24px 0;"><img src="{u}" style="width:100%;max-width:520px;border-radius:10px;" /></p>'
    
    h1_end = content.find('</h1>')
    if h1_end > 0 and wx_urls:
        content = content[:h1_end+6] + '\n' + img_tag(wx_urls[0]) + '\n' + content[h1_end+6:]
    
    h2_positions = [m.end() for m in re.finditer(r'</h2>', content)]
    if len(h2_positions) >= 2 and len(wx_urls) > 1:
        mid_pos = h2_positions[len(h2_positions)//2]
        content = content[:mid_pos] + '\n' + img_tag(wx_urls[1]) + '\n' + content[mid_pos:]
    
    if len(wx_urls) > 2:
        content = content.replace('</section>', img_tag(wx_urls[2]) + '\n</section>')
    
    # 7. 推送（铁律：ensure_ascii=False）
    article = {
        "title": title[:40],
        "author": "欢喜",
        "digest": digest[:30],
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
        print(f"SUCCESS: {result['media_id']}")
    else:
        print(f"FAIL: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
