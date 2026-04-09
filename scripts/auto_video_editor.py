#!/usr/bin/env python3
"""
自动视频剪辑脚本 - 自动口播视频剪辑 pipeline
用法: python3 auto_video_editor.py <视频文件路径> [输出路径]
"""

import sys
import os
import json
import subprocess
import tempfile
from pathlib import Path

# 字幕配置（1080x1920竖屏）
FONT_SIZE = 54
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
BAR_HEIGHT = 200
BAR_Y = VIDEO_HEIGHT - 280
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

def run_cmd(cmd, desc=""):
    """执行命令"""
    print(f"执行: {desc}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr[-500:]}")
        return False
    return True

def extract_audio(video_path, audio_path):
    """提取音频"""
    cmd = f'ffmpeg -y -hide_banner -i "{video_path}" -vn -ac 1 -ar 16000 "{audio_path}"'
    return run_cmd(cmd, "提取音频")

def transcribe(audio_path, output_dir):
    """语音识别"""
    cmd = f'whisper "{audio_path}" --model small --language Chinese --output_format json --word_timestamps True --output_dir "{output_dir}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # 解析结果
    json_file = Path(output_dir) / f"{Path(audio_path).stem}.json"
    if json_file.exists():
        with open(json_file) as f:
            return json.load(f)
    return None

def create_subtitle_frames(subs, output_dir):
    """生成字幕帧"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except:
        from PIL import Image, ImageDraw, ImageFont
        font = ImageFont.load_default()
    
    frames = []
    for i, (start, end, text) in enumerate(subs):
        img = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 黑色半透明底条
        draw.rectangle([0, BAR_Y, VIDEO_WIDTH, BAR_Y + BAR_HEIGHT], fill=(0, 0, 0, 200))
        
        # 白色文字
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (VIDEO_WIDTH - text_w) // 2
        y = BAR_Y + (BAR_HEIGHT - text_h) // 2 - 5
        
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        frame_path = f"{output_dir}/sub_{i}.png"
        img.save(frame_path)
        frames.append(frame_path)
    
    return frames

def build_overlay_filter(subs):
    """构建 ffmpeg overlay 滤镜"""
    filter_chain = "[0:v]"
    prev = "[v0]"
    
    for i, (start, end, text) in enumerate(subs):
        enable = f"between(t,{start},{end})"
        next_v = f"[v{i+1}]" if i < len(subs) - 1 else "[vout]"
        filter_chain += f"[{i+1}:v]overlay=0:0:enable='{enable}'{next_v}"
    
    return filter_chain

def add_subtitles(video_path, frames, subs, output_path):
    """合成字幕到视频"""
    # 构建输入参数
    inputs = [f'-i "{f}"' for f in frames]
    inputs_str = ' '.join(inputs)
    
    # 构建滤镜
    filter_chain = "[0:v]"
    for i, (start, end, text) in enumerate(subs):
        enable = f"between(t,{start},{end})"
        if i == 0:
            filter_chain = f"[0:v][{i+1}:v]overlay=0:0:enable='{enable}'[v{i+1}]"
        else:
            filter_chain += f";[v{i}][{i+1}:v]overlay=0:0:enable='{enable}'[v{i+1}]"
    filter_chain += f";[v{len(subs)}]copy{video_path.replace('[','').replace(']','')}"
    
    # 简化版：逐个叠加
    filter_str = "[0:v]"
    for i, (start, end, text) in enumerate(subs):
        enable = f"between(t,{start},{end})"
        if i < len(subs) - 1:
            filter_str += f"[{i+1}:v]overlay=0:0:enable='{enable}'[v{i+1}]"
        else:
            filter_str += f"[{i+1}:v]overlay=0:0:enable='{enable}'[vout]"
    
    cmd = f'ffmpeg -y -hide_banner -i "{video_path}" {inputs_str} -filter_complex "{filter_str}" -map "[vout]" -map "0:a" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart "{output_path}"'
    
    return run_cmd(cmd, "合成字幕")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 auto_video_editor.py <视频文件路径> [输出路径]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else video_path.replace('.mov', '_edited.mp4').replace('.mp4', '_edited.mp4')
    
    print(f"输入: {video_path}")
    print(f"输出: {output_path}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = f"{tmpdir}/audio.wav"
        
        # 1. 提取音频
        if not extract_audio(video_path, audio_path):
            sys.exit(1)
        
        # 2. 语音识别
        print("语音识别中...")
        result = transcribe(audio_path, tmpdir)
        if not result:
            print("语音识别失败")
            sys.exit(1)
        
        # 3. 提取字幕段落
        subs = []
        for seg in result.get('segments', []):
            start = seg.get('start', 0)
            end = seg.get('end', 0)
            text = seg.get('text', '').strip()
            if text and end - start > 0.3:  # 忽略太短的片段
                subs.append((start, end, text))
        
        print(f"识别到 {len(subs)} 个字幕段")
        
        # 4. 生成字幕帧
        print("生成字幕帧...")
        frames = create_subtitle_frames(subs, tmpdir)
        
        # 5. 合成视频
        print("合成视频...")
        if add_subtitles(video_path, frames, subs, output_path):
            print(f"完成: {output_path}")
        else:
            print("合成失败")
            sys.exit(1)

if __name__ == "__main__":
    main()
