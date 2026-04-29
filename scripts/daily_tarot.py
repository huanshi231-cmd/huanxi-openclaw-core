#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日塔罗能量生成脚本
计算规则：日期数字相加 → 数字根（各位相加直到1-22）→ 对应塔罗牌
"""

import datetime
import sys

# 塔罗牌对应表（22张大阿卡纳）
TAROT_CARDS = {
    1: {"name": "愚者", "zodiac": "天王星", "element": "风", "keywords": ["冒险", "新开始", "信任"]},
    2: {"name": "女祭司", "zodiac": "月亮", "element": "水", "keywords": ["直觉", "智慧", "内在声音"]},
    3: {"name": "皇后", "zodiac": "金星", "element": "土", "keywords": ["丰饶", "母性", "创造力"]},
    4: {"name": "皇帝", "zodiac": "白羊座", "element": "火", "keywords": ["权威", "结构", "领导力"]},
    5: {"name": "教皇", "zodiac": "金牛座", "element": "土", "keywords": ["传统", "信仰", "指导"]},
    6: {"name": "恋人", "zodiac": "双子座", "element": "风", "keywords": ["选择", "爱", "和谐"]},
    7: {"name": "战车", "zodiac": "巨蟹座", "element": "水", "keywords": ["意志力", "突破瓶颈", "内外平衡"]},
    8: {"name": "力量", "zodiac": "狮子座", "element": "火", "keywords": ["勇气", "耐心", "内在力量"]},
    9: {"name": "隐士", "zodiac": "处女座", "element": "土", "keywords": ["内省", "寻找", "智慧"]},
    10: {"name": "命运之轮", "zodiac": "木星", "element": "火", "keywords": ["变化", "命运", "转折点"]},
    11: {"name": "正义", "zodiac": "天秤座", "element": "风", "keywords": ["公平", "真相", "因果"]},
    12: {"name": "倒吊人", "zodiac": "海王星", "element": "水", "keywords": ["放下", "新视角", "牺牲"]},
    13: {"name": "死神", "zodiac": "天蝎座", "element": "水", "keywords": ["转变", "结束", "重生"]},
    14: {"name": "节制", "zodiac": "射手座", "element": "火", "keywords": ["平衡", "耐心", "调和"]},
    15: {"name": "恶魔", "zodiac": "摩羯座", "element": "土", "keywords": ["束缚", "阴影", "释放"]},
    16: {"name": "塔", "zodiac": "火星", "element": "火", "keywords": ["突破", "觉醒", "解放"]},
    17: {"name": "星星", "zodiac": "水瓶座", "element": "风", "keywords": ["希望", "灵感", "疗愈"]},
    18: {"name": "月亮", "zodiac": "双鱼座", "element": "水", "keywords": ["直觉", "梦境", "潜意识"]},
    19: {"name": "太阳", "zodiac": "太阳", "element": "火", "keywords": ["喜悦", "成功", "活力"]},
    20: {"name": "审判", "zodiac": "冥王星", "element": "火", "keywords": ["觉醒", "重生", "召唤"]},
    21: {"name": "世界", "zodiac": "土星", "element": "土", "keywords": ["完成", "整合", "成就"]},
    22: {"name": "愚者", "zodiac": "天王星", "element": "风", "keywords": ["冒险", "新开始", "信任"]}
}

# 星座能量提示
ZODIAC_GUIDANCE = {
    "白羊座": "🦁 白羊能量提示：今天适合主动出击，你的行动力就是最好的护身符。",
    "金牛座": "🌿 金牛能量提示：慢下来，安全感在你稳稳的每一步里。",
    "双子座": "💨 双子能量提示：多与人交流，信息里藏着你要的答案。",
    "巨蟹座": "🦀 巨蟹座能量提示：\n情绪不是弱点，是你的导航系统。今天如果感到莫名的焦灼或想哭，别压抑——那是旧模式在离开，新身份在就位。",
    "狮子座": "🦁 狮子能量提示：大方展现自己，你的光芒会照亮前路。",
    "处女座": "🌾 处女能量提示：细节里有魔鬼也有天使，保持觉察但不焦虑。",
    "天秤座": "⚖️ 天秤能量提示：平衡不是妥协，是知道自己真正要什么。",
    "天蝎座": "🦂 天蝎能量提示：深刻的转化正在发生，信任黑暗后的光明。",
    "射手座": "🏹 射手能量提示：保持好奇，远方的风景等你去探索。",
    "摩羯座": "🏔️ 摩羯能量提示：一步一个脚印，时间会给你最好的答案。",
    "水瓶座": "🌊 水瓶能量提示：你的独特就是你的天赋，不必从众。",
    "双鱼座": "🐟 双鱼能量提示：连接你的直觉，梦境里有重要讯息。",
    "太阳": "☀️ 太阳能量提示：做自己，发光是你的本能。",
    "月亮": "🌙 月亮能量提示：倾听内在声音，情绪是灵魂的语言。",
    "水星": "☿ 水星能量提示：清晰表达，好好说话就是最好的魔法。",
    "金星": "♀ 金星能量提示：爱自己，然后爱这个世界。",
    "火星": "♂ 火星能量提示：你的愤怒里藏着力量，善用它。",
    "木星": "♃ 木星能量提示：保持乐观，幸运站在你这边。",
    "土星": "♄ 土星能量提示：限制是伪装的祝福，耐心等待收获。",
    "天王星": "♅ 天王星能量提示：拥抱变化，惊喜就在转角。",
    "海王星": "♆ 海王星能量提示：相信你的想象力，灵性在指引你。",
    "冥王星": "♇ 冥王星能量提示：深度蜕变后，你会是全新的自己。"
}

def calculate_card_number(date_str=None):
    """根据日期计算塔罗牌数字（数字根算法）"""
    if date_str is None:
        today = datetime.date.today()
    else:
        today = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # 把日期所有数字相加
    date_digits = today.strftime("%Y%m%d")  # 例如 "20260429"
    total = sum(int(d) for d in date_digits)
    
    # 数字根算法：各位相加直到结果在1-22之间
    while total > 22:
        total = sum(int(d) for d in str(total))
    
    return total, today

def generate_content(date_str=None):
    """生成完整的每日塔罗内容"""
    card_num, date = calculate_card_number(date_str)
    card = TAROT_CARDS[card_num]
    
    date_str = date.strftime("%m.%d")
    card_name = card["name"]
    zodiac = card["zodiac"]
    keywords = "、".join(card["keywords"])
    
    # 获取星座提示
    zodiac_guidance = ZODIAC_GUIDANCE.get(zodiac, f"✨ {zodiac}能量提示：保持觉察，宇宙在指引你。")
    
    # 战车牌特殊处理
    if card_num == 7:
        content = f"""🌙 {date_str} 宇宙能量指引 | 战车牌：你的勇气正在显化奇迹

今日宇宙开出「战车牌」，月亮守护的巨蟹座能量全速流动——
✨ 今日关键词：{keywords}

你最近卡在某个十字路口的事，今天会出现清晰答案。不是外界给你，是你内心深处终于敢承认自己真正想要什么。

{zodiac_guidance}

💫 行动指引：
1. 开车/通勤时专注当下，战车牌提醒你握好自己的方向盘
2. 跟母亲或女性长辈连线，她们无意中的一句话会点醒你
3. 穿白色或银色衣服，增强月亮疗愈能量

今日 affirmation："我的每一步都在正确的轨道上，宇宙为我开路。"

#大众塔罗 #每日能量 #巨蟹座 #战车牌 #女性成长 #宇宙指引 #疗愈
"""
    else:
        # 通用三段式模板
        content = f"""🌙 {date_str} 宇宙能量指引 | {card_name}牌：你的{card['keywords'][0]}正在发光

【今日宇宙能量】
今日宇宙开出「{card_name}牌」，{zodiac}能量全速流动——
✨ 今日关键词：{keywords}

你最近放在心上的事，今天会有新的视角。不是外界给你答案，是你内心深处终于听见了真实的声音。

{zodiac_guidance}

【每日征兆指引】
💫 今日行动练习：
1. 给自己一个拥抱，告诉自己「你做得很好」
2. 做三次深呼吸，把焦虑呼出，把平静吸入
3. 穿{card['element']}色系衣服（风：浅蓝/灰白 | 水：深蓝/黑色 | 火：红色/橙色 | 土：绿色/棕色），增强元素疗愈能量

【欢喜疗愈视角】
每一张牌都没有「好」「坏」，宇宙只是在告诉你：现在你需要这份能量。
{card_name}邀请你今天更加{card['keywords'][0]}，因为你本来就拥有这份力量。

今日 affirmation："我的每一步都在正确的轨道上，宇宙为我开路。"

#大众塔罗 #每日能量 #{zodiac} #{card_name} #女性成长 #宇宙指引 #疗愈
"""
    return content

if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    content = generate_content(date_arg)
    print(content)
