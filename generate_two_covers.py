import os
import requests
import json
import base64

# 配置
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3-pro-image-preview"

# 设计官Prompt模板生成的提示词
prompts = [
    {
        "name": "cover_v1_暖紫色治愈风",
        "prompt": """
        【核心主体】一位温柔的亚洲女生侧影，安静坐在落地窗边
        【具体动作】双手捧着一杯热饮，杯口有淡淡的热气升腾
        【构图参数】1280×720像素，16:9比例，画面上方30%和下方30%区域完全留白，人物居中偏下
        【光影描述】下午柔和的金色阳光从窗外斜洒进来，形成丁达尔效应，暖紫色光晕笼罩整个场景，光影过渡自然柔和
        【色彩系统】主色：暖紫色#B48EAD，辅助色：米白色#F5F0EB，点缀色：金色阳光，整体低饱和度治愈色调
        【风格参考】写实摄影，电影感柔焦，ins风治愈系，高质感
        【尺寸分辨率】1280×720，300DPI
        【负面约束词】无文字，无水印，无logo，无多余装饰，无畸变，人物面部清晰自然
        """,
        "filename": "cover_v1_暖紫色治愈风.png"
    },
    {
        "name": "cover_v2_极简莫兰迪风",
        "prompt": """
        【核心主体】一本打开的空白笔记本，旁边放着一朵新鲜的小雏菊
        【具体动作】笔记本平放在浅色桌面上，小雏菊自然斜靠在笔记本边缘，花瓣舒展
        【构图参数】1280×720像素，16:9比例，画面上方40%和下方30%区域完全留白，主体居中偏下，极简构图
        【光影描述】柔和的漫射自然光，从正上方打下来，形成柔和的阴影，无硬边阴影
        【色彩系统】莫兰迪低饱和色系：笔记本米白色#F8F6F3，雏菊奶白色+鹅黄色花蕊，桌面浅卡其色#E8E4DE，整体色调统一柔和
        【风格参考】极简主义，莫兰迪色系，ins风静物摄影，干净高级，留白艺术
        【尺寸分辨率】1280×720，300DPI
        【负面约束词】无文字，无水印，无logo，无其他杂物，无多余元素，画面干净整洁
        """,
        "filename": "cover_v2_极简莫兰迪风.png"
    }
]

# 生成函数
def generate_cover(prompt_info):
    print(f"\n{'='*60}")
    print(f"正在生成：{prompt_info['name']}")
    print(f"使用模型：{MODEL}")
    print(f"{'='*60}")
    
    ENDPOINT = f"{BASE_URL}/models/{MODEL}:generateContent"
    
    try:
        response = requests.post(
            ENDPOINT,
            headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": prompt_info['prompt']}]
                }],
                "generationConfig": {
                    "responseModalities": ["IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "16:9"
                    }
                }
            },
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            parts = data["candidates"][0]["content"]["parts"]
            for part in parts:
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    image_bytes = base64.b64decode(image_data)
                    
                    # 保存图片
                    os.makedirs("final_covers", exist_ok=True)
                    img_path = f"final_covers/{prompt_info['filename']}"
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
print("🚀 开始生成2版公众号封面图...")
print(f"🤖 使用模型：{MODEL}")

results = []
for p in prompts:
    success = generate_cover(p)
    results.append({
        "name": p['name'],
        "status": "成功" if success else "失败",
        "path": f"final_covers/{p['filename']}" if success else ""
    })

# 汇总输出
print(f"\n{'='*60}")
print("📋 生成结果汇总")
print(f"{'='*60}")
for r in results:
    print(f"🎨 {r['name']} + {r['status']}")
    if r['path']:
        print(f"   📁 {r['path']}")

print(f"\n✅ 全部生成完成！")
