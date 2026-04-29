#!/usr/bin/env node
/**
 * Token 统计追踪器
 * 基于 Claude Code cost-tracker.ts 五维Token模型
 * 
 * 用法:
 *   node track.js add --input 5000 --output 3000 --cache-read 1000 --cache-write 500 --cost 0.05 --model MiniMax-M2
 *   node track.js show --period today|week|month
 *   node track.js by-model
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'token-stats');
const DATA_FILE = path.join(DATA_DIR, 'usage.json');
const DAYS_TO_KEEP = 90;

// 确保目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 加载数据
function loadData() {
  if (!fs.existsSync(DATA_FILE)) {
    return { sessions: {}, models: {}, lastUpdated: null };
  }
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  } catch (e) {
    return { sessions: {}, models: {}, lastUpdated: null };
  }
}

// 保存数据
function saveData(data) {
  data.lastUpdated = new Date().toISOString();
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// 获取今天的日期字符串
function today() {
  return new Date().toISOString().split('T')[0];
}

// 清理旧数据
function cleanOldData(data) {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - DAYS_TO_KEEP);
  const cutoffStr = cutoff.toISOString().split('T')[0];
  
  for (const date in data.sessions) {
    if (date < cutoffStr) {
      delete data.sessions[date];
    }
  }
  return data;
}

// 添加记录
function addRecord(inputTokens, outputTokens, cacheReadTokens, cacheWriteTokens, webSearch, cost, model) {
  const data = loadData();
  const date = today();
  
  // 初始化当日数据
  if (!data.sessions[date]) {
    data.sessions[date] = {
      totalInput: 0,
      totalOutput: 0,
      totalCacheRead: 0,
      totalCacheWrite: 0,
      totalWebSearch: 0,
      totalCost: 0,
      conversationCount: 0,
      byModel: {}
    };
  }
  
  const session = data.sessions[date];
  session.totalInput += inputTokens || 0;
  session.totalOutput += outputTokens || 0;
  session.totalCacheRead += cacheReadTokens || 0;
  session.totalCacheWrite += cacheWriteTokens || 0;
  session.totalWebSearch += webSearch || 0;
  session.totalCost += cost || 0;
  session.conversationCount += 1;
  
  // 按模型统计
  if (!session.byModel[model]) {
    session.byModel[model] = {
      input: 0, output: 0, cacheRead: 0, cacheWrite: 0, cost: 0
    };
  }
  const modelStats = session.byModel[model];
  modelStats.input += inputTokens || 0;
  modelStats.output += outputTokens || 0;
  modelStats.cacheRead += cacheReadTokens || 0;
  modelStats.cacheWrite += cacheWriteTokens || 0;
  modelStats.cost += cost || 0;
  
  // 更新模型汇总
  if (!data.models[model]) {
    data.models[model] = { totalInput: 0, totalOutput: 0, totalCost: 0, lastUsed: null };
  }
  const modelTotal = data.models[model];
  modelTotal.totalInput += inputTokens || 0;
  modelTotal.totalOutput += outputTokens || 0;
  modelTotal.totalCost += cost || 0;
  modelTotal.lastUsed = date;
  
  saveData(cleanOldData(data));
  console.log(`✅ 记录已保存: ${date} | ${model} | input:${inputTokens} output:${outputTokens} cost:$${cost}`);
}

// 格式化数字
function fmt(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
  return String(n);
}

// 显示统计
function showStats(period) {
  const data = loadData();
  const now = new Date();
  
  let dates = [];
  if (period === 'today') {
    dates = [today()];
  } else if (period === 'week') {
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      dates.push(d.toISOString().split('T')[0]);
    }
  } else if (period === 'month') {
    for (let i = 29; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      dates.push(d.toISOString().split('T')[0]);
    }
  }
  
  // 汇总
  let totalInput = 0, totalOutput = 0, totalCacheRead = 0, totalCacheWrite = 0, totalCost = 0, totalConvos = 0;
  const byModel = {};
  const byDate = {};
  
  for (const date of dates) {
    const session = data.sessions[date];
    if (!session) continue;
    
    totalInput += session.totalInput || 0;
    totalOutput += session.totalOutput || 0;
    totalCacheRead += session.totalCacheRead || 0;
    totalCacheWrite += session.totalCacheWrite || 0;
    totalCost += session.totalCost || 0;
    totalConvos += session.conversationCount || 0;
    byDate[date] = session;
    
    for (const [model, stats] of Object.entries(session.byModel || {})) {
      if (!byModel[model]) byModel[model] = { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, cost: 0 };
      byModel[model].input += stats.input || 0;
      byModel[model].output += stats.output || 0;
      byModel[model].cacheRead += stats.cacheRead || 0;
      byModel[model].cacheWrite += stats.cacheWrite || 0;
      byModel[model].cost += stats.cost || 0;
    }
  }
  
  // 打印
  const periodName = period === 'today' ? '今日' : period === 'week' ? '本周' : '本月';
  console.log(`\n📊 ${periodName}Token统计`);
  console.log('═'.repeat(50));
  console.log(`  💬 对话次数: ${totalConvos}`);
  console.log(`  📥 输入Token: ${fmt(totalInput)}`);
  console.log(`  📤 输出Token: ${fmt(totalOutput)}`);
  console.log(`  💾 缓存读: ${fmt(totalCacheRead)}`);
  console.log(`  💿 缓存写: ${fmt(totalCacheWrite)}`);
  console.log(`  💰 总费用: $${totalCost.toFixed(4)}`);
  console.log('─'.repeat(50));
  console.log('  按模型:');
  for (const [model, stats] of Object.entries(byModel)) {
    console.log(`    ${model}: in=${fmt(stats.input)} out=${fmt(stats.output)} $${stats.cost.toFixed(4)}`);
  }
  
  if (period !== 'today' && dates.length > 1) {
    console.log('─'.repeat(50));
    console.log('  每日详情:');
    for (const date of dates) {
      const s = byDate[date];
      if (s) {
        const d = new Date(date);
        const dayName = ['日','一','二','三','四','五','六'][d.getDay()];
        console.log(`    ${date} (${dayName}): ${s.conversationCount}次 $${s.totalCost.toFixed(4)}`);
      }
    }
  }
  console.log('═'.repeat(50) + '\n');
}

// 显示按模型的统计
function showByModel() {
  const data = loadData();
  console.log('\n🤖 模型使用统计');
  console.log('═'.repeat(50));
  
  const models = Object.entries(data.models).sort((a, b) => b[1].totalCost - a[1].totalCost);
  
  if (models.length === 0) {
    console.log('  暂无数据');
  } else {
    for (const [model, stats] of models) {
      console.log(`  ${model}`);
      console.log(`    输入: ${fmt(stats.totalInput)} | 输出: ${fmt(stats.totalOutput)}`);
      console.log(`    费用: $${stats.totalCost.toFixed(4)} | 最后使用: ${stats.lastUsed}`);
      console.log('');
    }
  }
  console.log('═'.repeat(50) + '\n');
}

// CLI 入口
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Token统计工具 - 用法:');
  console.log('  node track.js add --input 5000 --output 3000 --cost 0.05 --model MiniMax-M2');
  console.log('  node track.js show --period today|week|month');
  console.log('  node track.js by-model');
  process.exit(0);
}

const command = args[0];

if (command === 'add') {
  let input = 0, output = 0, cacheRead = 0, cacheWrite = 0, webSearch = 0, cost = 0, model = 'unknown';
  
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--input') input = parseInt(args[++i]) || 0;
    if (args[i] === '--output') output = parseInt(args[++i]) || 0;
    if (args[i] === '--cache-read') cacheRead = parseInt(args[++i]) || 0;
    if (args[i] === '--cache-write') cacheWrite = parseInt(args[++i]) || 0;
    if (args[i] === '--web-search') webSearch = parseInt(args[++i]) || 0;
    if (args[i] === '--cost') cost = parseFloat(args[++i]) || 0;
    if (args[i] === '--model') model = args[++i] || 'unknown';
  }
  
  addRecord(input, output, cacheRead, cacheWrite, webSearch, cost, model);
} else if (command === 'show') {
  let period = 'today';
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--period') period = args[++i] || 'today';
  }
  showStats(period);
} else if (command === 'by-model') {
  showByModel();
} else {
  console.log('未知命令:', command);
  process.exit(1);
}
