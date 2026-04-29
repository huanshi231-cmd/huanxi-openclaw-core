import os
import requests
import json

# 配置
API_KEY = "59e227c0-b14c-4e31-b825-0ab44658de81"
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "doubao-seedream-4-0-250828"

# 提示词列表（20张，水晶/星空/自然/脉轮/花卉/光能量主题）
prompts = [
    # 水晶主题（4张）
    {
        "name": "crystal_amethyst_cluster",
        "prompt": "高清紫水晶簇，柔和暖光照射，通透质感，黑色背景，疗愈能量风，无水印，免费商用风格",
        "size": "1024x1024"
    },
    {
        "name": "crystal_ball_rainbow",
        "prompt": "透明水晶球，内部折射彩虹光效，放在木质桌面上，柔和自然光，静谧氛围，高清",
        "size": "1024x1024"
    },
    {
        "name": "crystal_collection_arranged",
        "prompt": "多种水晶矿石排列，紫水晶、白水晶、粉晶，白色背景，干净整洁，疗愈风格",
        "size": "1024x1024"
    },
    {
        "name": "crystal_cave_inside",
        "prompt": "水晶洞内部，紫色晶簇，微光闪烁，特写镜头，质感细腻，高清",
        "size": "1024x1024"
    },
    # 星空主题（4张）
    {
        "name": "starry_galaxy_sky",
        "prompt": "银河星空，深蓝色夜空，繁星点点，静谧氛围，无地面景物，高清，治愈风",
        "size": "1024x1024"
    },
    {
        "name": "aurora_starry_sky",
        "prompt": "极光星空，绿色和紫色极光交织，雪地背景，梦幻氛围，高清",
        "size": "1024x1024"
    },
    {
        "name": "starry_night_forest",
        "prompt": "星夜森林，头顶是璀璨星空，下方是黑色森林剪影，神秘治愈风格",
        "size": "1024x1024"
    },
    {
        "name": "meteor_night_sky",
        "prompt": "流星划过夜空，深蓝色背景，金色流星轨迹，静谧氛围，高清",
        "size": "1024x1024"
    },
    # 自然主题（4张）
    {
        "name": "forest_morning_fog",
        "prompt": "清晨森林雾气，阳光穿透树叶，丁达尔效应，绿色调，治愈自然风景，高清",
        "size": "1024x1024"
    },
    {
        "name": "mountain_waterfall",
        "prompt": "山间瀑布，水流清澈，周围是绿色植被，柔和光线，静谧氛围，高清",
        "size": "1024x1024"
    },
    {
        "name": "beach_sunset",
        "prompt": "海边日落，粉色和橙色天空，海浪轻轻拍岸，温暖治愈风格，高清",
        "size": "1024x1024"
    },
    {
        "name": "spring_flower_field",
        "prompt": "春日花海，白色和粉色小花铺满地面，柔和阳光，清新自然，高清",
        "size": "1024x1024"
    },
    # 脉轮主题（3张）
    {
        "name": "seven_chakra_energy_balls",
        "prompt": "七脉轮彩色能量球，垂直排列，柔和发光效果，黑色背景，灵性疗愈风格，高清",
        "size": "1024x1024"
    },
    {
        "name": "chakra_symbols_glowing",
        "prompt": "脉轮符号发光，七种颜色对应不同脉轮，简约设计，白色背景，干净清晰",
        "size": "1024x1024"
    },
    {
        "name": "human_chakra_energy",
        "prompt": "人体脉轮能量图，侧身剪影，七个脉轮位置发光，柔和光效，灵性风格",
        "size": "1024x1024"
    },
    # 花卉主题（3张）
    {
        "name": "pink_lotus_water",
        "prompt": "粉色莲花，水面倒影，柔和晨光，露珠点缀，疗愈纯净风格，高清",
        "size": "1024x1024"
    },
    {
        "name": "white_lily_elegant",
        "prompt": "白色百合，深色背景，柔和侧光，优雅静谧，治愈风格",
        "size": "1024x1024"
    },
    {
        "name": "lavender_field_sunny",
        "prompt": "紫色薰衣草花海，阳光照射，微风拂过，温馨治愈，高清",
        "size": "1024x1024"
    },
    # 光能量主题（2张）
    {
        "name": "gold_light_particles",
        "prompt": "金色光粒子流动，抽象能量背景，温暖柔和，无具体物体，疗愈风格，高清",
        "size": "1024x1024"
    },
    {
        "name": "rainbow_energy_vortex",
        "prompt": "七彩光效漩涡，抽象能量流动，柔和渐变，灵性治愈风格，高清",
        "size": "1024x1024"
    }
]

# 创建保存目录
os.makedirs("linggan_images_20260428", exist_ok=True)

# 生成图片
results = []
success_count = 0
fail_count = 0

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
            img_path = f"linggan_images_20260428/{item['name']}.jpg"
            with open(img_path, "wb") as f:
                f.write(img_response.content)
            results.append({
                "name": item["name"],
                "url": image_url,
                "local_path": img_path
            })
            success_count += 1
            print(f"{item['name']} 生成成功：{img_path}")
        else:
            fail_count += 1
            print(f"{item['name']} 生成失败：{response.text}")
    except Exception as e:
        fail_count += 1
        print(f"{item['name']} 生成出错：{str(e)}")

# 保存结果
with open("linggan_images_20260428/results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n生成完成！成功：{success_count} 张，失败：{fail_count} 张")
