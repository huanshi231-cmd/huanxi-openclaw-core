#!/usr/bin/env python3
"""MiMo-V2-Omni 视频分析脚本
用法: python3 mimo_video_analyze.py <视频文件路径> [问题]
"""
import sys, json, base64, subprocess, mimetypes, os

API_BASE = "https://token-plan-cn.xiaomimimo.com/v1"
API_KEY = os.environ.get("MIMO_API_KEY", "tp-cboke2c3uptyidf2wmpm7z5tzli51inniftvakga6vpkur30")

def analyze_video(video_path: str, question: str = "请描述这个视频的内容") -> str:
    # 获取MIME类型
    mime_type, _ = mimetypes.guess_type(video_path)
    if not mime_type:
        mime_type = "video/mp4"
    
    # 读取并编码视频
    with open(video_path, 'rb') as f:
        video_data = f.read()
    
    if len(video_data) > 10 * 1024 * 1024:  # 10MB限制
        return "错误：视频文件超过10MB限制"
    
    video_b64 = base64.b64encode(video_data).decode()
    
    payload = json.dumps({
        "model": "mimo-v2-omni",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "video_url", "video_url": {"url": f"data:{mime_type};base64,{video_b64}"}, "fps": 2, "media_resolution": "default"},
                {"type": "text", "text": question}
            ]
        }],
        "max_completion_tokens": 1024
    }, ensure_ascii=False)
    
    proc = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'{API_BASE}/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {API_KEY}',
        '--max-time', '60',
        '-d', payload
    ], capture_output=True, text=True)
    
    try:
        d = json.loads(proc.stdout)
        if 'choices' in d:
            return d['choices'][0].get('message', {}).get('content', '空回复')
        elif 'error' in d:
            return f"API错误: {d['error'].get('message', '')}"
        else:
            return f"未知响应: {proc.stdout[:200]}"
    except:
        return f"解析失败: {proc.stdout[:200]}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 mimo_video_analyze.py <视频文件路径> [问题]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "请描述这个视频的内容"
    
    if not os.path.exists(video_path):
        print(f"错误：文件不存在 - {video_path}")
        sys.exit(1)
    
    result = analyze_video(video_path, question)
    print(result)
