import os
import requests
import json
import base64

# 配置 - 使用火山引擎chat completions接口
API_KEY = "59e227c0-b14c-4e31-b825-0ab44658de81"
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = "google/gemini-3.1-flash-image-preview"

# 封面提示词
prompt = """
请生成一张公众号封面图，要求：
1. 内容：写实电影感摄影，现代亚洲女性独自坐在落地窗前的背影，窗外是紫色调的城市黄昏，柔和的紫色光晕笼罩整个画面，暖黄色的室内灯光从侧面打亮人物轮廓，人物姿态安静平和，氛围治愈忧伤
2. 构图：简洁，画面上方和下方大量留白适合后期加文字
3. 色调：治愈紫色调#9370DB为主色
4. 风格：4K高清，电影质感，情绪疗愈风格
5. 重要：无任何文字，无字幕，纯画面
6. 尺寸：1280x720像素，16:9比例

直接返回图片。
"""

print(f"使用模型：{MODEL}")
print("正在生成公众号封面图...")

try:
    response = requests.post(
        ENDPOINT,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000
        }
    )
    
    print(f"响应状态码：{response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容：{json.dumps(data, ensure_ascii=False, indent=2)}")
        
        # 尝试提取图片
        content = data["choices"][0]["message"]["content"]
        print(f"返回内容类型：{type(content)}")
        
        # 保存结果
        os.makedirs("generated_images", exist_ok=True)
        with open("generated_images/cover_gemini_response.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    else:
        print(f"生成失败：{response.text}")
except Exception as e:
    print(f"生成出错：{str(e)}")
