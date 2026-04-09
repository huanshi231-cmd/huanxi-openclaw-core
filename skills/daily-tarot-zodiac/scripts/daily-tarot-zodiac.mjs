#!/usr/bin/env node
/**
 * 每日星座塔罗能量脚本
 * 
 * 日期 → 塔罗大牌 → 星座 → 守护行星
 * 三层联动解读
 */

import dayjs from "dayjs";
import { MAJOR_ARCANA, TAROT_MEANINGS, ZODIAC_MEANINGS, PLANET_MEANINGS, TAROT_ZODIAC_MAP } from "./base-data.mjs";

// 日期→塔罗数字
function dateToTarot(dateStr) {
    let num = dateStr.replace(/-/g, '').split('').reduce((a, b) => a + parseInt(b), 0);
    while (num > 21) {
        num = num.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return num;
}

// 计算过程描述
function getCalculationSteps(dateStr) {
    let num = dateStr.replace(/-/g, '').split('').reduce((a, b) => a + parseInt(b), 0);
    const steps = [num];
    while (num > 21) {
        num = num.toString().split('').reduce((a, b) => a + parseInt(b), 0);
        steps.push(num);
    }
    return steps;
}

// 生成整体定性
function generateOverallTheme(card, sign, planet) {
    const tarotE = TAROT_MEANINGS[card];
    const zodiacE = ZODIAC_MEANINGS[sign];
    const planetE = PLANET_MEANINGS[planet];
    
    // 生成一句话定性
    const themes = [
        `今天是一种"${zodiacE.essence}"的能量...`,
        `塔罗的${card}说：${tarotE.essence}...`,
        `加上${sign}座的特质：${zodiacE.energy}...`,
        `行星${planet}在推动：${planetE.energy}...`
    ];
    
    return themes.join('\n\n');
}

// 生成完整解读
function generateFullInterpretation(card, sign, planet) {
    const tarotE = TAROT_MEANINGS[card];
    const zodiacE = ZODIAC_MEANINGS[sign];
    const planetE = PLANET_MEANINGS[planet];
    
    let output = '';
    
    // 整体定性
    output += `今天是一种"${zodiacE.essence}"的能量。\n\n`;
    
    // 塔罗层
    output += `🔮 ${card}\n`;
    output += `牌意：${tarotE.essence}。\n`;
    output += `能量：${tarotE.energy}。\n`;
    output += `行动：${tarotE.action}。\n\n`;
    
    // 星座层
    output += `♈ ${sign}座\n`;
    output += `本质：${zodiacE.essence}。\n`;
    output += `能量：${zodiacE.energy}。\n`;
    output += `行动：${zodiacE.action}。\n\n`;
    
    // 行星层
    output += `🪐 ${planet}\n`;
    output += `本质：${planetE.essence}。\n`;
    output += `能量：${planetE.energy}。\n`;
    output += `行动：${planetE.action}。\n\n`;
    
    // 综合行动指引
    output += `⚡ 今日行动指引：\n`;
    output += `✅ 适合：${tarotE.action}；同时${zodiacE.action}。\n`;
    output += `❌ 忌讳：${tarotE.avoid}；也避免${zodiacE.avoid}。\n`;
    
    return output;
}

function generateDailyContent(date = dayjs().format('YYYY-MM-DD')) {
    const idx = dateToTarot(date);
    const steps = getCalculationSteps(date);
    const card = MAJOR_ARCANA[idx];
    const mapping = TAROT_ZODIAC_MAP[card];
    const sign = mapping.sign;
    const planet = mapping.planet;
    
    // 构建计算过程描述
    const dateNums = date.replace(/-/g, '').split('');
    const calcStr = dateNums.join(' + ') + ' = ' + steps.join(' → ');
    
    return {
        date: date,
        calculation: calcStr,
        tarotIndex: idx,
        tarotCard: card,
        sign: sign,
        planet: planet,
        interpretation: generateFullInterpretation(card, sign, planet),
        raw: {
            tarot: TAROT_MEANINGS[card],
            zodiac: ZODIAC_MEANINGS[sign],
            planet: PLANET_MEANINGS[planet]
        }
    };
}

function main() {
    const args = process.argv.slice(2);
    let date = dayjs().format('YYYY-MM-DD');
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--date' && args[i + 1]) {
            date = args[i + 1];
        }
    }
    
    const result = generateDailyContent(date);
    
    // 友好输出
    console.log('═══════════════════════════════════');
    console.log(`      【今日能量】${result.tarotCard}·${result.sign}座·${result.planet}`);
    console.log('═══════════════════════════════════');
    console.log('');
    console.log(`📅 日期：${result.date}`);
    console.log(`🔢 计算：${result.calculation}`);
    console.log('');
    console.log(result.interpretation);
}

main();
