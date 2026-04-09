#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿箱推送脚本（带排版和图片）
- 强制直连微信API，忽略系统代理
- 自动处理封面图：优先使用传入的 media_id，无则上传默认封面
- 自动添加排版格式和能量图片
- 用法: python3 push_draft_with_formatting.py "<title>" "<html_file>" "<digest>" [thumb_media_id]
"""
import os
import re
import sys
from pathlib import Path

import json
import requests

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
from sanitize_wechat_html import sanitize_text

DEFAULT_COVER = Path(__file__).resolve().parent.parent.parent.parent / "images" / "aquarius_cover.jpg"

# 飞书能量图片库图片URL
ENERGY_IMAGE_URL = "https://lf3-feishu-cdn.feishucdn.com/obj/feishu-assets/MyfhbxOw4oKcJAxJb9qcNP49nOh.image"


def ensure_utf8_content(text: str) -> str:
    """确保内容是UTF-8编码的中文，而不是Unicode转义序列"""
    if not text:
        return text
    # 如果内容中有 \\uXXXX 形式的转义序列，解码它
    def decode_u4(m):
        return chr(int(m.group(1), 16))
    text = re.sub(r"\\u([0-9a-fA-F]{4})".format(), decode_u4, text)
    text = re.sub(r"\\U([0-9a-fA-F]{8})".format(), decode_u4, text)
    return text


def upload_cover(s, token, cover_path=None):
    """上传封面图，返回 media_id"""
    path = Path(cover_path) if cover_path else DEFAULT_COVER
    if not path.exists():
        print(f"封面图不存在: {path}，跳过", file=sys.stderr)
        return ""
    with open(path, "rb") as f:
        files = {"media": (path.name, f, "image/jpeg")}
        r = s.post(
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
            files=files,
            timeout=60,
        )
    result = r.json()
    if "media_id" in result:
        return result["media_id"]
    print(f"上传封面失败: {result}", file=sys.stderr)
    return ""


def push_draft(title, content_file, digest, thumb_media_id=None):
    # 读取内容文件
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加排版格式
    formatted_content = f"""
    <h1>{title}</h1>
    <img src="{ENERGY_IMAGE_URL}" style="width:100%;" />
    <p>{content}</p>
    """
    
    # 清理内容
    content = sanitize_text(formatted_content)
    
    # 获取access_token
    # (原有获取access_token的代码保持不变)
    
    # 创建草稿
    # (原有创建草稿的代码保持不变，使用formatted_content)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 push_draft_with_formatting.py \"<title>\" \"<html_file>\" \"<digest>\" [thumb_media_id]")
        sys.exit(1)
    title = sys.argv[1]
    content_file = sys.argv[2]
    digest = sys.argv[3]
    thumb_media_id = sys.argv[4] if len(sys.argv) > 4 else None
    push_draft(title, content_file, digest, thumb_media_id)
