#!/usr/bin/env python3
"""
疗愈短视频生成器
流程：脚本 → TTS配音 → 背景图 → ARK图生视频 → 拼接 → 合成成品
用法：python3 make_healing_video.py --script "脚本文本" --output ~/Desktop/短视频/today.mp4
      python3 make_healing_video.py --script-file /tmp/script.txt --output ~/Desktop/短视频/today.mp4
"""
import os, sys, time, json, subprocess, argparse, requests, tempfile, shutil
from pathlib import Path

# ── 读取环境变量 ──────────────────────────────────────────────
def load_env():
    env_path = Path.home() / ".openclaw" / ".env"
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v.strip('"').strip("'"))

load_env()

ARK_API_KEY      = os.environ["ARK_API_KEY"]
ARK_VIDEO_EP     = os.environ.get("ARK_VIDEO_ENDPOINT", "ep-20260403163118-564sn")
PEXELS_KEYWORDS  = ["calm nature", "water flow", "morning mist", "forest peaceful", "zen garden"]

# ── Step 1: TTS 配音 ──────────────────────────────────────────
def generate_tts(text: str, output_mp3: str):
    print("🎙 生成配音...")
    # 找 tts 脚本
    tts_script = Path(__file__).parent.parent / "skills/lh-edge-tts/scripts/tts.py"
    if not tts_script.exists():
        # 直接用 edge-tts 命令行
        subprocess.run([
            "edge-tts",
            "--voice", "zh-CN-XiaoxiaoNeural",
            "--rate", "+5%",
            "--text", text,
            "--write-media", output_mp3
        ], check=True)
    else:
        subprocess.run([
            "python3", str(tts_script),
            "--text", text,
            "--voice", "zh-CN-XiaoxiaoNeural",
            "--rate", "+5%",
            "--output", output_mp3
        ], check=True)
    # 获取音频时长
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", output_mp3],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    print(f"  配音时长: {duration:.1f}秒")
    return duration

# ── Step 2: Pexels 获取背景图 ────────────────────────────────
def get_pexels_images(count: int, tmpdir: str) -> list:
    print(f"🌿 获取 {count} 张背景图...")
    images = []
    for i, kw in enumerate(PEXELS_KEYWORDS[:count]):
        try:
            resp = requests.get(
                f"https://api.pexels.com/v1/search?query={kw}&per_page=1&orientation=portrait",
                headers={"Authorization": "lYQCr0nWJDGLrMdULCEzrSbFnODmqDzNYsJb0XaDJM9KKfzHFRqYiGR4"},
                timeout=10
            )
            if resp.status_code == 200:
                photos = resp.json().get("photos", [])
                if photos:
                    img_url = photos[0]["src"]["large"]
                    img_path = f"{tmpdir}/bg_{i}.jpg"
                    img_data = requests.get(img_url, timeout=15).content
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    images.append(img_path)
                    print(f"  图{i+1}: {kw}")
        except Exception as e:
            print(f"  图{i+1} 获取失败: {e}")
    # 兜底：用本地默认图
    if not images:
        print("  Pexels 无法访问，使用纯色背景")
        for i in range(count):
            img_path = f"{tmpdir}/bg_{i}.jpg"
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", "color=c=0x1a1a2e:s=1080x1920",
                "-frames:v", "1", img_path
            ], capture_output=True)
            images.append(img_path)
    return images

# ── Step 3: ARK 图生视频 ──────────────────────────────────────
def image_to_video(img_path: str, prompt: str, out_path: str) -> bool:
    print(f"  🎬 ARK 生成视频片段: {Path(img_path).name}")
    # 上传图片到 data URL（base64）
    import base64
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    ext = Path(img_path).suffix.lstrip(".")
    data_url = f"data:image/{ext};base64,{img_b64}"

    resp = requests.post(
        "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks",
        headers={"Authorization": f"Bearer {ARK_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": ARK_VIDEO_EP,
            "content": [
                {"type": "image_url", "image_url": {"url": data_url}},
                {"type": "text", "text": prompt}
            ]
        },
        timeout=20
    )
    if resp.status_code != 200:
        print(f"    提交失败: {resp.text[:200]}")
        return False
    task_id = resp.json().get("id")

    # 轮询
    for _ in range(30):
        time.sleep(8)
        r = requests.get(
            f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}",
            headers={"Authorization": f"Bearer {ARK_API_KEY}"}, timeout=15
        )
        data = r.json()
        if data.get("status") == "succeeded":
            video_url = data["content"]["video_url"]
            video_data = requests.get(video_url, timeout=60).content
            with open(out_path, "wb") as f:
                f.write(video_data)
            return True
        elif data.get("status") in ("failed", "cancelled"):
            print(f"    ARK失败: {data}")
            return False
    return False

# ── Step 4: 拼接背景视频到目标时长 ────────────────────────────
def concat_videos_to_duration(clip_paths: list, target_duration: float, out_path: str):
    print(f"🔗 拼接背景视频（目标时长 {target_duration:.1f}s）...")
    # 写 concat 列表，循环直到够长
    total = 0
    clips_needed = []
    while total < target_duration:
        for c in clip_paths:
            clips_needed.append(c)
            total += 5  # 每段约5秒
            if total >= target_duration:
                break

    concat_file = out_path + ".txt"
    with open(concat_file, "w") as f:
        for c in clips_needed:
            f.write(f"file '{c}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-t", str(target_duration),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        out_path
    ], check=True, capture_output=True)
    os.remove(concat_file)

# ── Step 5: 合成最终视频 ─────────────────────────────────────
def merge_video_audio(video_path: str, audio_path: str, out_path: str):
    print("🎵 合成视频+配音...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", out_path
    ], check=True, capture_output=True)
    size_mb = Path(out_path).stat().st_size / 1024 / 1024
    print(f"✅ 成品: {out_path} ({size_mb:.1f}MB)")

# ── 主流程 ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", help="脚本文本（直接传入）")
    parser.add_argument("--script-file", help="脚本文件路径")
    parser.add_argument("--output", default=f"{Path.home()}/Desktop/短视频/{time.strftime('%Y%m%d')}_疗愈视频.mp4")
    parser.add_argument("--prompt", default="治愈系自然风景，缓慢流动，禅意，温柔光线", help="ARK 视频提示词")
    args = parser.parse_args()

    # 读脚本
    if args.script_file:
        script = Path(args.script_file).read_text(encoding="utf-8")
    elif args.script:
        script = args.script
    else:
        print("错误：需要 --script 或 --script-file")
        sys.exit(1)

    output_path = args.output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    tmpdir = tempfile.mkdtemp(prefix="healing_video_")
    try:
        # Step 1: TTS
        audio_path = f"{tmpdir}/voice.mp3"
        duration = generate_tts(script, audio_path)

        # Step 2: 背景图（需要 ceil(duration/5) 张）
        clip_count = max(3, int(duration / 5) + 1)
        images = get_pexels_images(min(clip_count, 5), tmpdir)

        # Step 3: ARK 图生视频
        clips = []
        for i, img in enumerate(images):
            clip_out = f"{tmpdir}/clip_{i}.mp4"
            ok = image_to_video(img, args.prompt, clip_out)
            if ok:
                clips.append(clip_out)
            else:
                # ARK 失败，用 Ken Burns 替代
                print(f"  ARK失败，用 Ken Burns 替代")
                subprocess.run([
                    "ffmpeg", "-y", "-loop", "1", "-i", img,
                    "-vf", "zoompan=z='zoom+0.0008':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1080x1920:fps=25",
                    "-t", "5", "-c:v", "libx264", clip_out
                ], capture_output=True)
                clips.append(clip_out)

        if not clips:
            print("没有背景视频，退出")
            sys.exit(1)

        # Step 4: 拼接背景
        bg_video = f"{tmpdir}/background.mp4"
        concat_videos_to_duration(clips, duration, bg_video)

        # Step 5: 合成
        merge_video_audio(bg_video, audio_path, output_path)
        print(f"\nSUCCESS:{output_path}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    main()
