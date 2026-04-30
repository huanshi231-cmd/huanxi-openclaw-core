#!/usr/bin/env node
/**
 * 塔罗占星每日能量脚本
 * 日期数字相加 → 塔罗大牌0-21 → 占星符号/行星
 */

import dayjs from "dayjs";

// 塔罗大牌0-21 与占星对应（标准韦特顺序）
const TAROT_ZODIAC_MAP = [
    { card: "愚人", planet: "天王星", sign: "风象", meaning: "自由、冒险、新开始" },        // 0
    { card: "魔术师", planet: "水星", sign: "双子", meaning: "创造、沟通、资源" },          // 1
    { card: "女祭司", planet: "月亮", sign: "巨蟹", meaning: "直觉、内在、秘密" },           // 2
    { card: "女皇", planet: "金星", sign: "金牛", meaning: "滋养、丰盛、感官" },             // 3
    { card: "皇帝", planet: "火星", sign: "白羊", meaning: "掌控、架构、领导" },             // 4
    { card: "教皇", planet: "木星", sign: "射手", meaning: "智慧、信念、指引" },             // 5
    { card: "恋人", planet: "金星", sign: "双子", meaning: "选择、关系、合一" },            // 6
    { card: "战车", planet: "火星", sign: "白羊", meaning: "意志、胜利、行动" },             // 7
    { card: "力量", planet: "太阳", sign: "狮子", meaning: "勇气、耐心、内在力量" },         // 8
    { card: "隐士", planet: "水星", sign: "处女", meaning: "内省、孤独、智慧" },             // 9
    { card: "命运之轮", planet: "木星", sign: "射手", meaning: "转变、循环、时机" },         // 10
    { card: "正义", planet: "金星", sign: "天秤", meaning: "平衡、因果、真理" },             // 11
    { card: "吊人", planet: "海王星", sign: "双鱼", meaning: "牺牲、接纳、视角" },           // 12
    { card: "死神", planet: "冥王星", sign: "天蝎", meaning: "结束、转化、重生" },           // 13
    { card: "节制", planet: "太阳", sign: "射手", meaning: "平衡、调和、净化" },             // 14
    { card: "恶魔", planet: "土星", sign: "摩羯", meaning: "束缚、欲望、物质" },             // 15
    { card: "高塔", planet: "火星", sign: "白羊", meaning: "突变、解放、觉醒" },             // 16
    { card: "星星", planet: "天王星", sign: "水瓶", meaning: "希望、灵感、星光" },           // 17
    { card: "月亮", planet: "月亮", sign: "双鱼", meaning: "幻象、恐惧、潜意识" },            // 18
    { card: "太阳", planet: "太阳", sign: "狮子", meaning: "喜悦、成功、生命" },             // 19
    { card: "审判", planet: "冥王星", sign: "天蝎", meaning: "清算、复兴、回应" },           // 20
    { card: "世界", planet: "土星", sign: "摩羯", meaning: "完成、整合、循环" }              // 21
];

// 默会知识风格解读
const INTERPRETATIONS = {
    "愚人": "有点像...你正站在一个边缘上。前面是什么还不知道，但是是时候抬脚了。",
    "魔术师": "有点像...你手里其实有牌，只是没意识到。今天在提醒你：资源是够的，缺的是第一个动作。",
    "女祭司": "有点像...有些东西在等着被听见。不是外面的声音，是里面的。今天适合静下来。",
    "女皇": "有点像...今天适合慢下来。不是懒，是需要滋养。吃点好的，待在舒服的地方。",
    "皇帝": "有点像...有些东西需要你来定。不是商量，是该你拍板的时候就拍。",
    "教皇": "有点像...今天有人在给你指路，或者你需要去问一个有经验的人。",
    "恋人": "有点像...今天有个选择要做。不是选对错，是选哪条路更靠近你想要的。",
    "战车": "有点像...你在推一件事，今天有进展。不用急，但要有方向。",
    "力量": "有点像...你比自己想的更有耐心。有些事不是用力气解决的，是用温度。",
    "隐士": "有点像...今天需要一个人待会儿。不是躲，是需要听听自己说什么。",
    "命运之轮": "有点像...你最近问的那些问题，快有答案了。不是你期待的那种，但是是该知道的。",
    "正义": "有点像...今天适合称一称。该面对的，今天有勇气面对。",
    "吊人": "有点像...有些事不是躺着就能解决的，但是也不需要急着动。有时候停下来看看也是一种动。",
    "死神": "有点像...某个阶段在结束。不是突然的，是慢慢到的。今天可能有个收尾。",
    "节制": "有点像...今天在找平衡。不是非黑即白，是找那个刚刚好的状态。",
    "恶魔": "有点像...有些东西在绑着你，但你假装没感觉到。今天可能会被戳到。",
    "高塔": "有点像...有些东西在崩。不是坏事——是早就该塌的，现在终于塌了。",
    "星星": "有点像...你之前丢了什么东西，不是物质上的。今天有机会再碰到。或者，只是想起来而已。",
    "月亮": "有点像...今天有些东西不太清晰。不是要急着看清楚，是要允许自己先感受。",
    "太阳": "有点像...你最近在找回那个发光的自己。今天在帮你——如果有什么事一直卡着，可以试着重新开始。",
    "审判": "有点像...今天有点像在清算。不是坏的清算，是那种这件事可以翻篇了的感觉。",
    "世界": "有点像...某个循环在完成。不是终点，是这一章该结尾了。下一章在等着你。"
};

function dateToTarotIndex(dateStr) {
    let num = dateStr.replace(/-/g, '').split('').reduce((a, b) => a + parseInt(b), 0);
    while (num > 21) {
        num = num.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return num;
}

function main() {
    const args = process.argv.slice(2);
    let date = dayjs().format("YYYY-MM-DD");
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === "--date" && args[i + 1]) {
            date = args[i + 1];
        }
    }
    
    const index = dateToTarotIndex(date);
    const info = TAROT_ZODIAC_MAP[index];
    const interpretation = INTERPRETATIONS[info.card] || "今天的能量在帮你找到方向。";
    
    console.log(JSON.stringify({
        date: date,
        tarotIndex: index,
        tarotCard: info.card,
        planet: info.planet,
        sign: info.sign,
        meaning: info.meaning,
        interpretation: interpretation
    }, null, 2));
}

main();
