#!/usr/bin/env python3
"""
火山引擎 ARK 视频生成脚本
用法：python3 generate_ark_video.py --prompt "视频描述" --output /tmp/output.mp4
"""
import os
import sys
import json
import time
import argparse
import requests

ARK_API_KEY = os.environ.get("ARK_API_KEY", "")
ARK_VIDEO_ENDPOINT = os.environ.get("ARK_VIDEO_ENDPOINT", "ep-20260403163118-564sn")
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

def submit_video_task(prompt: str) -> str:
    """提交视频生成任务，返回 task_id"""
    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": ARK_VIDEO_ENDPOINT,
        "content": prompt,
    }
    # 尝试视频生成接口
    resp = requests.post(
        f"{BASE_URL}/contents/generations/tasks",
        headers=headers,
        json=payload,
        timeout=30
    )
    if resp.status_code != 200:
        print(f"提交失败: {resp.status_code} {resp.text}")
        sys.exit(1)
    data = resp.json()
    task_id = data.get("id") or data.get("task_id")
    print(f"任务已提交，task_id: {task_id}")
    return task_id

def poll_task(task_id: str, max_wait=300) -> str:
    """轮询任务状态，返回视频 URL"""
    headers = {"Authorization": f"Bearer {ARK_API_KEY}"}
    start = time.time()
    while time.time() - start < max_wait:
        resp = requests.get(
            f"{BASE_URL}/contents/generations/tasks/{task_id}",
            headers=headers,
            timeout=15
        )
        data = resp.json()
        status = data.get("status", "")
        print(f"状态: {status}")
        if status == "succeeded":
            # 找视频 URL
            for item in data.get("content", []):
                if item.get("type") == "video_url":
                    return item["video_url"]["url"]
            # 兜底
            return json.dumps(data)
        elif status in ("failed", "cancelled"):
            print(f"任务失败: {data}")
            sys.exit(1)
        time.sleep(10)
    print("超时，任务未完成")
    sys.exit(1)

def download_video(url: str, output_path: str):
    """下载视频到本地"""
    resp = requests.get(url, stream=True, timeout=120)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"视频已保存: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, help="视频描述（中文）")
    parser.add_argument("--output", default="/tmp/ark_video.mp4", help="输出路径")
    args = parser.parse_args()

    if not ARK_API_KEY:
        print("错误：未设置 ARK_API_KEY 环境变量")
        sys.exit(1)

    print(f"开始生成视频：{args.prompt}")
    task_id = submit_video_task(args.prompt)
    video_url = poll_task(task_id)
    download_video(video_url, args.output)
    print(f"SUCCESS:{args.output}")

if __name__ == "__main__":
    main()
