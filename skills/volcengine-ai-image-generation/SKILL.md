---
name: volcengine-ai-image-generation
description: Image generation workflow on Volcengine AI services. Use when users need text-to-image, style variants, prompt refinement, or deterministic image generation parameters and troubleshooting.
---

# volcengine-ai-image-generation（火山引擎 ARK）

## 环境变量（已配置在 ~/.openclaw/.env）

- `ARK_API_KEY` — 火山引擎 ARK API 密钥
- `ARK_VIDEO_ENDPOINT` — 视频生成专用推理接入点 `ep-20260403163118-564sn`
- `DOUBAO_API_KEY` — 豆包智能路由（图片/文本）

## 视频生成调用方式

```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ.get("ARK_API_KEY"))

response = client.chat.completions.create(
    model=os.environ.get("ARK_VIDEO_ENDPOINT"),  # ep-20260403163118-564sn
    messages=[{"role": "user", "content": "视频描述提示词"}]
)
```

或用 requests 直接调用：

```python
import os, requests

resp = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['ARK_API_KEY']}"},
    json={
        "model": os.environ["ARK_VIDEO_ENDPOINT"],
        "messages": [{"role": "user", "content": "视频描述"}]
    }
)
```

## 图片生成 Execution Checklist

1. Confirm model/endpoint and output constraints (size, count, style).
2. Normalize prompt into subject, style, scene, lighting, camera terms.
3. Set generation parameters and run request.
4. Return image links/files with prompt and params.

## Prompt Structure

- Subject
- Composition
- Style
- Lighting
- Quality constraints

## References

- `references/sources.md`
