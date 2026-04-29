import os
import requests
import json
import base64

# 配置 - 使用Gemini原生API
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"
MODEL = "gemini-3.1-flash-image-preview"
ENDPOINT = f"{BASE_URL}/models/{MODEL}:generateContent"

# 封面提示词
prompt = """
Generate a WeChat official account cover image:
1. Content: realistic cinematic photography, back view of a modern Asian woman sitting alone by floor-to-ceiling window, outside is purple-toned city dusk, soft purple halo envelops the whole scene, warm yellow indoor light illuminates character's outline from the side, character's posture is quiet and peaceful, healing and melancholic atmosphere
2. Composition: simple, plenty of blank space at the top and bottom of the image for adding text later
3. Color tone: healing purple #9370DB as main color
4. Style: 4K HD, cinematic texture, emotional healing style
5. Important: no text, no subtitles, pure image
6. Size: 1280x720 pixels, 16:9 aspect ratio
"""

print(f"使用模型：{MODEL}")
print("正在生成公众号封面图...")

try:
    response = requests.post(
        ENDPOINT,
        headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": "16:9"
                }
            }
        }
    )
    
    print(f"响应状态码：{response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # 提取图片数据
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                image_data = part["inlineData"]["data"]
                image_bytes = base64.b64decode(image_data)
                
                # 保存图片
                os.makedirs("generated_images", exist_ok=True)
                img_path = "generated_images/cover_gemini_final.png"
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                print(f"封面生成成功！")
                print(f"使用模型：{MODEL}")
                print(f"本地路径：{img_path}")
                
                # 保存结果
                with open("generated_images/cover_gemini_final_result.json", "w") as f:
                    json.dump({
                        "model_used": MODEL,
                        "local_path": img_path,
                        "prompt": prompt
                    }, f, ensure_ascii=False, indent=2)
                    
                break
    else:
        print(f"生成失败：{response.text}")
except Exception as e:
    print(f"生成出错：{str(e)}")
    import traceback
    traceback.print_exc()
