# SOP 能量视频制作流程

## 工具
- 配图：browser工具搜索下载（外网免费图片，**不用豆包生图**）
- 配音：edge-tts（Edge浏览器TTS）
- 合成：FFmpeg（Ken Burns缩放 + 交叉淡入淡出 + 音画合并）

## 完整流程

### 第1步：准备配图

**优先级顺序：**
1. **先从飞书"网络能量图片"取图**（临时下载到 /tmp/ 用完即删）
2. **图不够用时：用 browser 搜图 → 直接上传飞书**（不存本地）
3. **最后才考虑 AI 生图**（豆包/火山引擎，按次计费，能不用就不用）

**browser 工具搜图流程：**
```
1. browser action="start"
2. browser action="open" targetUrl="https://unsplash.com/s/photos/crystal-healing"
   （或 Pinterest、Pexels，关键词见下方表格）
3. browser action="snapshot"  ← 看页面 + 获取图片元素 ref
4. browser action="act" 下载图片到 /tmp/img_xxx.jpg
5. 用 feishu_doc upload_image 上传到飞书"网络能量图片"文件夹
6. 记录 file_token，后续用 feishu_doc 下载到 /tmp/ 使用
```

**主题关键词对照表：**
| 视频主题 | 搜索关键词 |
|---------|----------|
| 水晶疗愈 | crystal healing energy, amethyst crystal |
| 脉轮能量 | chakra energy, colorful chakra |
| 星空宇宙 | aurora borealis, starry sky colorful |
| 自然疗愈 | forest light healing, peaceful nature |
| 情绪释放 | calm ocean, sunrise hope |
| 身心灵 | spiritual awakening, energy healing light |

### 第2步：生成Ken Burns效果背景视频
每张图片生成5-10秒缩放效果
```bash
ffmpeg -y -loop 1 -i /tmp/chakra1.jpg \
  -vf "scale=1920:1080,zoompan=z='min(zoom+0.002,1.2)':d=125:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2)" \
  -t 5 -r 25 -s 1920x1080 /tmp/c1.mp4
```

### 第3步：拼接多张图片（无过渡）
```bash
# 先转ts格式
ffmpeg -y -i /tmp/c1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts /tmp/c1.ts

# 用concat拼接
ffmpeg -y -i "concat:/tmp/c1.ts|/tmp/c2.ts|/tmp/c3.ts" \
  -c copy -bsf:a aac_adtstoasc /tmp/chakras_concat.mp4
```

### 第4步：生成配音
```bash
edge-tts -t "配音文案" -v zh-CN-XiaoxiaoNeural --write-media /tmp/prayer_full.mp3

# 多段合并
ffmpeg -y -i "concat:/tmp/seg1.mp3|/tmp/seg2.mp3" -acodec copy /tmp/full.mp3
```

### 第5步：音画合并
```bash
ffmpeg -y -i /tmp/chakras_concat.mp4 -i /tmp/full.mp3 \
  -c:v libx264 -preset fast -b:v 3M \
  -c:a aac -b:a 128k -shortest /tmp/最终视频.mp4
```

### 第6步：保存到桌面
```bash
cp /tmp/最终视频.mp4 ~/Desktop/短视频/视频名.mp4
```

## 关键参数
- 图片尺寸：1920x1080
- Ken Burns缩放范围：zoom+0.001到1.2
- 每段背景时长：5秒
- 交叉淡入淡出：1秒（可选）
- 视频码率：3M
- 音频码率：128k

## 图片主题建议
- 七脉轮：红/橙/黄/绿/蓝/靛/紫 能量图
- 宇宙星空：星云、银河、繁星
- 自然风景：流水、莲花、山川
- 禅意风格：日落、冥想、光晕

## 图片库维护

- 所有图片**只存飞书**，不存本地（本地内存有限）
- 飞书"网络能量图片"文件夹是主图库，手机电脑都能看
- 每次 browser 下载新图后，立即上传飞书，记录 file_token
- 制作视频时临时下载到 /tmp/，完成后清除
- 禁止：为省事反复用同一张图，要保持多样性


## 图片风格规范（施欢2026-04-01明确要求）

### 禁止 ❌
- 全黑背景的宇宙星空
- 暗色调、低饱和度图片
- 单调、沉闷的画面

### 推荐 ✅
- 彩色、明艳、高饱和度
- 自然山川、河流、山峰
- 草原、峡谷、自然奇观
- 世界各地宏观风景（航拍视角更佳）
- 宏大叙事感、震撼感
- 瀑布、湖泊、海岸线、日出日落

### Unsplash推荐关键词
- nature landscape, mountain peaks, aerial view
- grand canyon, waterfall, northern lights
- ocean waves, sunrise sunset, starry sky（但选彩色非全黑）
- aurora borealis, desert dunes, tropical beach
