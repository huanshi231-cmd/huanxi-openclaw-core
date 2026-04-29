import os
import requests
import json

# 配置 - 使用火山引擎统一路由
API_KEY = "59e227c0-b14c-4e31-b825-0ab44658de81"
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "google/gemini-3.1-flash-image-preview"

# 封面提示词
prompt = """
写实电影感摄影，现代亚洲女性独自坐在落地窗前的背影，窗外是紫色调的城市黄昏，柔和的紫色光晕笼罩整个画面，暖黄色的室内灯光从侧面打亮人物轮廓，人物姿态安静平和，氛围治愈忧伤，构图简洁，画面上方和下方大量留白适合后期加文字，治愈紫色调#9370DB为主色，4K高清，电影质感，情绪疗愈风格，无任何文字，无字幕
"""

print(f"使用模型：{MODEL}")
print("正在生成公众号封面图...")

try:
    response = requests.post(
        ENDPOINT,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "prompt": prompt,
            "size": "1280x720",
            "n": 1
        }
    )
    
    print(f"响应状态码：{response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        image_url = data["data"][0]["url"]
        # 下载图片
        os.makedirs("generated_images", exist_ok=True)
        img_response = requests.get(image_url)
        img_path = "generated_images/cover_gemini.png"
        with open(img_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"封面生成成功！")
        print(f"使用模型：{MODEL}")
        print(f"图片链接：{image_url}")
        print(f"本地路径：{img_path}")
        
        # 保存结果
        with open("generated_images/cover_gemini_result.json", "w") as f:
            json.dump({
                "model_used": MODEL,
                "image_url": image_url,
                "local_path": img_path,
                "prompt": prompt
            }, f, ensure_ascii=False, indent=2)
    else:
        print(f"生成失败：{response.text}")
except Exception as e:
    print(f"生成出错：{str(e)}")
