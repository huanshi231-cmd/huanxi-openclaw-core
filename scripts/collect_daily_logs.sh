#!/bin/bash
# 太阳每日日报收集脚本
# 触发方式：每天 8:00 自动执行
# 作用：读取所有分身昨日日报，汇总后通过 sessions_send 推送给太阳(main)，由太阳生成运营日报

BASE="$HOME/.openclaw"
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$BASE/logs/daily-collect.log"

mkdir -p "$(dirname "$LOG_FILE")"
echo "[$TODAY 08:00] 开始收集 $YESTERDAY 日报..." >> "$LOG_FILE"

WORKSPACES=(
  "workspace-system:系统官"
  "workspace-neirong:内容官"
  "workspace-linggangshenghuo:灵感官"
  "workspace-liaoyuyewu:疗愈业务官"
  "workspace-memory:记忆官"
  "workspace-peixun:培训官"
  "workspace-funeng:赋能官"
  "workspace-fuwu:服务官"
  "workspace-xinmeiyunying:新媒体运营官"
  "workspace-shejiguansheji:设计官"
  "workspace-kechengcehua:课程策划官"
)

REPORT="【每日运营日报】$YESTERDAY\n\n"
MISSING=""

for item in "${WORKSPACES[@]}"; do
  ws="${item%%:*}"
  name="${item##*:}"
  log_path="$BASE/$ws/daily_log/$YESTERDAY.md"

  if [ -f "$log_path" ]; then
    content=$(cat "$log_path")
    REPORT+="## $name\n$content\n\n"
    echo "  ✅ $name: 已读取" >> "$LOG_FILE"
  else
    MISSING+="$name "
    REPORT+="## $name\n（未提交日报）\n\n"
    echo "  ⚠️  $name: 无日报文件" >> "$LOG_FILE"
  fi
done

if [ -n "$MISSING" ]; then
  REPORT+="\n⚠️ 未提交日报：$MISSING\n"
fi

# 保存汇总文件到 main 工作区
OUTPUT_DIR="$BASE/workspace-main/daily_summary"
mkdir -p "$OUTPUT_DIR"
echo -e "$REPORT" > "$OUTPUT_DIR/$YESTERDAY.md"
echo "  已保存汇总: $OUTPUT_DIR/$YESTERDAY.md" >> "$LOG_FILE"

# 通过 sessions_send 推送给太阳(main)，触发它生成运营日报
PROMPT="你是太阳（COO），现在是 $TODAY 早上8点。请阅读以下各分身昨日（$YESTERDAY）的工作日报，生成一份《每日运营日报》推送给欢喜（CEO）。

日报内容如下：

$(echo -e "$REPORT")

请按以下格式生成运营日报：
1. 昨日整体完成情况（1-2句总结）
2. 各部门进展（按部门列出关键成果）
3. 今日重点任务建议（3-5条）
4. 需要欢喜关注或决策的事项"

/opt/homebrew/bin/openclaw sessions_send agent=main "$PROMPT" >> "$LOG_FILE" 2>&1
echo "  已推送给太阳(main)" >> "$LOG_FILE"
echo "[$TODAY 08:00] 收集完成" >> "$LOG_FILE"
