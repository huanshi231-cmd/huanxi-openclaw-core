import os
import requests
import json
import base64

# 配置
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3-pro-image-preview"

# 前4个角色
characters = [
    {
        "name": "太阳_主控",
        "colors": "暖橙色#FFB344 + 米白色#FFF5E6",
        "personality": "沉稳可靠，温暖有力量",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：圆润的太阳卡通形象，温柔微笑，柔和橙黄色光晕。
        标识：右下角有简化"太"字艺术标识。
        配色：暖橙色为主，米白色为辅，低饱和柔和。
        风格：无描边，色块柔化，温暖治愈，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_01_太阳.png"
    },
    {
        "name": "灵夕_灵感官",
        "colors": "淡紫色#D4B2D8 + 浅粉色#FFE6F2",
        "personality": "灵动梦幻，充满创意",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：灵动小仙女侧脸，星星发饰，眼睛亮晶晶，周围漂浮小星月牙。
        标识：左上角有简化"灵"字艺术标识。
        配色：淡紫色为主，浅粉色为辅，梦幻渐变。
        风格：无描边，色块柔化，灵动梦幻，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_02_灵夕.png"
    },
    {
        "name": "蕊蕊_内容官",
        "colors": "樱花粉#FFB6C1 + 奶白色#FFFAF0",
        "personality": "温柔文艺，细腻敏感",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：温柔女生侧脸，头发别小樱花，周围飘花瓣，浅微笑。
        标识：右下角有简化"蕊"字艺术标识。
        配色：樱花粉为主，奶白色为辅，柔和低饱和。
        风格：无描边，色块柔化，温柔文艺，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_03_蕊蕊.png"
    },
    {
        "name": "跳跳_运营官",
        "colors": "亮黄色#FFE066 + 天蓝色#87CEEB",
        "personality": "活泼开朗，充满能量",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：活泼卡通形象，大笑，跳跃动态，周围有小闪电火花。
        标识：左下角有简化"跳"字艺术标识。
        配色：亮黄色为主，天蓝色为辅，明亮活泼。
        风格：无描边，色块柔化，活泼开朗，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_04_跳跳.png"
    }
]

# 生成函数
def generate_avatar(char):
    print(f"\n生成：{char['name']}...")
    ENDPOINT = f"{BASE_URL}/models/{MODEL}:generateContent"
    
    try:
        response = requests.post(
            ENDPOINT,
            headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": char['prompt']}]}],
                "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}
            },
            timeout=120
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
                    return True
            print(f"❌ 失败：无图片")
            return False
        else:
            print(f"❌ 失败：HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 异常：{str(e)}")
        return False

# 执行
print("🚀 开始生成前4个头像...")
success = 0
for char in characters:
    if generate_avatar(char):
        success +=1

print(f"\n✅ 前4个生成完成：成功{success}/4")
