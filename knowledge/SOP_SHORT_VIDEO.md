# SOP_SHORT_VIDEO.md - 短视频生成流程

## 定位
内容创作分身的主业，负责把脚本变成真正可发布的短视频。

## 工具现状
- TTS配音：✅ Edge TTS（已可用）
- 视频生成：✅ 火山引擎 ARK（ep-20260403163118-564sn，env: ARK_VIDEO_ENDPOINT）
- 视频合成：✅ ffmpeg（音画合并）
- 背景图备选：✅ Pexels 免费图（ARK失败时用）

## 目标效果
- 禅意/身心灵风格的真实视频（有流动画面，不是字幕卡片）
- AI配音（语音同步）
- 竖屏 9:16，可直接发抖音/视频号

## 标准流程

### 第一步：生成脚本
根据当天主题（禅意/能量/疗愈）写30-60秒口播脚本。

### 第二步：TTS 配音
```bash
python3 skills/lh-edge-tts/scripts/tts.py \
  --text "脚本内容" \
  --voice zh-CN-XiaoxiaoNeural \
  --rate +5% \
  --output /tmp/short_video_audio.mp3
```

### 第三步：火山 ARK 生成视频背景
```bash
source ~/.openclaw/.env
python3 scripts/generate_ark_video.py \
  --prompt "禅意自然风景，流水山石，晨雾，治愈系，竖屏9:16" \
  --output /tmp/ark_bg_video.mp4
```
ARK 失败时，用 Pexels 图 + Ken Burns 效果替代：
```bash
python3 scripts/search_free_image.py "calm nature peaceful"
ffmpeg -loop 1 -i 图片路径 -vf "zoompan=z='zoom+0.001':x='iw/2':y='ih/2':d=300:s=1080x1920" -t 30 /tmp/ark_bg_video.mp4
```

### 第四步：合成
```bash
ffmpeg -i /tmp/ark_bg_video.mp4 -i /tmp/short_video_audio.mp3 \
  -c:v copy -c:a aac -shortest \
  /tmp/short_video_final.mp4
mkdir -p ~/Desktop/短视频
cp /tmp/short_video_final.mp4 ~/Desktop/短视频/$(date +%Y%m%d)_短视频.mp4
```

## 禁止
- 禁止用 lh-video-gen 的字幕卡片模式作为最终产品
- 不得输出静态图轮播当做视频交付

## 输出路径
- 最终视频：~/Desktop/短视频/YYYYMMDD_短视频.mp4

## 短视频图片来源规则（2026-04-04更新）

**默认方案B**，方案A备用。

| 方案 | 图片来源 | 何时用 |
|------|---------|--------|
| B（默认）| Pexels免费图库选图 | 日常量产 |
| A（备用）| 火山引擎AI生图 | B找不到合适图片时 |

执行顺序：先搜Pexels图库 → 找不到合适的 → 切换火山引擎生图。
