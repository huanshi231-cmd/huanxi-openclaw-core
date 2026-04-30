#!/bin/bash
# 系统分身自检脚本 - 基于工程控制论

echo "=== 系统分身自检 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 检查核心文件
echo "1. 核心文件检查:"
for f in SOUL.md USER.md IDENTITY.md SELF_CONTROL.md; do
    if [ -f "$HOME/.openclaw/workspace-system/$f" ]; then
        echo "  ✅ $f 存在"
    else
        echo "  ❌ $f 缺失"
    fi
done
echo ""

# 2. 检查反馈文件
echo "2. 反馈文件检查:"
if [ -f "$HOME/.openclaw/workspace-system/memory/feedback.md" ]; then
    lines=$(wc -l < "$HOME/.openclaw/workspace-system/memory/feedback.md")
    echo "  ✅ feedback.md ($lines 行)"
else
    echo "  ❌ feedback.md 缺失"
fi
echo ""

# 3. 检查知识库
echo "3. 知识库检查:"
knowledge_count=$(find "$HOME/.openclaw/workspace-system/knowledge" -name "*.md" 2>/dev/null | wc -l)
echo "  📚 知识库: $knowledge_count 个文件"
echo ""

# 4. 检查系统状态
echo "4. 系统状态:"
if pgrep -f "openclaw" > /dev/null; then
    echo "  ✅ Gateway 运行中"
else
    echo "  ⚠️ Gateway 未运行"
fi
echo ""

# 5. 今日教训
echo "5. 今日教训:"
today=$(date '+%Y-%m-%d')
if [ -f "$HOME/.openclaw/workspace-system/memory/diary/$today.md" ]; then
    echo "  ✅ 日记存在"
else
    echo "  ⚠️ 今日日记未创建"
fi
echo ""

echo "=== 自检完成 ==="
