import os
import requests
import base64

API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3-pro-image-preview"

char = {
    "name": "太阳_主控",
    "prompt": """
    治愈系扁平插画，1:1正方形头像，2000×2000px。
    主体：圆润的太阳卡通形象，温柔微笑，柔和橙黄色光晕。
    标识：右下角有简化"太"字艺术标识。
    配色：暖橙色#FFB344为主，米白色#FFF5E6为辅，低饱和柔和。
    风格：无描边，色块柔化，温暖治愈，女性疗愈风。
    约束：无水印，无多余文字，浅纯色背景，边缘清晰。
    """,
    "filename": "avatar_01_太阳.png"
}

print(f"生成：{char['name']}...")
ENDPOINT = f"{BASE_URL}/models/{MODEL}:generateContent"

try:
    response = requests.post(
        ENDPOINT,
        headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": char['prompt']}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}
        },
        timeout=180
    )
    
    if response.status_code == 200:
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                image_bytes = base64.b64decode(part["inlineData"]["data"])
                os.makedirs("avatars", exist_ok=True)
                img_path = f"avatars/{char['filename']}"
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                print(f"✅ 成功：{img_path} ({len(image_bytes)/1024/1024:.2f}MB)")
except Exception as e:
    print(f"❌ 异常：{str(e)}")
