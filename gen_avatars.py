import os, requests, base64, time

API_KEY = "sk-1l0NzAe1KldcTJBFscJGcD4gi84e5iBtIkDz5iL5FSl1ykyS"
BASE = "https://new.suxi.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"
HEADER = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}

chars = [
    {"n":"太阳","c":"暖橙+米白","p":"治愈扁平插画1:1头像，圆润太阳形象带温柔微笑，橙光晕，右下角有'太'字小标识，暖橙#FFB344为主，米白为辅，无描边柔色块，无水印浅背景"},
    {"n":"灵夕","c":"淡紫+浅粉","p":"治愈扁平插画1:1头像，小仙女侧脸带星星发饰，周围飘星月牙，左上角有'灵'字小标识，淡紫#D4B2D8为主，浅粉为辅，无描边柔色块，无水印浅背景"},
    {"n":"蕊蕊","c":"樱花粉+奶白","p":"治愈扁平插画1:1头像，温柔女生侧脸别樱花，周围飘花瓣，右下角有'蕊'字小标识，樱花粉#FFB6C1为主，奶白为辅，无描边柔色块，无水印浅背景"},
    {"n":"跳跳","c":"亮黄+天蓝","p":"治愈扁平插画1:1头像，活泼形象大笑跳跃，周围有小闪电，左下角有'跳'字小标识，亮黄#FFE066为主，天蓝为辅，无描边柔色块，无水印浅背景"},
    {"n":"朵朵","c":"水绿+鹅黄","p":"治愈扁平插画1:1头像，花朵精灵顶小雏菊，周围有花瓣画笔，右上角有'朵'字小标识，水绿#98D8C8为主，鹅黄为辅，无描边柔色块，无水印浅背景"},
    {"n":"光头强","c":"深蓝+灰","p":"治愈扁平插画1:1头像，稳重戴眼镜光头形象，周围有小齿轮，左下角有'强'字小标识，深蓝#4A6FA5为主，灰色为辅，无描边柔色块，无水印浅背景"},
    {"n":"梦梦","c":"浅紫+淡蓝","p":"治愈扁平插画1:1头像，云朵精灵温柔微笑，周围有星光碎片，右下角有'梦'字小标识，浅紫#E6E6FA为主，淡蓝为辅，无描边柔色块，无水印浅背景"}
]

os.makedirs("avatars", exist_ok=True)
res = []

for i, c in enumerate(chars):
    print(f"\n[{i+1}/7] 生成 {c['n']} ({c['c']})...")
    try:
        r = requests.post(BASE, headers=HEADER, json={
            "contents": [{"parts": [{"text": c['p']}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}
        }, timeout=90)
        if r.status_code == 200:
            parts = r.json()["candidates"][0]["content"]["parts"]
            for p in parts:
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    path = f"avatars/avatar_{c['n']}.png"
                    with open(path, "wb") as f: f.write(img)
                    res.append(f"✅ {c['n']}: {path} ({len(img)/1024/1024:.1f}MB)")
                    print(f"✅ 成功")
                    break
            else:
                res.append(f"❌ {c['n']}: 无图片返回")
                print(f"❌ 失败")
        else:
            res.append(f"❌ {c['n']}: HTTP {r.status_code}")
            print(f"❌ 失败")
    except Exception as e:
        res.append(f"❌ {c['n']}: {str(e)[:30]}")
        print(f"❌ 异常: {str(e)[:30]}")
    time.sleep(2)

print("\n" + "="*50)
print("📋 生成结果汇总")
print("="*50)
for line in res: print(line)
print(f"\n✅ 成功 {sum(1 for l in res if '✅' in l)}/7")
print("📂 保存路径: /Users/huanxi/.openclaw/workspace-shejiguan/avatars/")
