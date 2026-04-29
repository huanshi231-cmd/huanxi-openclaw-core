#!/bin/bash
# 每日塔罗发送脚本

cd /Users/huanxi/.openclaw/workspace-neirong

# 生成内容
CONTENT=$(python3 scripts/daily_tarot.py)

# 保存到日志文件
echo "=== $(date) ===" >> logs/daily_tarot.log
echo "$CONTENT" >> logs/daily_tarot.log
echo "" >> logs/daily_tarot.log

# 使用openclaw发送到飞书群
# 群聊ID: oc_6c409c73f6d1bc540d0e54d472ea6bf2
echo "$CONTENT" | openclaw message --channel feishu --chat oc_6c409c73f6d1bc540d0e54d472ea6bf2

echo "✅ 每日塔罗已发送"
