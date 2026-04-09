import sys
import os
os.chdir('/Users/huanxi/.openclaw/workspace-neirong')
sys.path.insert(0, '/Users/huanxi/.openclaw/workspace-neirong/skills/weixin-wechat-channel/scripts')
import auto_push_v7 as p

articles = [
    {
        "title": "爱你老己——那个受伤的内在小孩，等了你二十年",
        "input_file": "tmp/article_0409_01.md",
        "digest": "你骂自己最狠的地方，正是你最需要被爱的地方。那个等了二十年的内在小孩，值得被好好对待。"
    },
    {
        "title": "为什么你总是在关系里忍？不是善良，是不敢",
        "input_file": "tmp/article_0409_02.md",
        "digest": "忍不是美德，无底线地忍是对自我的慢性谋杀。真正的善良，是先照顾好自己。"
    },
    {
        "title": "拼豆、冥想、颂钵——成年人找回掌控感的3种温柔方式",
        "input_file": "tmp/article_0409_03.md",
        "digest": "在什么都抓不住的世界里，先抓住一点能抓住的东西。平静，是最强的能力。"
    }
]

for art in articles:
    print(f"\n{'='*50}")
    print(f"推文: {art['title']}")
    print(f"{'='*50}")
    sys.argv = [
        "auto_push_v7.py",
        art["title"],
        art["input_file"],
        art["digest"]
    ]
    try:
        p.main()
        print(f"✓ 成功")
    except Exception as e:
        print(f"✗ 失败: {e}")
