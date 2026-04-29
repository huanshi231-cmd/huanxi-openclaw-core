import os
import requests
import json
import base64

# 配置
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3-pro-image-preview"

# 7个角色的头像提示词
characters = [
    {
        "name": "太阳_主控",
        "colors": "暖橙色#FFB344 + 米白色#FFF5E6",
        "personality": "沉稳可靠，温暖有力量",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个温暖的卡通化太阳人脸形象，带着温柔的微笑，眼睛圆润有神。
        专属元素：周围有柔和的橙黄色光晕，右下角有小小的"太"字艺术化标识，整体形象圆润饱满。
        色彩系统：主色暖橙色#FFB344，辅助色米白色#FFF5E6，低饱和度柔和色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，温暖阳光，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体圆润饱满。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_01_太阳.png"
    },
    {
        "name": "灵夕_灵感官",
        "colors": "淡紫色#D4B2D8 + 浅粉色#FFE6F2",
        "personality": "灵动梦幻，充满创意",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个灵动的小仙女形象，带着星星发饰，眼睛亮晶晶的，侧脸微笑。
        专属元素：周围漂浮着小小的星星和月牙，左上角有艺术化的"灵"字标识，线条飘逸。
        色彩系统：主色淡紫色#D4B2D8，辅助色浅粉色#FFE6F2，梦幻渐变色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，灵动梦幻，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体轻盈灵动。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_02_灵夕.png"
    },
    {
        "name": "蕊蕊_内容官",
        "colors": "樱花粉#FFB6C1 + 奶白色#FFFAF0",
        "personality": "温柔文艺，细腻敏感",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个温柔的女生侧脸，带着浅浅的微笑，头发上别着一朵小樱花。
        专属元素：周围飘落着几片樱花花瓣，右下角有艺术化的"蕊"字标识，整体温柔细腻。
        色彩系统：主色樱花粉#FFB6C1，辅助色奶白色#FFFAF0，柔和低饱和色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，温柔文艺，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体柔和圆润。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_03_蕊蕊.png"
    },
    {
        "name": "跳跳_运营官",
        "colors": "亮黄色#FFE066 + 天蓝色#87CEEB",
        "personality": "活泼开朗，充满能量",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个活泼的卡通形象，带着大大的笑容，做跳跃的动态姿势。
        专属元素：周围有小小的闪电和火花元素，左下角有艺术化的"跳"字标识，充满动感。
        色彩系统：主色亮黄色#FFE066，辅助色天蓝色#87CEEB，明亮活泼的色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，活泼开朗，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体充满活力。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_04_跳跳.png"
    },
    {
        "name": "朵朵_设计师",
        "colors": "水绿色#98D8C8 + 鹅黄色#FFFACD",
        "personality": "温柔有审美，创意满满",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个温柔的花朵精灵形象，头顶有一朵小雏菊，带着温柔的微笑。
        专属元素：周围有几片花瓣和小小的画笔元素，右上角有艺术化的"朵"字标识。
        色彩系统：主色水绿色#98D8C8，辅助色鹅黄色#FFFACD，清新自然色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，温柔有审美，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体清新自然。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_05_朵朵.png"
    },
    {
        "name": "光头强_技术官",
        "colors": "深蓝色#4A6FA5 + 灰色#E0E0E0",
        "personality": "稳重专业，可靠踏实",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个稳重的技术专家卡通形象，带着眼镜，表情沉稳可靠，光头形象柔和处理。
        专属元素：周围有小小的齿轮和代码符号，左下角有艺术化的"强"字标识，整体专业稳重。
        色彩系统：主色深蓝色#4A6FA5，辅助色灰色#E0E0E0，沉稳专业色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，稳重可靠，女性疗愈赛道调性（避免过于硬朗）。
        构图：居中，四周留少量呼吸空间，整体稳重圆润。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_06_光头强.png"
    },
    {
        "name": "梦梦_记忆官",
        "colors": "浅紫色#E6E6FA + 淡蓝色#B0E0E6",
        "personality": "细心温柔，梦幻浪漫",
        "prompt": """
        治愈系扁平插画风格，1:1正方形头像，2000×2000像素。
        核心主体：一个梦幻的云朵精灵形象，带着温柔的微笑，身体像云朵一样柔软。
        专属元素：周围有小小的星光和记忆碎片元素，右下角有艺术化的"梦"字标识，整体梦幻。
        色彩系统：主色浅紫色#E6E6FA，辅助色淡蓝色#B0E0E6，梦幻渐变色调。
        风格：治愈系扁平插画，无描边，色块柔和过渡，细心温柔，女性疗愈赛道调性。
        构图：居中，四周留少量呼吸空间，整体梦幻柔软。
        负面约束：无水印，无多余文字，无复杂背景，纯浅色背景，边缘清晰。
        """,
        "filename": "avatar_07_梦梦.png"
    }
]

# 生成函数
def generate_avatar(char):
    print(f"\n{'='*60}")
    print(f"正在生成：{char['name']}")
    print(f"配色：{char['colors']}")
    print(f"性格：{char['personality']}")
    print(f"{'='*60}")
    
    ENDPOINT = f"{BASE_URL}/models/{MODEL}:generateContent"
    
    try:
        response = requests.post(
            ENDPOINT,
            headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": char['prompt']}]
                }],
                "generationConfig": {
                    "responseModalities": ["IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "1:1"
                    }
                }
            },
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            parts = data["candidates"][0]["content"]["parts"]
            for part in parts:
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    image_bytes = base64.b64decode(image_data)
                    
                    # 保存图片
                    os.makedirs("avatars", exist_ok=True)
                    img_path = f"avatars/{char['filename']}"
                    with open(img_path, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"✅ 生成成功！")
                    print(f"📁 保存路径：{img_path}")
                    print(f"📊 文件大小：{len(image_bytes) / 1024 / 1024:.2f} MB")
                    return True
            print(f"❌ 生成失败：无图片数据返回")
            return False
        else:
            print(f"❌ 生成失败：HTTP {response.status_code}")
            print(f"错误信息：{response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 生成异常：{str(e)}")
        return False

# 执行生成
print("🚀 开始生成7个角色的专属头像...")
print(f"🤖 使用模型：{MODEL}")
print(f"🎨 风格：统一治愈系扁平插画")

results = []
for char in characters:
    success = generate_avatar(char)
    results.append({
        "name": char['name'],
        "status": "成功" if success else "失败",
        "path": f"avatars/{char['filename']}" if success else ""
    })

# 汇总输出
print(f"\n{'='*60}")
print("📋 头像生成结果汇总")
print(f"{'='*60}")
success_count = sum(1 for r in results if r['status'] == "成功")
for r in results:
    print(f"🎨 {r['name']} + {r['status']}")
    if r['path']:
        print(f"   📁 {r['path']}")

print(f"\n✅ 生成完成！成功 {success_count}/7 个头像")
print(f"📂 所有头像保存在：/Users/huanxi/.openclaw/workspace-shejiguan/avatars/")
