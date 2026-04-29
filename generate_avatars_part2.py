import os
import requests
import json
import base64

# 配置
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3-pro-image-preview"

# 剩余5个角色（含之前失败的2个）
characters = [
    {
        "name": "太阳_主控",
        "colors": "暖橙色#FFB344 + 米白色#FFF5E6",
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
        "name": "蕊蕊_内容官",
        "colors": "樱花粉#FFB6C1 + 奶白色#FFFAF0",
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
        "name": "朵朵_设计师",
        "colors": "水绿色#98D8C8 + 鹅黄色#FFFACD",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：温柔花朵精灵，头顶小雏菊，周围飘花瓣和小画笔。
        标识：右上角有简化"朵"字艺术标识。
        配色：水绿色为主，鹅黄色为辅，清新自然。
        风格：无描边，色块柔化，温柔有审美，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_05_朵朵.png"
    },
    {
        "name": "光头强_技术官",
        "colors": "深蓝色#4A6FA5 + 灰色#E0E0E0",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：稳重技术专家形象，戴眼镜，光头柔和处理，周围小齿轮代码符号。
        标识：左下角有简化"强"字艺术标识。
        配色：深蓝色为主，灰色为辅，沉稳专业。
        风格：无描边，色块柔化，稳重可靠，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_06_光头强.png"
    },
    {
        "name": "梦梦_记忆官",
        "colors": "浅紫色#E6E6FA + 淡蓝色#B0E0E6",
        "prompt": """
        治愈系扁平插画，1:1正方形头像，2000×2000px。
        主体：梦幻云朵精灵，温柔微笑，周围飘星光和记忆碎片。
        标识：右下角有简化"梦"字艺术标识。
        配色：浅紫色为主，淡蓝色为辅，梦幻渐变。
        风格：无描边，色块柔化，细心温柔，女性疗愈风。
        约束：无水印，无多余文字，浅纯色背景，边缘清晰。
        """,
        "filename": "avatar_07_梦梦.png"
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
print("🚀 开始生成剩余5个头像...")
success = 0
for char in characters:
    if generate_avatar(char):
        success +=1

# 统计总成功数
import os
total_success = len([f for f in os.listdir("avatars") if f.startswith("avatar_")])
print(f"\n✅ 本轮生成完成：成功{success}/5")
print(f"📊 总生成进度：{total_success}/7")
