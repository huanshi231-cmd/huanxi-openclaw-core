import os
import requests
import json

# 配置
API_KEY = "59e227c0-b14c-4e31-b825-0ab44658de81"
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "doubao-seedream-4-0-250828"

# 提示词列表
prompts = [
    {
        "name": "image1",
        "prompt": "现代家庭餐厅场景，一对夫妻对坐在长餐桌两端，各自低头看手机，没有任何交流，餐桌成为视觉分割线，冷灰色调，柔和自然光，写实风格，氛围沉默压抑，治愈紫色调点缀，画面下方预留文案位置",
        "size": "1280x720"
    },
    {
        "name": "image2",
        "prompt": "现代客厅场景，一张米色双人沙发，只有一个女人孤单地坐着，另一半位置空着，放着一件男士外套，背景是模糊的落地窗，暖黄色调，柔和光影，写实风格，氛围安静孤独，治愈紫色调点缀，画面下方预留文案位置",
        "size": "1280x720"
    }
]

# 创建保存目录
os.makedirs("generated_images", exist_ok=True)

# 生成图片
results = []
for item in prompts:
    print(f"正在生成 {item['name']}...")
    try:
        response = requests.post(
            ENDPOINT,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "prompt": item["prompt"],
                "size": item["size"],
                "n": 1
            }
        )
        if response.status_code == 200:
            data = response.json()
            image_url = data["data"][0]["url"]
            # 下载图片
            img_response = requests.get(image_url)
            img_path = f"generated_images/{item['name']}.png"
            with open(img_path, "wb") as f:
                f.write(img_response.content)
            results.append({
                "name": item["name"],
                "url": image_url,
                "local_path": img_path
            })
            print(f"{item['name']} 生成成功：{img_path}")
        else:
            print(f"{item['name']} 生成失败：{response.text}")
    except Exception as e:
        print(f"{item['name']} 生成出错：{str(e)}")

# 保存结果
with open("generated_images/results.json", "a") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("剩余图片生成完成！")
