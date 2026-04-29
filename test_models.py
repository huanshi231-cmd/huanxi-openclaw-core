import os
import requests
import json
import base64

# 配置
API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE_URL = "https://new.suxi.ai/v1beta"

# 测试提示词（简单无字封面）
test_prompt = "simple abstract purple background, soft gradient, minimalist style, no text, 1280x720"

def test_model(model_name):
    print(f"\n{'='*50}")
    print(f"测试模型：{model_name}")
    print(f"{'='*50}")
    
    ENDPOINT = f"{BASE_URL}/models/{model_name}:generateContent"
    
    try:
        response = requests.post(
            ENDPOINT,
            headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": test_prompt}]
                }],
                "generationConfig": {
                    "responseModalities": ["IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "16:9"
                    }
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                parts = data["candidates"][0]["content"]["parts"]
                has_image = any("inlineData" in part for part in parts)
                if has_image:
                    # 保存测试图片
                    for part in parts:
                        if "inlineData" in part:
                            image_data = part["inlineData"]["data"]
                            image_bytes = base64.b64decode(image_data)
                            os.makedirs("test_images", exist_ok=True)
                            img_path = f"test_images/{model_name}_test.png"
                            with open(img_path, "wb") as f:
                                f.write(image_bytes)
                            break
                    return (model_name, "成功", "正常生成图片")
                else:
                    return (model_name, "失败", "无图片返回")
            else:
                return (model_name, "失败", "响应格式异常")
        else:
            return (model_name, "失败", f"HTTP {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        return (model_name, "失败", f"异常：{str(e)[:50]}")

# 执行测试
print("开始模型测试...")
results = []

# 测试1
results.append(test_model("gemini-3.1-flash-image-preview"))

# 测试2
results.append(test_model("gemini-3-pro-image-preview"))

# 输出结果
print(f"\n{'='*50}")
print("测试结果汇总")
print(f"{'='*50}")
for model, status, reason in results:
    print(f"{model} + {status} + {reason}")

# 推荐
success_models = [r for r in results if r[1] == "成功"]
if len(success_models) == 2:
    print(f"\n推荐：gemini-3-pro-image-preview（画质更优，细节更丰富）")
elif len(success_models) == 1:
    print(f"\n推荐：{success_models[0][0]}")
else:
    print("\n无成功模型")
